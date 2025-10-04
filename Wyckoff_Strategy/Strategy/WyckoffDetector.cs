using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wyckoff_Strategy.Model;

namespace Wyckoff_Strategy.Strategy
{
    // USAGE example (call from WPF ViewModel or code-behind):
    // var result = WyckoffDetector.DetectBestMatch(listOf180Candles);
    // result.MatchScore => percentage
    // result.Markers contains SC, AR, SPRING, SOS, LPS with indices relative to the original list (WindowStart..WindowEnd)
    class WyckoffDetector
    {
        // Public entry: accepts 180 candles and returns best-matching window result
        // windows considered: 60, 90, 120, 150 (sliding)
        public DetectionResult DetectBestMatch(List<Candle> candles)
        {
            if (candles == null || candles.Count < 60) return null;


            var windowSizes = new[] { 60, 90, 120, 150 };
            DetectionResult best = null;


            for (int w = 0; w < windowSizes.Length; w++)
            {
                int sz = windowSizes[w];
                for (int start = 0; start + sz <= candles.Count; start++)
                {
                    var slice = candles.GetRange(start, sz);
                    var r = AnalyzeWindow(slice);
                    r.WindowStart = start;
                    r.WindowEnd = start + sz - 1;
                    if (best == null || r.MatchScore > best.MatchScore) best = r;
                }
            }


            return best;
        }

        // Analyze a single window and return detection result + match score
        public DetectionResult AnalyzeWindow(List<Candle> window)
        {
            var res = new DetectionResult();

            // 1) Prior trend (down) using normalized linear regression slope
            double slope = LinearRegressionSlope(window.Select(c => c.Close).ToArray());
            bool priorDowntrend = slope < -0.0001;

            // 2) Extrema
            var lows = FindLocalExtrema(window, findMin: true, radius: 3);
            var highs = FindLocalExtrema(window, findMin: false, radius: 3);

            // 3) SC
            int scIndex = -1;
            double meanVol = Math.Max(1e-9, window.Average(c => c.Volume));
            double meanRange = Math.Max(1e-9, window.Average(c => c.Range));
            foreach (var idx in lows)
            {
                if (window[idx].Volume >= 1.2 * meanVol && window[idx].Range >= 1.0 * meanRange)
                { scIndex = idx; break; }
            }
            if (scIndex == -1) scIndex = window.Select((c, i) => (c.Low, i)).OrderBy(t => t.Low).First().i;
            res.Markers.Add(new Marker { Name = "SC", Index = scIndex, Price = window[scIndex].Low });

            // 4) AR
            int arIndex = -1; double scPrice = window[scIndex].Low;
            for (int i = scIndex + 1; i < window.Count; i++)
            {
                if (window[i].Close >= scPrice * 1.06) { arIndex = i; break; }
            }
            if (arIndex == -1)
            {
                var postHighs = highs.Where(h => h > scIndex).ToList();
                arIndex = postHighs.Count > 0 ? postHighs.First() : Math.Min(window.Count - 1, scIndex + 5);
            }
            res.Markers.Add(new Marker { Name = "AR", Index = arIndex, Price = window[arIndex].High });

            // 5) Range bounds
            double support = window[scIndex].Low;
            double resistance = window[arIndex].High;
            res.Support = support; res.Resistance = resistance;

            // 6) Phase A
            int phaseAStart = 0;
            int phaseAEnd = Math.Min(window.Count - 1, arIndex + 3);
            res.Phases["A"] = new PhaseRange { StartIndex = phaseAStart, EndIndex = phaseAEnd };

            // 7) Phase B: sideways until Spring
            int bStart = Math.Min(window.Count - 1, phaseAEnd + 1);
            int bEndCandidate = Math.Min(window.Count - 1, bStart + (int)((window.Count - bStart) * 0.6));

            // 8) Spring (Phase C)
            int springIndex = -1; int recoverIdxForSpring = -1;
            for (int i = bStart; i <= Math.Min(window.Count - 1, bEndCandidate + 10); i++)
            {
                if (window[i].Low < support * 0.98)
                {
                    for (int j = i + 1; j <= Math.Min(window.Count - 1, i + 7); j++)
                    {
                        if (window[j].Close > support * 1.01) { recoverIdxForSpring = j; break; }
                    }
                    if (recoverIdxForSpring != -1) { springIndex = i; break; }
                }
            }
            int bEnd = springIndex != -1 ? Math.Max(bStart, springIndex - 1) : bEndCandidate;
            res.Phases["B"] = new PhaseRange { StartIndex = bStart, EndIndex = bEnd };

            if (springIndex != -1)
            {
                res.Markers.Add(new Marker { Name = "SPRING", Index = springIndex, Price = window[springIndex].Low });
                int cStart = Math.Max(bStart, springIndex - 3);
                int cEnd = Math.Min(window.Count - 1, (recoverIdxForSpring != -1 ? recoverIdxForSpring + 2 : springIndex + 5));
                res.Phases["C"] = new PhaseRange { StartIndex = cStart, EndIndex = cEnd };
            }

            // 9) Phase D: SOS breakout + LPS pullback
            int startForDScan = res.Phases.ContainsKey("C") ? res.Phases["C"].EndIndex : bEnd;
            int sosIndex = -1;
            for (int i = Math.Max(0, startForDScan - 5); i < window.Count; i++)
            {
                if (window[i].Close > resistance * 1.01 && window[i].Volume > 1.1 * meanVol)
                { sosIndex = i; break; }
            }
            if (sosIndex != -1)
            {
                res.Markers.Add(new Marker { Name = "SOS", Index = sosIndex, Price = window[sosIndex].Close });
                int dStart = Math.Max(startForDScan + 1, sosIndex - 8);
                int dEnd = Math.Min(window.Count - 1, sosIndex + 12);
                res.Phases["D"] = new PhaseRange { StartIndex = dStart, EndIndex = dEnd };

                // LPS detection
                int lpsIndex = -1;
                for (int i = sosIndex + 1; i < Math.Min(window.Count, sosIndex + 12); i++)
                {
                    bool aboveOldRange = window[i].Low > resistance * 0.985; // pullback stays above/barely into range top
                    bool notHigherHigh = window[i].Close < window[sosIndex].Close;
                    if (aboveOldRange && notHigherHigh)
                    { lpsIndex = i; break; }
                }
                if (lpsIndex != -1)
                    res.Markers.Add(new Marker { Name = "LPS", Index = lpsIndex, Price = window[lpsIndex].Close });
            }

            // 10) Score
            double score = 0;
            score += priorDowntrend ? 15 : 0; // downtrend precondition
            if (scIndex >= 0) score += 15;     // SC
            if (arIndex > scIndex) score += 10; // AR

            // B quality
            int inRangeCount = 0;
            int bCnt = Math.Max(1, bEnd - bStart + 1);
            for (int i = bStart; i <= bEnd; i++)
                if (window[i].High <= resistance * 1.02 && window[i].Low >= support * 0.985) inRangeCount++;
            double bRatio = (double)inRangeCount / bCnt; // 0..1
            score += 20 * Math.Min(1.0, bRatio);

            if (springIndex != -1) score += 20; // Spring
            if (sosIndex != -1) score += 10;    // SOS
            if (res.Markers.Any(m => m.Name == "LPS")) score += 10; // LPS

            res.MatchScore = Math.Round(Math.Max(0, Math.Min(100, score)), 2);

            // 11) Current phase by last bar location and price extension
            int lastIdx = window.Count - 1;
            string current = "Unknown";
            foreach (var kv in res.Phases)
            {
                if (lastIdx >= kv.Value.StartIndex && lastIdx <= kv.Value.EndIndex)
                { current = kv.Key; break; }
            }
            if (current == "Unknown" && res.Phases.ContainsKey("D") && lastIdx > res.Phases["D"].EndIndex)
            {
                var lastClose = window[lastIdx].Close;
                if (lastClose > resistance * 1.01 && lastClose < resistance * 1.08) current = "D"; // still consolidating near top → near E
                else if (lastClose >= resistance * 1.08) current = "E"; // already trending up strongly
            }
            res.CurrentPhase = current;

            // 12) Normalize markers order
            res.Markers = res.Markers.OrderBy(m => m.Index).ToList();

            return res;
        }

