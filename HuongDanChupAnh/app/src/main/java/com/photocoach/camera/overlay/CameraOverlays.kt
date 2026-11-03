package com.photocoach.camera.overlay

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.photocoach.camera.R
import com.photocoach.camera.analysis.DeviceTilt
import com.photocoach.camera.config.LevelThresholds
import com.photocoach.camera.ui.theme.CoachAmber
import com.photocoach.camera.ui.theme.CoachGreen
import java.util.Locale
import kotlin.math.abs
import kotlin.math.roundToInt

/** Lưới 1/3, vẽ trên vùng cùng kích thước với PreviewView. */
@Composable
fun RuleOfThirdsGrid(modifier: Modifier = Modifier) {
    Canvas(modifier.fillMaxSize()) {
        val stroke = 1.dp.toPx()
        val color = Color.White.copy(alpha = 0.45f)
        for (i in 1..2) {
            val x = size.width * i / 3f
            val y = size.height * i / 3f
            drawLine(color, Offset(x, 0f), Offset(x, size.height), stroke)
            drawLine(color, Offset(0f, y), Offset(size.width, y), stroke)
        }
    }
}

/**
 * Thước cân bằng: hai vạch cố định theo cạnh ngang màn hình và một đường chân trời
 * xoay theo góc nghiêng thật. Chuyển xanh khi lệch dưới ngưỡng.
 */
@Composable
fun LevelGauge(tilt: DeviceTilt, thresholds: LevelThresholds, modifier: Modifier = Modifier) {
    if (!tilt.rollReliable) return
    val isLevel = abs(tilt.roll) < thresholds.levelToleranceDeg
    val color = if (isLevel) CoachGreen else Color.White
    Column(modifier, horizontalAlignment = Alignment.CenterHorizontally) {
        Canvas(Modifier.size(width = 180.dp, height = 40.dp)) {
            val stroke = 2.dp.toPx()
            val cy = size.height / 2f
            val gap = 22.dp.toPx()
            // Vạch tham chiếu cố định hai bên.
            drawLine(color, Offset(0f, cy), Offset(gap, cy), stroke * 1.5f)
            drawLine(color, Offset(size.width - gap, cy), Offset(size.width, cy), stroke * 1.5f)
            // Đường chân trời xoay theo thế giới (Compose xoay dương = cùng chiều kim đồng hồ).
            rotate(degrees = tilt.roll, pivot = Offset(size.width / 2f, cy)) {
                drawLine(
                    if (isLevel) CoachGreen else CoachAmber,
                    Offset(gap + 6.dp.toPx(), cy),
                    Offset(size.width - gap - 6.dp.toPx(), cy),
                    stroke,
                )
            }
        }
        Text(
            text = if (isLevel) stringResource(R.string.level_ok)
            else stringResource(R.string.level_tilt, formatDeg(tilt.roll)),
            color = color,
            fontSize = 13.sp,
            modifier = Modifier
                .background(Color.Black.copy(alpha = 0.4f), RoundedCornerShape(8.dp))
                .padding(horizontal = 8.dp, vertical = 2.dp),
        )
        Spacer(Modifier.height(4.dp))
        PitchLabel(tilt.pitch, thresholds)
    }
}

@Composable
private fun PitchLabel(pitch: Float, thresholds: LevelThresholds) {
    val text = when {
        abs(pitch) < thresholds.pitchToleranceDeg -> stringResource(R.string.pitch_level)
        pitch < 0 -> stringResource(R.string.pitch_down, formatDeg(pitch))
        else -> stringResource(R.string.pitch_up, formatDeg(pitch))
    }
    Text(
        text = text,
        color = Color.White.copy(alpha = 0.85f),
        fontSize = 12.sp,
        modifier = Modifier
            .background(Color.Black.copy(alpha = 0.4f), RoundedCornerShape(8.dp))
            .padding(horizontal = 8.dp, vertical = 2.dp),
    )
}

private fun formatDeg(deg: Float): String = String.format(Locale.US, "%d", abs(deg).roundToInt())

/** Vòng lấy nét hiện tại điểm chạm rồi mờ dần. [key] đổi mỗi lần chạm để chạy lại hiệu ứng. */
@Composable
fun FocusRing(position: Offset, key: Int) {
    val alpha = remember(key) { Animatable(1f) }
    val scale = remember(key) { Animatable(1.4f) }
    LaunchedEffect(key) {
        scale.animateTo(1f, tween(200))
        alpha.animateTo(0f, tween(durationMillis = 600, delayMillis = 700))
    }
    Canvas(Modifier.fillMaxSize()) {
        val r = 34.dp.toPx() * scale.value
        drawCircle(
            color = CoachAmber.copy(alpha = alpha.value),
            radius = r,
            center = position,
            style = Stroke(width = 2.dp.toPx()),
        )
    }
}

/** Nháy trắng ngắn khi chụp. */
@Composable
fun ShutterFlash(tick: Int) {
    if (tick == 0) return
    val alpha = remember(tick) { Animatable(0.7f) }
    LaunchedEffect(tick) { alpha.animateTo(0f, tween(250)) }
    Box(
        Modifier
            .fillMaxSize()
            .background(Color.White.copy(alpha = alpha.value)),
    )
}
