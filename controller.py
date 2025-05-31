#!/usr/bin/env python3
"""
Simple Mini Kinta DMX Controller
Works on all platforms - menu-driven interface
"""

import serial
import time
import threading

PORT = "/dev/cu.usbserial-AQ02YN7D"

class MiniKintaController:
    def __init__(self):
        self.running = False
        self.color = 0
        self.strobe = 0
        self.motor = 0
        
        # Connect to DMX interface
        self.ser = serial.Serial(
            port=PORT,
            baudrate=250000,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=2,
            timeout=1
        )
        print(f"✓ Connected to DMX interface: {PORT}")
        
    def send_dmx_frame(self):
        """Send a single DMX frame"""
        try:
            # DMX Break
            self.ser.break_condition = True
            time.sleep(0.0001)
            self.ser.break_condition = False
            time.sleep(0.00001)
            
            # Create DMX packet
            dmx_data = [0] * 513
            dmx_data[0] = 0           # Start code
            dmx_data[1] = self.color  # Channel 1: Color
            dmx_data[2] = self.strobe # Channel 2: Strobe
            dmx_data[3] = self.motor  # Channel 3: Motor
            
            self.ser.write(bytes(dmx_data))
            
        except Exception as e:
            print(f"DMX send error: {e}")
    
    def dmx_thread(self):
        """Continuous DMX transmission thread"""
        while self.running:
            self.send_dmx_frame()
            time.sleep(0.023)  # ~44Hz refresh rate
    
    def start(self):
        """Start the DMX controller"""
        self.running = True
        
        # Start DMX transmission thread
        dmx_thread = threading.Thread(target=self.dmx_thread, daemon=True)
        dmx_thread.start()
        
        print("🎪 Mini Kinta Controller Started!")
        print("=" * 50)
        
        # Main control loop
        try:
            while self.running:
                self.show_menu()
                choice = input("\nEnter choice: ").strip().lower()
                self.handle_choice(choice)
                
        except KeyboardInterrupt:
            print("\n⏹️  Stopping...")
        finally:
            self.stop()
    
    def show_menu(self):
        """Show the control menu"""
        print(f"\n🎨 CURRENT STATUS:")
        print(f"   Color: {self.color:3d} ({self.get_color_name(self.color)})")
        print(f"   Strobe: {self.strobe:3d} ({self.get_strobe_name(self.strobe)})")
        print(f"   Motor: {self.motor:3d} ({self.get_motor_name(self.motor)})")
        
        print(f"\n🎛️  CONTROLS:")
        print(f"   COLORS: r=Red  g=Green  b=Blue  w=White  m=Mixed  all=All Colors")
        print(f"   STROBE: s0=Off  s1=Slow  s2=Medium  s3=Fast")
        print(f"   MOTOR:  m0=Stop  m1=Slow  m2=Medium  m3=Fast")
        print(f"   PRESETS: party=Party Mode  off=All Off  demo=Demo Show")
        print(f"   MANUAL: c123=Set Color to 123  st45=Set Strobe to 45  mo67=Set Motor to 67")
        print(f"   OTHER: help=Show Help  q=Quit")
    
    def handle_choice(self, choice):
        """Handle user input"""
        if choice == 'q' or choice == 'quit':
            self.running = False
            
        elif choice == 'help':
            self.show_help()
            
        elif choice == 'off':
            self.color = 0
            self.strobe = 0
            self.motor = 0
            print("🔴 All OFF")
            
        elif choice == 'party':
            self.color = 215  # All colors
            self.strobe = 100 # Medium strobe
            self.motor = 200  # Fast motor
            print("🎉 PARTY MODE!")
            
        elif choice == 'demo':
            self.run_demo()
            
        # Colors
        elif choice == 'r':
            self.color = 20
            print("🔴 Red")
        elif choice == 'g':
            self.color = 35
            print("🟢 Green")
        elif choice == 'b':
            self.color = 50
            print("🔵 Blue")
        elif choice == 'w':
            self.color = 65
            print("⚪ White")
        elif choice == 'm':
            self.color = 125
            print("🌈 Mixed Colors")
        elif choice == 'all':
            self.color = 215
            print("🎨 All Colors")
            
        # Strobe
        elif choice == 's0':
            self.strobe = 0
            print("⭕ Strobe OFF")
        elif choice == 's1':
            self.strobe = 50
            print("💫 Slow Strobe")
        elif choice == 's2':
            self.strobe = 150
            print("⚡ Medium Strobe")
        elif choice == 's3':
            self.strobe = 255
            print("🔥 Fast Strobe")
            
        # Motor
        elif choice == 'm0':
            self.motor = 0
            print("⏹️  Motor STOP")
        elif choice == 'm1':
            self.motor = 80
            print("🐌 Slow Motor")
        elif choice == 'm2':
            self.motor = 150
            print("🚗 Medium Motor")
        elif choice == 'm3':
            self.motor = 255
            print("🏎️  Fast Motor")
            
        # Manual value setting
        elif choice.startswith('c') and choice[1:].isdigit():
            value = int(choice[1:])
            if 0 <= value <= 255:
                self.color = value
                print(f"🎨 Color set to {value}")
            else:
                print("❌ Color must be 0-255")
                
        elif choice.startswith('st') and choice[2:].isdigit():
            value = int(choice[2:])
            if 0 <= value <= 255:
                self.strobe = value
                print(f"⚡ Strobe set to {value}")
            else:
                print("❌ Strobe must be 0-255")
                
        elif choice.startswith('mo') and choice[2:].isdigit():
            value = int(choice[2:])
            if 0 <= value <= 255:
                self.motor = value
                print(f"🔄 Motor set to {value}")
            else:
                print("❌ Motor must be 0-255")
                
        else:
            print("❓ Unknown command. Type 'help' for instructions.")
    
    def run_demo(self):
        """Run a demo light show"""
        print("🎭 Running Demo Show...")
        original_color = self.color
        original_strobe = self.strobe
        original_motor = self.motor
        
        demo_sequence = [
            (20, 0, 100, "Red"),
            (35, 0, 150, "Green"),
            (50, 0, 200, "Blue"),
            (65, 50, 100, "White + Strobe"),
            (125, 100, 255, "Mixed + Effects"),
            (215, 150, 200, "All Colors + Fast Strobe"),
        ]
        
        for color, strobe, motor, desc in demo_sequence:
            print(f"   🎬 {desc}")
            self.color = color
            self.strobe = strobe
            self.motor = motor
            time.sleep(3)
        
        # Restore original settings
        self.color = original_color
        self.strobe = original_strobe
        self.motor = original_motor
        print("   ✅ Demo complete!")
    
    def show_help(self):
        """Show detailed help"""
        print("\n" + "="*60)
        print("🎪 MINI KINTA DMX CONTROLLER HELP")
        print("="*60)
        print("This controller sends continuous DMX data to your Mini Kinta.")
        print("\nCOLOR VALUES (Channel 1):")
        print("  0     = Off")
        print("  1-25  = Red")
        print("  26-40 = Green") 
        print("  41-55 = Blue")
        print("  56-70 = White")
        print("  71-85 = Red+Green")
        print("  86-100= Red+Blue")
        print("  200+  = All colors")
        print("\nSTROBE VALUES (Channel 2):")
        print("  0     = No strobe")
        print("  6-255 = Strobe speed (6=slow, 255=fast)")
        print("\nMOTOR VALUES (Channel 3):")
        print("  0     = Motor stopped")
        print("  1-255 = Motor rotation speed")
        print("\nEXAMPLES:")
        print("  'r' then 'm2' = Red color with medium motor")
        print("  'c85' = Set color to exact value 85")
        print("  'party' = Quick party mode")
        print("="*60)
    
    def get_color_name(self, value):
        if value == 0: return "Off"
        elif value <= 25: return "Red"
        elif value <= 40: return "Green"
        elif value <= 55: return "Blue"
        elif value <= 70: return "White"
        elif value <= 85: return "Red+Green"
        elif value <= 100: return "Red+Blue"
        elif value <= 115: return "Red+White"
        elif value <= 130: return "Green+Blue"
        elif value <= 200: return "Mixed"
        else: return "All Colors"
    
    def get_strobe_name(self, value):
        if value == 0: return "Off"
        elif value < 50: return "Slow"
        elif value < 150: return "Medium"
        else: return "Fast"
    
    def get_motor_name(self, value):
        if value == 0: return "Stopped"
        elif value < 80: return "Slow"
        elif value < 150: return "Medium"
        else: return "Fast"
    
    def stop(self):
        """Stop the controller"""
        self.running = False
        
        # Send all-off command
        print("🔴 Turning off Mini Kinta...")
        self.color = 0
        self.strobe = 0
        self.motor = 0
        
        # Send a few final frames
        for _ in range(10):
            self.send_dmx_frame()
            time.sleep(0.023)
        
        self.ser.close()
        print("✅ Mini Kinta Controller stopped.")

def main():
    print("🎪 Mini Kinta DMX Controller")
    print("============================")
    
    try:
        controller = MiniKintaController()
        controller.start()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()