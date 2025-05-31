#!/usr/bin/env python3
"""
Mini Kinta specific DMX test based on manual specifications
"""

import serial
import time

PORT = "/dev/cu.usbserial-AQ02YN7D"

def mini_kinta_dmx_test():
    """Test with Mini Kinta's exact DMX specifications"""
    
    print("Mini Kinta DMX Test")
    print("===================")
    print("Make sure:")
    print("1. Mini Kinta is powered ON")
    print("2. Display shows 'A001' (DMX address 1)")
    print("3. DMX cable connected: USB-DMX OUT -> Mini Kinta IN")
    print("4. Press Enter to start test...")
    input()
    
    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=250000,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=2,
            timeout=1
        )
        
        print("\nSending DMX data...")
        
        # According to Mini Kinta manual, it has 3 DMX channels:
        # Channel 1: Color selection
        # Channel 2: Strobe
        # Channel 3: Motor rotation
        
        test_sequences = [
            # (description, ch1_color, ch2_strobe, ch3_motor)
            ("Red color only", 20, 0, 0),
            ("Red with slow motor", 20, 0, 100),
            ("Green color", 35, 0, 100),
            ("Blue color", 50, 0, 100),
            ("White color", 65, 0, 100),
            ("Red/Green mix", 80, 0, 100),
            ("All colors fast motor", 215, 0, 200),
            ("All colors with strobe", 215, 100, 150),
            ("Turn off", 0, 0, 0),
        ]
        
        for desc, color, strobe, motor in test_sequences:
            print(f"\nTest: {desc}")
            print(f"  Channel 1 (Color): {color}")
            print(f"  Channel 2 (Strobe): {strobe}")
            print(f"  Channel 3 (Motor): {motor}")
            
            # Send continuous DMX for 5 seconds
            start_time = time.time()
            frame_count = 0
            
            while time.time() - start_time < 5:
                # DMX Break (minimum 88 microseconds)
                ser.break_condition = True
                time.sleep(0.0001)  # 100 microseconds
                ser.break_condition = False
                
                # Mark After Break (minimum 8 microseconds)
                time.sleep(0.00001)  # 10 microseconds
                
                # DMX packet: start code + 512 channels
                dmx_data = [0] * 513
                dmx_data[0] = 0      # Start code
                dmx_data[1] = color  # Channel 1
                dmx_data[2] = strobe # Channel 2
                dmx_data[3] = motor  # Channel 3
                
                ser.write(bytes(dmx_data))
                frame_count += 1
                
                # Standard DMX refresh rate (44Hz)
                time.sleep(0.023)
            
            print(f"  Sent {frame_count} DMX frames")
            
            # Ask user for feedback
            response = input("  Did you see any change? (y/n/quit): ")
            if response.lower().startswith('q'):
                break
            elif response.lower().startswith('y'):
                print("  ✓ SUCCESS! Mini Kinta responded")
            else:
                print("  ✗ No response")
        
        # Final cleanup
        print("\nSending final OFF command...")
        for _ in range(10):
            ser.break_condition = True
            time.sleep(0.0001)
            ser.break_condition = False
            time.sleep(0.00001)
            
            dmx_data = [0] * 513
            ser.write(bytes(dmx_data))
            time.sleep(0.023)
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")

def check_dmx_cable():
    """Guide for checking DMX cable"""
    print("\nDMX Cable Check")
    print("===============")
    print("Your DMX cable should be wired as:")
    print("Pin 1: Shield/Ground")
    print("Pin 2: Data- (Cold)")
    print("Pin 3: Data+ (Hot)")
    print()
    print("Common problems:")
    print("- Pins 2 and 3 swapped (very common in cheap cables)")
    print("- Audio XLR cable used instead of DMX cable")
    print("- Cable wired for different DMX polarity")
    print()
    print("Try:")
    print("1. Different DMX cable")
    print("2. DMX cable with opposite polarity")
    print("3. Test cable with other DMX devices if available")

def test_extreme_values():
    """Test with extreme values to see any response"""
    print("\nTesting with extreme values...")
    
    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=250000,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=2,
            timeout=1
        )
        
        # Send maximum values for 10 seconds
        print("Sending MAXIMUM values (all channels at 255)...")
        print("This should produce obvious effects if working...")
        
        start_time = time.time()
        while time.time() - start_time < 10:
            ser.break_condition = True
            time.sleep(0.0001)
            ser.break_condition = False
            time.sleep(0.00001)
            
            dmx_data = [0] + [255] * 512  # All channels max
            ser.write(bytes(dmx_data))
            time.sleep(0.023)
        
        # Turn everything off
        print("Turning everything OFF...")
        for _ in range(10):
            ser.break_condition = True
            time.sleep(0.0001)
            ser.break_condition = False
            time.sleep(0.00001)
            
            dmx_data = [0] * 513
            ser.write(bytes(dmx_data))
            time.sleep(0.023)
        
        ser.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    mini_kinta_dmx_test()
    check_dmx_cable()
    
    response = input("\nTry extreme values test? (y/n): ")
    if response.lower().startswith('y'):
        test_extreme_values()