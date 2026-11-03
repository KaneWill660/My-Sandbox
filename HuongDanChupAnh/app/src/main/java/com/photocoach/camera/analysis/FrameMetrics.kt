package com.photocoach.camera.analysis

/**
 * Khuôn mặt trong khung, chuẩn hoá 0..1 theo vùng ảnh sẽ được chụp (ảnh đứng, chưa lật gương).
 */
data class FaceMetrics(val box: RectN, val trackingId: Int?) {
    /** Chiều cao mặt so với chiều cao khung — số đo chính cho luật khoảng cách (M3). */
    val heightRatio: Float get() = box.height
    val areaRatio: Float get() = box.area
}

/** Số đo thuần Kotlin của một khung hình, đầu vào cho rule engine ở M3. */
data class FrameMetrics(
    val timestampMs: Long,
    val faces: List<FaceMetrics>,
    val exposure: ExposureStats,
    val exposureState: ExposureState,
    val isFrontCamera: Boolean,
) {
    /** Mặt lớn nhất được coi là người mẫu chính. */
    val primaryFace: FaceMetrics? get() = faces.maxByOrNull { it.areaRatio }
}
