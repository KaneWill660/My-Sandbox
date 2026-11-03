package com.photocoach.camera.analysis

import com.photocoach.camera.config.ExposureThresholds

/** Nguồn độ sáng (kênh Y) theo toạ độ buffer, tách khỏi ImageProxy để unit test được. */
interface LumaSource {
    val width: Int
    val height: Int
    fun luma(x: Int, y: Int): Int
}

/**
 * Thống kê độ sáng của một khung hình.
 * @property faceMean độ sáng trung bình vùng mặt chính, null nếu không có mặt.
 * @property backgroundMean độ sáng trung bình phần còn lại của khung khi có mặt.
 */
data class ExposureStats(
    val mean: Float,
    val darkRatio: Float,
    val clippedRatio: Float,
    val faceMean: Float? = null,
    val backgroundMean: Float? = null,
)

enum class ExposureState { OK, UNDER, OVER, BACKLIT }

object LumaStats {

    /**
     * Lấy mẫu kênh Y với bước [step] trong vùng [region] (toạ độ buffer), tách riêng vùng [face].
     * Bước 4 trên ảnh 640x480 chỉ khoảng 19 nghìn mẫu — đủ nhanh cho mỗi khung hình.
     */
    fun compute(
        src: LumaSource,
        region: RectN,
        face: RectN?,
        step: Int,
        darkLevel: Int,
        clippedLevel: Int,
    ): ExposureStats {
        val x0 = region.left.toInt().coerceIn(0, src.width)
        val y0 = region.top.toInt().coerceIn(0, src.height)
        val x1 = region.right.toInt().coerceIn(0, src.width)
        val y1 = region.bottom.toInt().coerceIn(0, src.height)
        val faceClip = face?.intersect(region)

        var n = 0L
        var sum = 0L
        var dark = 0L
        var clipped = 0L
        var faceN = 0L
        var faceSum = 0L

        var y = y0
        while (y < y1) {
            var x = x0
            while (x < x1) {
                val v = src.luma(x, y)
                n++
                sum += v
                if (v <= darkLevel) dark++
                if (v >= clippedLevel) clipped++
                if (faceClip != null && x >= faceClip.left && x < faceClip.right && y >= faceClip.top && y < faceClip.bottom) {
                    faceN++
                    faceSum += v
                }
                x += step
            }
            y += step
        }
        if (n == 0L) return ExposureStats(0f, 0f, 0f)

        val bgN = n - faceN
        return ExposureStats(
            mean = sum.toFloat() / n,
            darkRatio = dark.toFloat() / n,
            clippedRatio = clipped.toFloat() / n,
            faceMean = if (faceN > 0) faceSum.toFloat() / faceN else null,
            backgroundMean = if (faceN > 0 && bgN > 0) (sum - faceSum).toFloat() / bgN else null,
        )
    }
}

object ExposureClassifier {

    /** Ngược sáng được ưu tiên vì cụ thể hơn: nền sáng có thể kéo trung bình lên mức "ổn". */
    fun classify(s: ExposureStats, t: ExposureThresholds): ExposureState {
        val face = s.faceMean
        val bg = s.backgroundMean
        if (face != null && bg != null && bg >= t.backlitMinBackground && face < bg * t.backlitFaceToBackgroundRatio) {
            return ExposureState.BACKLIT
        }
        val subject = face ?: s.mean
        return when {
            subject < t.underMean -> ExposureState.UNDER
            s.mean > t.overMean || s.clippedRatio > t.overClippedRatio -> ExposureState.OVER
            else -> ExposureState.OK
        }
    }
}
