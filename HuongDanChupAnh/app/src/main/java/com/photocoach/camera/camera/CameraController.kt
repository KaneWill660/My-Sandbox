package com.photocoach.camera.camera

import android.content.ContentValues
import android.content.Context
import android.net.Uri
import android.os.Build
import android.provider.MediaStore
import androidx.camera.core.Camera
import androidx.camera.core.CameraSelector
import androidx.camera.core.FocusMeteringAction
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.MeteringPoint
import androidx.camera.core.Preview
import androidx.camera.core.resolutionselector.AspectRatioStrategy
import androidx.camera.core.resolutionselector.ResolutionSelector
import androidx.camera.core.resolutionselector.ResolutionStrategy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleOwner
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.suspendCancellableCoroutine
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

enum class LensFacing { BACK, FRONT }

enum class FlashMode(val cameraX: Int) {
    OFF(ImageCapture.FLASH_MODE_OFF),
    AUTO(ImageCapture.FLASH_MODE_AUTO),
    ON(ImageCapture.FLASH_MODE_ON);

    fun next(): FlashMode = entries[(ordinal + 1) % entries.size]
}

/** Khả năng của camera vừa mở, để UI ẩn các nút máy không hỗ trợ. */
data class CameraCapabilities(
    val lens: LensFacing,
    val hasFlash: Boolean,
    val canSwitchLens: Boolean,
)

/**
 * Bọc CameraX: Preview + ImageCapture (M2 sẽ thêm ImageAnalysis).
 * Preview và ảnh chụp cùng tỷ lệ 4:3 để khung nhìn khớp với ảnh lưu.
 */
class CameraController @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    private var provider: ProcessCameraProvider? = null
    private var camera: Camera? = null

    private val ratio4x3 = AspectRatioStrategy.RATIO_4_3_FALLBACK_AUTO_STRATEGY

    private val preview = Preview.Builder()
        .setResolutionSelector(ResolutionSelector.Builder().setAspectRatioStrategy(ratio4x3).build())
        .build()

    private val imageCapture = ImageCapture.Builder()
        .setCaptureMode(ImageCapture.CAPTURE_MODE_MAXIMIZE_QUALITY)
        .setResolutionSelector(
            ResolutionSelector.Builder()
                .setAspectRatioStrategy(ratio4x3)
                .setResolutionStrategy(ResolutionStrategy.HIGHEST_AVAILABLE_STRATEGY)
                .build(),
        )
        .build()

    suspend fun bind(
        owner: LifecycleOwner,
        surfaceProvider: Preview.SurfaceProvider,
        requested: LensFacing,
        displayRotation: Int,
    ): CameraCapabilities {
        val p = provider ?: awaitCameraProvider().also { provider = it }
        val hasBack = p.hasCamera(CameraSelector.DEFAULT_BACK_CAMERA)
        val hasFront = p.hasCamera(CameraSelector.DEFAULT_FRONT_CAMERA)
        // Dự phòng: máy chỉ có một camera thì dùng camera đó, bất kể yêu cầu.
        val lens = when {
            requested == LensFacing.FRONT && hasFront -> LensFacing.FRONT
            hasBack -> LensFacing.BACK
            else -> LensFacing.FRONT
        }
        val selector =
            if (lens == LensFacing.FRONT) CameraSelector.DEFAULT_FRONT_CAMERA else CameraSelector.DEFAULT_BACK_CAMERA

        setTargetRotation(displayRotation)
        preview.setSurfaceProvider(surfaceProvider)
        p.unbindAll()
        val cam = p.bindToLifecycle(owner, selector, preview, imageCapture)
        camera = cam
        return CameraCapabilities(
            lens = lens,
            hasFlash = cam.cameraInfo.hasFlashUnit(),
            canSwitchLens = hasBack && hasFront,
        )
    }

    private suspend fun awaitCameraProvider(): ProcessCameraProvider = suspendCancellableCoroutine { cont ->
        val future = ProcessCameraProvider.getInstance(context)
        future.addListener(
            {
                try {
                    cont.resume(future.get())
                } catch (e: Exception) {
                    cont.resumeWithException(e.cause ?: e)
                }
            },
            ContextCompat.getMainExecutor(context),
        )
    }

    fun setTargetRotation(displayRotation: Int) {
        preview.targetRotation = displayRotation
        imageCapture.targetRotation = displayRotation
    }

    fun setFlashMode(mode: FlashMode) {
        imageCapture.flashMode = mode.cameraX
    }

    /** F1.4: lấy nét + đo sáng tại điểm chạm; tự huỷ sau vài giây để về chế độ liên tục. */
    fun focusAt(point: MeteringPoint) {
        val action = FocusMeteringAction.Builder(
            point,
            FocusMeteringAction.FLAG_AF or FocusMeteringAction.FLAG_AE,
        ).setAutoCancelDuration(5, TimeUnit.SECONDS).build()
        camera?.cameraControl?.startFocusAndMetering(action)
    }

    /** F1.2: chụp đầy đủ chất lượng, lưu vào MediaStore (Pictures/PhotoCoach từ Android 10). */
    suspend fun takePhoto(): Uri = suspendCancellableCoroutine { cont ->
        val name = "PC_" + SimpleDateFormat("yyyyMMdd_HHmmss_SSS", Locale.US).format(Date())
        val values = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, name)
            put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg")
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                put(MediaStore.MediaColumns.RELATIVE_PATH, "Pictures/PhotoCoach")
            }
        }
        val options = ImageCapture.OutputFileOptions.Builder(
            context.contentResolver,
            MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
            values,
        ).build()
        imageCapture.takePicture(
            options,
            ContextCompat.getMainExecutor(context),
            object : ImageCapture.OnImageSavedCallback {
                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    val uri = output.savedUri
                    if (uri != null) cont.resume(uri)
                    else cont.resumeWithException(IllegalStateException("MediaStore returned no URI"))
                }

                override fun onError(exception: ImageCaptureException) {
                    cont.resumeWithException(exception)
                }
            },
        )
    }

    fun unbind() {
        provider?.unbindAll()
        camera = null
    }
}
