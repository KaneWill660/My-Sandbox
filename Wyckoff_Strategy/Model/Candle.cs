using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wyckoff_Strategy.Model
{
    class Candle
    {
        public DateTime Time { get; set; }
        public double Open { get; set; }
        public double High { get; set; }
        public double Low { get; set; }
        public double Close { get; set; }
        public double Volume { get; set; }

        public double Body => Math.Abs(Close - Open);
        public double Range => High - Low;
    }
}
