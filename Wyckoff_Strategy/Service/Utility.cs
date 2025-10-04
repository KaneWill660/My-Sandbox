using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wyckoff_Strategy.Service
{
    class Utility
    {
        public static string InsertSlash(string symbol)
        {
            if (symbol.EndsWith("USDT"))
                return symbol.Replace("USDT", "/USDT");
            return symbol; // Trường hợp không phải USDT
        }
        public static string RemoveSlash(string symbol)
        {
            if (symbol.EndsWith("/USDT"))
                return symbol.Replace("/USDT", "USDT");
            return symbol; // Trường hợp không phải USDT
        }
    }
}
