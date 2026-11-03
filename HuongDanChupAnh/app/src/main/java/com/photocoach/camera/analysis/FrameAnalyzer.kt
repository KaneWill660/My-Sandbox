package com.photocoach.camera.analysis

import android.os.SystemClock
import android.util.Log
import androidx.annotation.OptIn
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.view.TransformExperimental
import androidx.camera.view.transform.ImageProxyTransformFactory
import androidx.camera.view.transform.OutputTransform
import com.google.android.gms.tasks.Tasks
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.face.FaceDetection
import com.google.mlkit.vision.face.FaceDetectorOptions
import com.photocoach.camera.config.CoachThresholds
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject

/**
 * Kết quả phân tích một khung hình.
 * @property metrics số đo thuần Kotlin cho rule engine.
 * @property facesUpright khung mặt theo toạ độ ảnh đứng (toàn buffer) — dùng để vẽ overlay.
 * @property sourceTransform nguồn của CoordinateTransform khi quy đổi sang PreviewView.
 */
@OptIn(TransformExperimental::class)
class AnalysisFrame(
    val metrics: FrameMetrics,
    val facesUpright: List<RectN>,
    val sourceTransform: OutputTransform,
)

/**
 * F2.1–F2.4: chạy trên luồng nền của ImageAnalysis (KEEP_ONLY_LATEST). Bỏ bớt khung để
 * giữ khoảng 12 khung/giây, nhận diện mặt bằng ML Kit rồi đo histogram kênh Y.
 */
@OptIn(TransformExperimental::class)
class FrameAnalyzer @Inject constructor(
    private val thresholds: CoachThresholds,
) : ImageAnalysis.Analyzer {

    private val detector = FaceDetection.getClient(
        FaceDetectorOptions.Builder()
            .setPerformanceMode(FaceDetectorOptions.PERFORMANCE_MODE_FAST)
            .setMinFaceSize(thresholds.analysis.minFaceSize)
            .enableTracking()
            .build(),
    )

    // Hệ toạ độ nguồn = ảnh đã xoay theo rotationDegrees, khớp với toạ độ ML Kit trả về.
    private val transformFactory = ImageProxyTransformFactory().apply { isUsingRotationDegrees = true }

    private val _frames = MutableStateFlow<AnalysisFrame?>(null)
    val frames: StateFlow<AnalysisFrame?> = _frames.asStateFlow()

    @Volatile
    var isFrontCamera: Boolean = false

    private var lastAnalyzedMs = 0L

    fun reset() {
        _frames.value = null
    }

    @OptIn(ExperimentalGetImage::class)
    override fun analyze(proxy: ImageProxy) {
        proxy.use {
            val now = SystemClock.elapsedRealtime()
            if (now - lastAnalyzedMs < thresholds.analysis.minFrameIntervalMs) return
            lastAnalyzedMs = now

            val media = proxy.image ?: return
            val rotation = proxy.imageInfo.rotationDegrees
            val bufW = proxy.width
            val bufH = proxy.height

            val faces = try {
                Tasks.await(detector.process(InputImage.fromMediaImage(media, rotation)))
            } catch (e: Exception) {
                Log.w(TAG, "Face detection failed", e)
                emptyList()
            }

            // Vùng sẽ được chụp (ViewPort) theo toạ độ buffer và theo ảnh đứng.
            val crop = proxy.cropRect.let { RectN(it.left.toFloat(), it.top.toFloat(), it.right.toFloat(), it.bottom.toFloat()) }
            val cropUpright = ImageGeometry.bufferToUpright(crop, rotation, bufW, bufH)

            val facesUpright = faces.map {
                val b = it.boundingBox
                RectN(b.left.toFloat(), b.top.toFloat(), b.right.toFloat(), b.bottom.toFloat())
            }
            val faceMetrics = faces.zip(facesUpright).map { (face, box) ->
                FaceMetrics(ImageGeometry.normalizeIn(box, cropUpright), face.trackingId)
            }
            val primaryUpright = facesUpright.maxByOrNull { it.area }

            val e = thresholds.exposure
            val stats = LumaStats.compute(
                src = YPlaneSource(proxy.planes[0], bufW, bufH),
                region = crop,
                face = primaryUpright?.let { ImageGeometry.uprightToBuffer(it, rotation, bufW, bufH) },
                step = thresholds.analysis.lumaSampleStep,
                darkLevel = e.darkLevel,
                clippedLevel = e.clippedLevel,
            )

            val metrics = FrameMetrics(
                timestampMs = now,
                faces = faceMetrics,
                exposure = stats,
                exposureState = ExposureClassifier.classify(stats, e),
                isFrontCamera = isFrontCamera,
            )
            _frames.value = AnalysisFrame(metrics, facesUpright, transformFactory.getOutputTransform(proxy))
        }
    }

    fun close() = detector.close()

    private companion object {
        const val TAG = "FrameAnalyzer"
    }
}

private class YPlaneSource(
    plane: ImageProxy.PlaneProxy,
    override val width: Int,
    override val height: Int,
) : LumaSource {
    private val buffer = plane.buffer
    private val rowStride = plane.rowStride
    private val pixelStride = plane.pixelStride

    override fun luma(x: Int, y: Int): Int = buffer.get(y * rowStride + x * pixelStride).toInt() and 0xFF
}
