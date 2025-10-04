using Binance.Net.Enums;
using Binance.Net.Interfaces;
using LiveCharts.Definitions.Series;
using LiveCharts.Wpf;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using Wyckoff_Strategy.Model;
using Wyckoff_Strategy.Service;
using Wyckoff_Strategy.Strategy;

namespace Wyckoff_Strategy
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private readonly BinanceService _binanceService = new BinanceService();
        private WyckoffAnalyzer _wyckoffAnalyzer = new WyckoffAnalyzer();
        private WyckoffDetector wyckoffDetector = new WyckoffDetector();
        private WyckoffPlotter wyckoffPlotter = new WyckoffPlotter();
        public MainWindow()
        {
            InitializeComponent();
            LoadPairs();
        }

        private async void LoadPairs()
        {
            try
            {
                ObservableCollection<string> results = new ObservableCollection<string>();
                lstResults.ItemsSource = results;

                var pairs = await _binanceService.GetTopPairsAsync(5000);
                foreach(string pair in pairs)
                {
                    string selectedPair = Utility.RemoveSlash(pair);
                    IEnumerable<Candle> candles = await LoadChart(selectedPair);
                    DetectionResult detectionResult = wyckoffDetector.DetectBestMatch(candles.ToList());
                    
                    if (detectionResult != null )
                    {
                        var window = candles.Skip(detectionResult.WindowStart).Take(detectionResult.WindowEnd - detectionResult.WindowStart + 1).ToList();
                        if(wyckoffDetector.IsNearPhaseE(detectionResult, window))
                        {
                            string output = $"PAIR: {pair}, Score: {detectionResult.MatchScore}, Phase: {detectionResult.CurrentPhase}";
                            Console.WriteLine(output);
                            results.Add(selectedPair);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Lỗi khi tải danh sách cặp: {ex.Message}");
            }
        }

        private async void lstResults_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (lstResults.SelectedItem == null) return;
            string selectedPair = Utility.RemoveSlash(lstResults.SelectedItem.ToString());
            IEnumerable<Candle> candles = await LoadChart(selectedPair);
            //DrawChart(candles, selectedPair);
            //DrawCandlestickChart(candles);
            // Hiển thị chart
            DetectionResult detectionResult = wyckoffDetector.DetectBestMatch(candles.ToList());
            wpfPlot.Model = wyckoffPlotter.CreatePlotModel(candles.ToList(), detectionResult);
        }

        private async Task<IEnumerable<Candle>> LoadChart(string symbol)
        {
            try
            {
                var candles = await _binanceService.GetKlinesAsync(symbol, KlineInterval.OneDay, Define.CandleLimit);
                var candleList = candles.Select(c => new Candle {
                    Time = c.OpenTime,
                    Open = (double)c.OpenPrice,
                    High = (double)c.HighPrice,
                    Low = (double)c.LowPrice,
                    Close = (double)c.ClosePrice,
                    Volume = (double)c.Volume,
                });

                return candleList;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Lỗi vẽ biểu đồ: {ex.Message}");
                return null;
            }
        }

        //private void DrawChart(IEnumerable<Candle> candles, string symbol)
        //{
        //    var ohlcs = candles.Select(c => new ScottPlot.OHLC(
        //            open: (double)c.Open,
        //            high: (double)c.High,
        //            low: (double)c.Low,
        //            close: (double)c.Close,
        //            timeStart: c.Time,
        //            timeSpan: TimeSpan.FromDays(1)
        //        )).ToArray();

        //    wpfPlot.Plot.Clear();
        //    wpfPlot.Plot.AddCandlesticks(ohlcs);
        //    wpfPlot.Plot.XAxis.DateTimeFormat(true);
        //    wpfPlot.Plot.Title($"{symbol} - Daily");
        //    wpfPlot.Plot.YLabel("Price (USDT)");

        //    wpfPlot.Refresh();
        //}

        private string FormatPair(string pair)
        {
            return pair.Insert(pair.Length - 4, "/");
        }

        //private void DrawCandlestickChart(IEnumerable<Candle> candles)
        //{
        //    // Xóa biểu đồ cũ
        //    wpfPlot.Plot.Clear();

        //    // Chuyển dữ liệu sang OHLC array
        //    var ohlcs = candles.Select((c, i) => new ScottPlot.OHLC(
        //        open: (double)c.Open,
        //        high: (double)c.High,
        //        low: (double)c.Low,
        //        close: (double)c.Close,
        //        timeStart: c.Time,
        //        timeSpan: TimeSpan.FromDays(1)
        //    )).ToArray();

        //    // Thêm candlestick plot
        //    var candlePlot = wpfPlot.Plot.AddCandlesticks(ohlcs);
        //    candlePlot.WickColor = System.Drawing.Color.Gray;
        //    candlePlot.ColorDown = System.Drawing.Color.Red;
        //    candlePlot.ColorUp = System.Drawing.Color.Green;

        //    // Vẽ các đường trendline Wyckoff
        //    double support = ohlcs.Min(c => c.Low);
        //    double resistance = ohlcs.Max(c => c.High);
        //    wpfPlot.Plot.AddHorizontalLine(support, color: System.Drawing.Color.Blue, width: 2);
        //    wpfPlot.Plot.AddHorizontalLine(resistance, color: System.Drawing.Color.Blue, width: 2);

        //    // Thêm annotation các phase (A, B, C, D)
        //    wpfPlot.Plot.AddAnnotation("Phase A", x: ohlcs.Length * 0.1, y: resistance + 2);
        //    //wpfPlot.Plot.AddAnnotation("Phase B", x: ohlcs.Length * 0.3, y: resistance + 2);
        //    //wpfPlot.Plot.AddAnnotation("Phase C", x: ohlcs.Length * 0.6, y: resistance + 2);
        //    //wpfPlot.Plot.AddAnnotation("Phase D", x: ohlcs.Length * 0.8, y: resistance + 2);

        //    wpfPlot.Plot.Legend();

        //    // Render
        //    wpfPlot.Refresh();
        //}

        // Trả về (a, b) trong y = a + b*x
        private (double a, double b) LinearRegression(IList<double> y, int xOffset = 0)
        {
            int n = y.Count;
            if (n == 0) return (0, 0);

            double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

            for (int i = 0; i < n; i++)
            {
                double x = i + xOffset;    // dùng index thực trên trục X (khớp với OHLC index)
                double yi = y[i];

                sumX += x;
                sumY += yi;
                sumXY += x * yi;
                sumX2 += x * x;
            }

            double denom = n * sumX2 - (sumX * sumX);
            if (Math.Abs(denom) < 1e-9)
                return (sumY / n, 0); // tránh chia 0 → đường ngang trung bình

            double b = (n * sumXY - sumX * sumY) / denom;
            double a = (sumY - b * sumX) / n;
            return (a, b);
        }

        private void btnScanAll_Click(object sender, RoutedEventArgs e)
        {

            LoadPairs();
        }
    }
}
