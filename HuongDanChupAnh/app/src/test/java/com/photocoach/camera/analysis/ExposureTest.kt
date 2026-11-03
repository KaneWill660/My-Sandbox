package com.photocoach.camera.analysis

import com.photocoach.camera.config.ExposureThresholds
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class ExposureTest {

    private val t = ExposureThresholds()

    /** Ảnh giả: nền có độ sáng [bg], vùng [face] có độ sáng [faceLuma]. */
    private fun image(bg: Int, face: RectN? = null, faceLuma: Int = bg, w: Int = 64, h: Int = 48) =
        object : LumaSource {
            override val width = w
            override val height = h
            override fun luma(x: Int, y: Int): Int =
                if (face != null && x >= face.left && x < face.right && y >= face.top && y < face.bottom) faceLuma else bg
        }

    private fun stats(src: LumaSource, face: RectN? = null) = LumaStats.compute(
        src,
        region = RectN(0f, 0f, src.width.toFloat(), src.height.toFloat()),
        face = face,
        step = 1,
        darkLevel = t.darkLevel,
        clippedLevel = t.clippedLevel,
    )

    @Test
    fun `uniform image has exact mean and no face stats`() {
        val s = stats(image(100))
        assertEquals(100f, s.mean, 0.001f)
        assertEquals(0f, s.clippedRatio, 0.001f)
        assertNull(s.faceMean)
        assertEquals(ExposureState.OK, ExposureClassifier.classify(s, t))
    }

    @Test
    fun `face and background means are separated`() {
        val face = RectN(16f, 12f, 48f, 36f) // 32x24 = 1/4 ảnh
        val s = stats(image(bg = 200, face = face, faceLuma = 40), face)
        assertEquals(40f, s.faceMean!!, 0.001f)
        assertEquals(200f, s.backgroundMean!!, 0.001f)
        assertEquals(160f, s.mean, 0.001f)
    }

    @Test
    fun `dark face on bright background is backlit`() {
        val face = RectN(16f, 12f, 48f, 36f)
        val s = stats(image(bg = 220, face = face, faceLuma = 70), face)
        assertEquals(ExposureState.BACKLIT, ExposureClassifier.classify(s, t))
    }

    @Test
    fun `face slightly darker than background is not backlit`() {
        val face = RectN(16f, 12f, 48f, 36f)
        val s = stats(image(bg = 160, face = face, faceLuma = 130), face)
        assertEquals(ExposureState.OK, ExposureClassifier.classify(s, t))
    }

    @Test
    fun `dark scene is under exposed`() {
        assertEquals(ExposureState.UNDER, ExposureClassifier.classify(stats(image(30)), t))
    }

    @Test
    fun `dark scene with dark face is under not backlit`() {
        // Nền tối nên không đủ điều kiện ngược sáng.
        val face = RectN(16f, 12f, 48f, 36f)
        val s = stats(image(bg = 60, face = face, faceLuma = 25), face)
        assertEquals(ExposureState.UNDER, ExposureClassifier.classify(s, t))
    }

    @Test
    fun `clipped highlights are over exposed`() {
        val s = stats(image(255))
        assertEquals(1f, s.clippedRatio, 0.001f)
        assertEquals(ExposureState.OVER, ExposureClassifier.classify(s, t))
    }

    @Test
    fun `sampling step and region are respected`() {
        val src = image(100)
        val s = LumaStats.compute(src, RectN(0f, 0f, 10f, 10f), null, step = 5, darkLevel = 20, clippedLevel = 250)
        assertEquals(100f, s.mean, 0.001f)
    }

    @Test
    fun `primary face is the largest`() {
        val small = FaceMetrics(RectN(0f, 0f, 0.1f, 0.1f), 1)
        val big = FaceMetrics(RectN(0.4f, 0.2f, 0.7f, 0.6f), 2)
        val m = FrameMetrics(0, listOf(small, big), ExposureStats(100f, 0f, 0f), ExposureState.OK, false)
        assertEquals(big, m.primaryFace)
        assertEquals(0.4f, big.heightRatio, 0.001f)
    }
}
