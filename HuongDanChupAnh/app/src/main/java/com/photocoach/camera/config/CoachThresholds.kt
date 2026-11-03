package com.photocoach.camera.config

/**
 * Mọi ngưỡng của phần hướng dẫn nằm ở đây, không rải rác trong code.
 * Từ M5 (F9) các giá trị này sẽ được nạp từ file cấu hình JSON; đây là bản mặc định.
 */
data class CoachThresholds(
    val level: LevelThresholds = LevelThresholds(),
    val analysis: AnalysisThresholds = AnalysisThresholds(),
    val exposure: ExposureThresholds = ExposureThresholds(),
)

data class LevelThresholds(
    /** Lệch ngang dưới ngưỡng này (độ) coi là đã cân bằng. */
    val levelToleranceDeg: Float = 1.5f,
    /** Máy chúc/ngửa dưới ngưỡng này (độ) coi là thẳng đứng. */
    val pitchToleranceDeg: Float = 5f,
    /**
     * Thành phần trọng lực trong mặt phẳng màn hình (m/s²) tối thiểu để góc nghiêng
     * có nghĩa. Khi máy gần nằm ngang (đặt trên bàn) thì ẩn thước.
     */
    val minInPlaneGravity: Float = 3f,
    /** Hệ số lọc thông thấp cho cảm biến (0..1, nhỏ = mượt hơn nhưng chậm hơn). */
    val smoothingAlpha: Float = 0.15f,
)

data class AnalysisThresholds(
    /** Khoảng cách tối thiểu giữa 2 khung được phân tích (80ms ≈ 12 khung/giây). */
    val minFrameIntervalMs: Long = 80,
    /** Kích thước mặt nhỏ nhất ML Kit cần tìm, so với chiều rộng ảnh. */
    val minFaceSize: Float = 0.08f,
    /** Bước lấy mẫu kênh Y khi tính histogram. */
    val lumaSampleStep: Int = 4,
)

data class ExposureThresholds(
    /** Độ sáng (0..255) của chủ thể dưới mức này => thiếu sáng. */
    val underMean: Float = 55f,
    /** Độ sáng trung bình cả khung trên mức này => cháy sáng. */
    val overMean: Float = 205f,
    /** Tỷ lệ điểm cháy (>= clippedLevel) trên mức này => cháy sáng. */
    val overClippedRatio: Float = 0.12f,
    val clippedLevel: Int = 250,
    val darkLevel: Int = 20,
    /** Mặt tối hơn nền theo tỷ lệ này (và nền đủ sáng) => ngược sáng. */
    val backlitFaceToBackgroundRatio: Float = 0.6f,
    val backlitMinBackground: Float = 110f,
)
