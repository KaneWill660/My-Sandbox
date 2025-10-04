using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wyckoff_Strategy.Model
{
    class DetectionResult
    {
        public double MatchScore { get; set; }
        public Dictionary<string, PhaseRange> Phases { get; set; } = new Dictionary<string, PhaseRange>();
        public List<Marker> Markers { get; set; } = new List<Marker>();
        public int WindowStart { get; set; }
        public int WindowEnd { get; set; }
        public string CurrentPhase { get; set; } = "Unknown"; // A/B/C/D/E/Unknown
        public double Support { get; set; } // ~ SC price
        public double Resistance { get; set; } // ~ AR price
    }
}
