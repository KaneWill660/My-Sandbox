package com.photocoach.camera.analysis

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class TiltMathTest {

    private val g = 9.81f
    private val eps = 0.5f

    @Test
    fun `upright portrait is level and vertical`() {
        val t = TiltMath.tilt(Gravity(0f, g, 0f), displayRotationDeg = 0, minInPlaneGravity = 3f)
        assertEquals(0f, t.roll, eps)
        assertEquals(0f, t.pitch, eps)
        assertTrue(t.rollReliable)
    }

    @Test
    fun `landscape rotation 90 is level on screen`() {
        // Xoay máy ngược chiều kim đồng hồ 90°: cạnh phải hướng lên, trọng lực nằm trên trục +x.
        val t = TiltMath.tilt(Gravity(g, 0f, 0f), displayRotationDeg = 90, minInPlaneGravity = 3f)
        assertEquals(0f, t.roll, eps)
    }

    @Test
    fun `landscape rotation 270 is level on screen`() {
        val t = TiltMath.tilt(Gravity(-g, 0f, 0f), displayRotationDeg = 270, minInPlaneGravity = 3f)
        assertEquals(0f, t.roll, eps)
    }

    @Test
    fun `upside down portrait is level on screen`() {
        val t = TiltMath.tilt(Gravity(0f, -g, 0f), displayRotationDeg = 180, minInPlaneGravity = 3f)
        assertEquals(0f, t.roll, eps)
    }

    @Test
    fun `clockwise tilt gives negative roll`() {
        // Máy xoay 10° theo chiều kim đồng hồ: hướng "lên" có thành phần x âm.
        val rad = Math.toRadians(10.0)
        val gravity = Gravity((-g * Math.sin(rad)).toFloat(), (g * Math.cos(rad)).toFloat(), 0f)
        val t = TiltMath.tilt(gravity, displayRotationDeg = 0, minInPlaneGravity = 3f)
        assertEquals(-10f, t.roll, eps)
    }

    @Test
    fun `camera pointing down gives negative pitch`() {
        val rad = Math.toRadians(30.0)
        // Ngả đỉnh máy ra sau 30° => camera sau chúc xuống, trọng lực có thành phần +z.
        val gravity = Gravity(0f, (g * Math.cos(rad)).toFloat(), (g * Math.sin(rad)).toFloat())
        val t = TiltMath.tilt(gravity, displayRotationDeg = 0, minInPlaneGravity = 3f)
        assertEquals(-30f, t.pitch, eps)
    }

    @Test
    fun `phone lying flat makes roll unreliable`() {
        val t = TiltMath.tilt(Gravity(0.2f, 0.3f, g), displayRotationDeg = 0, minInPlaneGravity = 3f)
        assertFalse(t.rollReliable)
        assertEquals(-90f, t.pitch, 3f)
    }

    @Test
    fun `normalize wraps into half-open range`() {
        assertEquals(180f, TiltMath.normalize(-180f), 0.001f)
        assertEquals(-90f, TiltMath.normalize(270f), 0.001f)
        assertEquals(10f, TiltMath.normalize(370f), 0.001f)
        assertEquals(0f, TiltMath.normalize(-360f), 0.001f)
    }

    @Test
    fun `low pass moves partially toward new value`() {
        val out = TiltMath.lowPass(Gravity(0f, 0f, 0f), Gravity(10f, 10f, 10f), alpha = 0.25f)
        assertEquals(2.5f, out.x, 0.001f)
        assertEquals(Gravity(1f, 2f, 3f), TiltMath.lowPass(null, Gravity(1f, 2f, 3f), 0.5f))
    }
}
