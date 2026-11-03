package com.photocoach.camera.overlay

import android.graphics.RectF
import androidx.annotation.OptIn
import androidx.camera.view.PreviewView
import androidx.camera.view.TransformExperimental
import androidx.camera.view.transform.CoordinateTransform
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.photocoach.camera.R
import com.photocoach.camera.analysis.AnalysisFrame
import com.photocoach.camera.analysis.ExposureState
import com.photocoach.camera.ui.theme.CoachAmber
import java.util.Locale
import kotlin.math.roundToInt

/**
 * F4.1/F4.4: vẽ khung mặt lên vùng có cùng kích thước PreviewView. Toạ độ ảnh đứng của
 * ML Kit được quy đổi bằng CameraX CoordinateTransform, nên tự đúng khi xoay màn hình
 * và khi camera trước lật gương.
 */
@OptIn(TransformExperimental::class)
@Composable
fun FaceOverlay(frame: AnalysisFrame, previewView: PreviewView, modifier: Modifier = Modifier) {
    if (frame.facesUpright.isEmpty()) return
    // Phải gọi trên luồng chính; null khi preview chưa sẵn sàng.
    val target = previewView.outputTransform ?: return
    val transform = CoordinateTransform(frame.sourceTransform, target)
    val primary = frame.facesUpright.maxByOrNull { it.area }
    val mapped = frame.facesUpright.map { r ->
        RectF(r.left, r.top, r.right, r.bottom).also(transform::mapRect) to (r === primary)
    }
    Canvas(modifier.fillMaxSize()) {
        mapped.forEach { (rect, isPrimary) ->
            drawCornerBox(rect, if (isPrimary) Color.White else Color.White.copy(alpha = 0.5f), isPrimary)
        }
    }
}

private fun DrawScope.drawCornerBox(r: RectF, color: Color, thick: Boolean) {
    val stroke = (if (thick) 3.dp else 2.dp).toPx()
    val len = minOf(r.width(), r.height()) * 0.25f
    val corners = listOf(
        Triple(Offset(r.left, r.top), 1f, 1f),
        Triple(Offset(r.right, r.top), -1f, 1f),
        Triple(Offset(r.left, r.bottom), 1f, -1f),
        Triple(Offset(r.right, r.bottom), -1f, -1f),
    )
    corners.forEach { (p, dx, dy) ->
        drawLine(color, p, Offset(p.x + dx * len, p.y), stroke, StrokeCap.Round)
        drawLine(color, p, Offset(p.x, p.y + dy * len), stroke, StrokeCap.Round)
    }
}

/** F2.4: chip báo thiếu/cháy/ngược sáng (M3 sẽ thay bằng gợi ý kèm hành động). */
@Composable
fun ExposureChip(state: ExposureState, modifier: Modifier = Modifier) {
    val text = when (state) {
        ExposureState.OK -> return
        ExposureState.UNDER -> stringResource(R.string.exposure_under)
        ExposureState.OVER -> stringResource(R.string.exposure_over)
        ExposureState.BACKLIT -> stringResource(R.string.exposure_backlit)
    }
    Text(
        text = text,
        color = Color.Black,
        fontSize = 14.sp,
        modifier = modifier
            .background(CoachAmber, RoundedCornerShape(12.dp))
            .padding(horizontal = 12.dp, vertical = 4.dp),
    )
}

/** Số đo thô để kiểm tra M2 trên máy thật. */
@Composable
fun AnalysisDebugInfo(frame: AnalysisFrame, modifier: Modifier = Modifier) {
    val m = frame.metrics
    val e = m.exposure
    val face = m.primaryFace
    val text = buildString {
        append(stringResource(R.string.debug_faces, m.faces.size))
        if (face != null) {
            append(" · ")
            append(stringResource(R.string.debug_face_height, (face.heightRatio * 100).roundToInt()))
        }
        append(" · ")
        append(stringResource(R.string.debug_luma, e.mean.roundToInt(), (e.clippedRatio * 100).roundToInt()))
        if (e.faceMean != null && e.backgroundMean != null && e.backgroundMean > 0f) {
            append(" · ")
            append(stringResource(R.string.debug_face_bg, String.format(Locale.US, "%.2f", e.faceMean / e.backgroundMean)))
        }
    }
    Text(
        text = text,
        color = Color.White,
        fontSize = 11.sp,
        modifier = modifier
            .background(Color.Black.copy(alpha = 0.55f), RoundedCornerShape(6.dp))
            .padding(horizontal = 6.dp, vertical = 2.dp),
    )
}
