using OxyPlot;
using OxyPlot.Annotations;
using OxyPlot.Axes;
using OxyPlot.Series;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wyckoff_Strategy.Model;

namespace Wyckoff_Strategy.Strategy
{
    // USAGE IN WPF (XAML):
    // 1) Install OxyPlot.Wpf from NuGet
    // 2) In MainWindow.xaml: xmlns:oxy="http://oxyplot.org/wpf"
    //    <oxy:PlotView x:Name="PlotView" Model="{Binding PlotModel}" />
    // 3) In code-behind or ViewModel: var model = WyckoffPlotter.CreatePlotModel(windowCandles, detectionResult);
    //    PlotView.Model = model;
    class WyckoffPlotter
    {
        // Create a PlotModel for a given window of candles and detection result
        // Requires NuGet: OxyPlot.Wpf (for WPF) or OxyPlot.Core + OxyPlot.Wpf
        public PlotModel CreatePlotModel(List<Candle> window, DetectionResult result, string title = "Wyckoff Scan")
        {
            var pm = new PlotModel { Title = title };

            // Axes
            var xAxis = new LinearAxis { Position = AxisPosition.Bottom, Minimum = 0, Maximum = window.Count - 1, MajorStep = Math.Max(1, window.Count / 10) };
            var yMin = window.Min(c => c.Low);
            var yMax = window.Max(c => c.High);
            var yPad = (yMax - yMin) * 0.08;
            var yAxis = new LinearAxis { Position = AxisPosition.Left, Minimum = yMin - yPad, Maximum = yMax + yPad };
            pm.Axes.Add(xAxis); pm.Axes.Add(yAxis);

            // Candles
            var cs = new CandleStickSeries { StrokeThickness = 1, IncreasingColor = OxyColors.ForestGreen, DecreasingColor = OxyColors.IndianRed };
            for (int i = 0; i < window.Count; i++)
            {
                var c = window[i];
                cs.Items.Add(new HighLowItem(i, c.High, c.Low, c.Open, c.Close));
            }
            pm.Series.Add(cs);

            // Phase rectangles
            var phaseColors = new Dictionary<string, OxyColor>
            {
                { "A", OxyColor.FromAColor(60, OxyColors.LightBlue) },
                { "B", OxyColor.FromAColor(40, OxyColors.LightGreen) },
                { "C", OxyColor.FromAColor(60, OxyColors.LightSalmon) },
                { "D", OxyColor.FromAColor(40, OxyColors.LightGoldenrodYellow) }
            };
            foreach (var kv in result.Phases)
            {
                var name = kv.Key; var pr = kv.Value; if (pr == null) continue;
                double x0 = pr.StartIndex - 0.5; double x1 = pr.EndIndex + 0.5;
                var rect = new RectangleAnnotation
                {
                    MinimumX = x0,
                    MaximumX = x1,
                    MinimumY = yMin - yPad,
                    MaximumY = yMax + yPad,
                    Fill = phaseColors.ContainsKey(name) ? phaseColors[name] : OxyColor.FromAColor(40, OxyColors.Gray),
                    Layer = AnnotationLayer.BelowSeries,
                    Text = name,
                    TextHorizontalAlignment = HorizontalAlignment.Left,
                    TextVerticalAlignment = VerticalAlignment.Top
                };
                pm.Annotations.Add(rect);
            }

            // Markers
            foreach (var m in result.Markers)
            {
                OxyColor color;
                switch (m.Name)
                {
                    case "SC":
                        color = OxyColors.Red;
                        break;
                    case "AR":
                        color = OxyColors.Blue;
                        break;
                    case "SPRING":
                        color = OxyColors.Orange;
                        break;
                    case "SOS":
                        color = OxyColors.Green;
                        break;
                    case "LPS":
                        color = OxyColors.DarkGreen;
                        break;
                    default:
                        color = OxyColors.Black;
                        break;
                }

                var line = new LineAnnotation
                {
                    Type = LineAnnotationType.Vertical,
                    X = m.Index,
                    Text = m.Name,
                    TextOrientation = AnnotationTextOrientation.Horizontal,
                    StrokeThickness = 1.5,
                    LineStyle = LineStyle.Solid,
                    Color = color
                };
                pm.Annotations.Add(line);

                var txt = new TextAnnotation
                {
                    Text = m.Name + ": " + m.Price.ToString("F2"),
                    TextPosition = new DataPoint(m.Index + 0.4, (yMax + yMin) / 2),
                    FontSize = 10,
                    Stroke = OxyColors.Transparent
                };
                pm.Annotations.Add(txt);
            }

            // Entry hints + Range lines
            foreach (var m in result.Markers.Where(mm => mm.Name == "SPRING" || mm.Name == "LPS"))
            {
                var h = new LineAnnotation
                {
                    Type = LineAnnotationType.Horizontal,
                    Y = m.Price,
                    Text = "Entry: " + m.Name,
                    LineStyle = LineStyle.Dash,
                    StrokeThickness = 1,
                    Color = m.Name == "SPRING" ? OxyColors.Orange : OxyColors.DarkGreen
                };
                pm.Annotations.Add(h);
            }

            pm.Annotations.Add(new LineAnnotation { Type = LineAnnotationType.Horizontal, Y = result.Support, Color = OxyColors.SteelBlue, LineStyle = LineStyle.Dot, Text = "Support" });
            pm.Annotations.Add(new LineAnnotation { Type = LineAnnotationType.Horizontal, Y = result.Resistance, Color = OxyColors.DarkSlateGray, LineStyle = LineStyle.Dot, Text = "Resistance" });

            pm.Title = ($"{title} | Phase: {result.CurrentPhase} | Score: {result.MatchScore}%");
            return pm;
        }
    }
}
