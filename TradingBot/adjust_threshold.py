#!/usr/bin/env python3
"""
Adjust Signal Threshold - Điều chỉnh ngưỡng tín hiệu
"""

import os
import shutil
from datetime import datetime

def backup_config():
    """Backup config file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"scalping_config_backup_{timestamp}.py"
    shutil.copy("scalping_config.py", backup_file)
    print(f"✅ Backup created: {backup_file}")
    return backup_file

def adjust_threshold(new_threshold):
    """Adjust MIN_SIGNAL_STRENGTH threshold"""
    
    # Backup original
    backup_file = backup_config()
    
    # Read current config
    with open("scalping_config.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace threshold
    old_line = f"    MIN_SIGNAL_STRENGTH = 0.3  # Lower threshold for more signals"
    new_line = f"    MIN_SIGNAL_STRENGTH = {new_threshold}  # Adjusted threshold"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Write new config
        with open("scalping_config.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Threshold updated to {new_threshold}")
        print(f"📁 Backup saved as: {backup_file}")
        return True
    else:
        print("❌ Could not find threshold line to replace")
        return False

def show_current_threshold():
    """Show current threshold"""
    try:
        with open("scalping_config.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        for line in content.split("\n"):
            if "MIN_SIGNAL_STRENGTH" in line:
                print(f"📊 Current threshold: {line.strip()}")
                break
    except Exception as e:
        print(f"❌ Error reading config: {e}")

def main():
    import sys
    
    print("🔧 SIGNAL THRESHOLD ADJUSTER")
    print("=" * 40)
    
    show_current_threshold()
    print()
    
    if len(sys.argv) > 1:
        try:
            new_threshold = float(sys.argv[1])
            if 0.0 <= new_threshold <= 1.0:
                if adjust_threshold(new_threshold):
                    print(f"\n💡 Recommendations:")
                    if new_threshold >= 0.7:
                        print("   ⚠️ High threshold - fewer signals, higher quality")
                    elif new_threshold >= 0.5:
                        print("   ⚖️ Medium threshold - balanced signals")
                    elif new_threshold >= 0.3:
                        print("   ✅ Good threshold - more signals")
                    else:
                        print("   🚀 Low threshold - many signals, test carefully")
                    
                    print(f"\n🧪 Test with: python test_signal_frequency.py --quick")
            else:
                print("❌ Threshold must be between 0.0 and 1.0")
        except ValueError:
            print("❌ Invalid threshold value")
    else:
        print("Usage:")
        print("  python adjust_threshold.py 0.2    # Set threshold to 0.2 (more signals)")
        print("  python adjust_threshold.py 0.5    # Set threshold to 0.5 (balanced)")
        print("  python adjust_threshold.py 0.7    # Set threshold to 0.7 (fewer signals)")
        print()
        print("💡 Current recommendations:")
        print("  • 0.1-0.2: Very aggressive (many signals)")
        print("  • 0.3-0.4: Good for testing")
        print("  • 0.5-0.6: Balanced approach")
        print("  • 0.7-0.8: Conservative (fewer signals)")

if __name__ == "__main__":
    main()

