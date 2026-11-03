package com.photocoach.camera.analysis

import org.junit.Assert.assertEquals
import org.junit.Test

class ImageGeometryTest {

    // Buffer cảm biến 640x480, mặt ở góc trên-trái của buffer.
    private val w = 640
    private val h = 480
    private val face = RectN(40f, 20f, 140f, 120f)

    @Test
    fun `rotation 0 keeps rect`() {
        assertEquals(face, ImageGeometry.bufferToUpright(face, 0, w, h))
    }

    @Test
    fun `rotation 90 moves top-left of buffer to top-right of upright image`() {
        // Xoay 90° theo chiều kim đồng hồ: ảnh đứng rộng 480, cao 640.
        val r = ImageGeometry.bufferToUpright(face, 90, w, h)
        assertEquals(RectN(360f, 40f, 460f, 140f), r)
        assertEquals(480 to 640, ImageGeometry.uprightSize(w, h, 90))
    }

    @Test
    fun `rotation 180 mirrors both axes`() {
        assertEquals(RectN(500f, 360f, 600f, 460f), ImageGeometry.bufferToUpright(face, 180, w, h))
    }

    @Test
    fun `rotation 270 moves top-left of buffer to bottom-left of upright image`() {
        assertEquals(RectN(20f, 500f, 120f, 600f), ImageGeometry.bufferToUpright(face, 270, w, h))
    }

    @Test
    fun `upright to buffer is the inverse for every rotation`() {
        for (rot in listOf(0, 90, 180, 270)) {
            val upright = ImageGeometry.bufferToUpright(face, rot, w, h)
            assertEquals("rotation $rot", face, ImageGeometry.uprightToBuffer(upright, rot, w, h))
        }
    }

    @Test
    fun `rect area is preserved by rotation`() {
        for (rot in listOf(90, 180, 270)) {
            assertEquals(face.area, ImageGeometry.bufferToUpright(face, rot, w, h).area, 0.001f)
        }
    }

    @Test
    fun `normalize relative to crop frame`() {
        val frame = RectN(0f, 0f, 480f, 640f)
        val n = ImageGeometry.normalizeIn(RectN(120f, 160f, 360f, 320f), frame)
        assertEquals(RectN(0.25f, 0.25f, 0.75f, 0.5f), n)
    }

    @Test
    fun `normalize accounts for crop offset`() {
        val frame = RectN(100f, 0f, 300f, 400f)
        val n = ImageGeometry.normalizeIn(RectN(100f, 100f, 200f, 200f), frame)
        assertEquals(RectN(0f, 0.25f, 0.5f, 0.5f), n)
    }

    @Test
    fun `intersect returns overlap or null`() {
        assertEquals(RectN(50f, 50f, 100f, 100f), RectN(0f, 0f, 100f, 100f).intersect(RectN(50f, 50f, 150f, 150f)))
        assertEquals(null, RectN(0f, 0f, 10f, 10f).intersect(RectN(20f, 20f, 30f, 30f)))
    }
}
