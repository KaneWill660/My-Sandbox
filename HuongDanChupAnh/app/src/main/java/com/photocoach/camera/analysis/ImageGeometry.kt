package com.photocoach.camera.analysis

/** Hình chữ nhật thuần Kotlin (không dùng android.graphics) để unit test được. */
data class RectN(val left: Float, val top: Float, val right: Float, val bottom: Float) {
    val width: Float get() = right - left
    val height: Float get() = bottom - top
    val centerX: Float get() = (left + right) / 2f
    val centerY: Float get() = (top + bottom) / 2f
    val area: Float get() = width.coerceAtLeast(0f) * height.coerceAtLeast(0f)

    fun intersect(other: RectN): RectN? {
        val l = maxOf(left, other.left)
        val t = maxOf(top, other.top)
        val r = minOf(right, other.right)
        val b = minOf(bottom, other.bottom)
        return if (r > l && b > t) RectN(l, t, r, b) else null
    }
}

/**
 * Quy đổi giữa toạ độ buffer của camera (chưa xoay) và ảnh "đứng" (đã xoay theo
 * rotationDegrees, chiều kim đồng hồ) — hệ toạ độ mà ML Kit trả về và rule engine dùng.
 *
 * Việc quy đổi sang toạ độ màn hình (PreviewView) KHÔNG làm ở đây mà dùng
 * CameraX CoordinateTransform (xem overlay/FaceOverlay.kt).
 */
object ImageGeometry {

    fun uprightSize(bufferWidth: Int, bufferHeight: Int, rotationDegrees: Int): Pair<Int, Int> =
        if (rotationDegrees % 180 == 0) bufferWidth to bufferHeight else bufferHeight to bufferWidth

    fun bufferToUpright(r: RectN, rotationDegrees: Int, bufferWidth: Int, bufferHeight: Int): RectN {
        val w = bufferWidth.toFloat()
        val h = bufferHeight.toFloat()
        return when (normalizeRotation(rotationDegrees)) {
            90 -> RectN(h - r.bottom, r.left, h - r.top, r.right)
            180 -> RectN(w - r.right, h - r.bottom, w - r.left, h - r.top)
            270 -> RectN(r.top, w - r.right, r.bottom, w - r.left)
            else -> r
        }
    }

    fun uprightToBuffer(r: RectN, rotationDegrees: Int, bufferWidth: Int, bufferHeight: Int): RectN {
        val (uw, uh) = uprightSize(bufferWidth, bufferHeight, rotationDegrees)
        // Nghịch đảo của xoay θ là xoay (360 - θ) trên ảnh đã xoay.
        return bufferToUpright(r, (360 - normalizeRotation(rotationDegrees)) % 360, uw, uh)
    }

    /** Chuẩn hoá [r] về 0..1 so với vùng [frame] (cùng hệ toạ độ). */
    fun normalizeIn(r: RectN, frame: RectN): RectN = RectN(
        (r.left - frame.left) / frame.width,
        (r.top - frame.top) / frame.height,
        (r.right - frame.left) / frame.width,
        (r.bottom - frame.top) / frame.height,
    )

    private fun normalizeRotation(deg: Int): Int = ((deg % 360) + 360) % 360
}