        public bool IsNearPhaseE(DetectionResult r, List<Candle> window)
        {
            if (r == null) return false;
            if (r.CurrentPhase != "D") return false;
            bool hasSOS = r.Markers.Any(m => m.Name == "SOS");
            bool hasLPS = r.Markers.Any(m => m.Name == "LPS");
            double lastClose = window.Last().Close;
            bool aboveRes = lastClose > r.Resistance * 1.01;
            bool notExtended = lastClose < r.Resistance * 1.10; // <10% above range top
            return r.MatchScore >= 95 && hasSOS && (hasLPS || lastClose >= r.Resistance * 1.03) && aboveRes && notExtended;
        }

        // ===== Helpers =====
        private double LinearRegressionSlope(double[] ys)
        {
            int n = ys.Length;
            double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
            for (int i = 0; i < n; i++) { sumX += i; sumY += ys[i]; sumXY += i * ys[i]; sumX2 += i * i; }
            double denom = n * sumX2 - sumX * sumX;
            if (Math.Abs(denom) < 1e-12) return 0;
            double slope = (n * sumXY - sumX * sumY) / denom;
            return slope / (ys.Average() + 1e-9); // normalized
        }


        private List<int> FindLocalExtrema(List<Candle> data, bool findMin, int radius)
        {
            var res = new List<int>();
            for (int i = radius; i < data.Count - radius; i++)
            {
                bool ok = true;
                double center = findMin ? data[i].Low : data[i].High;
                for (int j = i - radius; j <= i + radius; j++)
                {
                    if (j == i) continue;
                    double cmp = findMin ? data[j].Low : data[j].High;
                    if (findMin) { if (cmp <= center) { ok = false; break; } }
                    else { if (cmp >= center) { ok = false; break; } }
                }
                if (ok) res.Add(i);
            }
            return res;
        }
    }
}
