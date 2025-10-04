using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Wyckoff_Strategy.Model;
using Binance.Net.Clients;
using Binance.Net.Enums;
using Binance.Net.Interfaces;

namespace Wyckoff_Strategy.Service
{
    class BinanceService
    {
        private readonly HttpClient _httpClient = new HttpClient();
        private readonly BinanceRestClient _client;

        public BinanceService()
        {
            _client = new BinanceRestClient();
        }

        public async Task<List<Candle>> GetCandlesAsync(string symbol = "BTCUSDT", string interval = "1d", int limit = 100)
        {
            string url = $"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}";
            var response = await _httpClient.GetStringAsync(url);
            var rawData = JsonConvert.DeserializeObject<List<object[]>>(response);

            var candles = new List<Candle>();
            foreach (var item in rawData)
            {
                candles.Add(new Candle
                {
                    Time = DateTimeOffset.FromUnixTimeMilliseconds(Convert.ToInt64(item[0])).UtcDateTime,
                    Open = Convert.ToDouble(item[1]),
                    High = Convert.ToDouble(item[2]),
                    Low = Convert.ToDouble(item[3]),
                    Close = Convert.ToDouble(item[4])
                });
            }
            return candles;
        }

        public async Task<string[]> GetTopPairsAsync(int count)
        {
            var allSymbols = (await _client.SpotApi.ExchangeData.GetExchangeInfoAsync())
                                            .Data.Symbols
                                            .Where(s => s.Name.EndsWith("USDT") && !s.Name.Contains("UP") && !s.Name.Contains("DOWN"))
                                            .Take(count) // lấy 100 cặp đầu tiên
                                            .Select(s => Utility.InsertSlash(s.Name))
                                            .ToList();
            return allSymbols.ToArray();
        }

        public async Task<IEnumerable<IBinanceKline>> GetKlinesAsync(string symbol, KlineInterval interval, int limit)
        {
            var result = await _client.SpotApi.ExchangeData.GetKlinesAsync(symbol, interval, limit: limit);
            if (!result.Success)
                throw new Exception(result.Error?.Message ?? $"Không lấy được dữ liệu cho {symbol}");

            return result.Data;
        }
    }
}
