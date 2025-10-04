using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wyckoff_Strategy.Model;

namespace Wyckoff_Strategy.Strategy
{
    class WyckoffAnalyzer
    {
        /// <summary>
        /// Tính điểm tương đồng của dữ liệu với mô hình Wyckoff Accumulation
        /// </summary>
        /// <param name="candles">Danh sách nến (open, high, low, close, volume, time)</param>
        /// <returns>Score từ 0 đến 100</returns>
        public double CalculateWyckoffScore(List<Candle> candles)
        {
            if (candles == null || candles.Count < 50)
                return 0;

            // Lấy giá trị high, low
            double maxPrice = candles.Max(c => c.High);
            double minPrice = candles.Min(c => c.Low);

            // Kiểm tra biên độ dao động (dấu hiệu tích lũy)
            double range = maxPrice - minPrice;
            if (range <= 0) return 0;

            // Chia dữ liệu thành các giai đoạn (A, B, C, D)
            int chunkSize = candles.Count / 4;
            var phaseA = candles.Take(chunkSize).ToList();
            var phaseB = candles.Skip(chunkSize).Take(chunkSize).ToList();
            var phaseC = candles.Skip(chunkSize * 2).Take(chunkSize).ToList();
            var phaseD = candles.Skip(chunkSize * 3).ToList();

            // Điều kiện cơ bản:
            // - Phase A: xu hướng giảm dần
            bool phaseACondition = phaseA.Last().Close < phaseA.First().Close;
            // - Phase B: dao động trong range
            bool phaseBCondition = phaseB.All(c => c.Low > minPrice * 0.95 && c.High < maxPrice * 1.05);
            // - Phase C: có 1 cú Spring (giá chọc thủng đáy nhẹ rồi bật lại)
            bool phaseCCondition = phaseC.Any(c => c.Low < minPrice * 1.02);
            // - Phase D: xu hướng tăng
            bool phaseDCondition = phaseD.Last().Close > phaseD.First().Close;

            double score = 0;
            if (phaseACondition) score += 25;
            if (phaseBCondition) score += 25;
            if (phaseCCondition) score += 25;
            if (phaseDCondition) score += 25;

            return score;
        }
    }
}
