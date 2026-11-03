package com.photocoach.camera.analysis

import kotlin.math.atan2
import kotlin.math.sqrt

/** Vector trọng lực theo hệ toạ độ của máy (m/s²): x sang phải, y lên trên, z ra khỏi màn hình. */
data class Gravity(val x: Float, val y: Float, val z: Float)

/**
 * Góc nghiêng của máy so với thế giới, đã quy về hướng màn hình hiện tại.
 *
 * @property roll độ lệch ngang (độ) so với cạnh ngang của màn hình hiện tại, trong (-180, 180].
 *   Dương khi máy xoay ngược chiều kim đồng hồ.
 * @property pitch góc chúc/ngửa của camera sau (độ): âm khi chúc xuống, dương khi ngửa lên.
 * @property rollReliable false khi máy gần nằm ngang, lúc đó [roll] không có ý nghĩa.
 */
data class DeviceTilt(val roll: Float, val pitch: Float, val rollReliable: Boolean)

/** Hàm thuần, không phụ thuộc Android, để unit test được. */
object TiltMath {

    private const val RAD_TO_DEG = (180.0 / Math.PI).toFloat()

    /** Góc xoay của máy quanh trục vuông góc màn hình, 0 khi cầm dọc thẳng. */
    fun deviceRoll(g: Gravity): Float = atan2(g.x, g.y) * RAD_TO_DEG

    /** Góc chúc/ngửa của camera sau: 0 khi máy thẳng đứng. */
    fun cameraPitch(g: Gravity): Float = atan2(-g.z, inPlaneMagnitude(g)) * RAD_TO_DEG

    fun inPlaneMagnitude(g: Gravity): Float = sqrt(g.x * g.x + g.y * g.y)

    /**
     * Quy góc roll của máy về hướng màn hình. [displayRotationDeg] là 0/90/180/270
     * tương ứng Surface.ROTATION_0..270.
     */
    fun screenRoll(deviceRoll: Float, displayRotationDeg: Int): Float =
        normalize(deviceRoll - displayRotationDeg)

    fun tilt(g: Gravity, displayRotationDeg: Int, minInPlaneGravity: Float): DeviceTilt =
        DeviceTilt(
            roll = screenRoll(deviceRoll(g), displayRotationDeg),
            pitch = cameraPitch(g),
            rollReliable = inPlaneMagnitude(g) >= minInPlaneGravity,
        )

    /** Đưa góc về khoảng (-180, 180]. */
    fun normalize(deg: Float): Float {
        var a = deg % 360f
        if (a <= -180f) a += 360f
        if (a > 180f) a -= 360f
        return a
    }

    /** Lọc thông thấp đơn giản để thước không rung. */
    fun lowPass(previous: Gravity?, current: Gravity, alpha: Float): Gravity {
        if (previous == null) return current
        return Gravity(
            x = previous.x + alpha * (current.x - previous.x),
            y = previous.y + alpha * (current.y - previous.y),
            z = previous.z + alpha * (current.z - previous.z),
        )
    }
}
