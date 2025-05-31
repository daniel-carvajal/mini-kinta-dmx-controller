#!/usr/bin/env python3
"""
DMX Debug Tool - Test communication with USB-DMX interface
"""

import serial
import time

PORT = "/dev/cu.usbserial-AQ02YN7D"

def test_serial_connection():
    """Test basic serial connection"""
    try:
        print("Testing serial connection...")
        ser = serial.Serial(
            port=PORT,
            baudrate=250000,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=2,
            timeout=1
        )
        print(f"✓ Connected to {PORT}")
        print(f"  Baudrate: {ser.baudrate}")
        print(f"  Bytesize: {ser.bytesize}")
        print(f"  Parity: {ser.parity}")
        print(f"  Stopbits: {ser.stopbits}")
        
        # Test writing some data
        test_data = b"Hello"
        ser.write(test_data)
        print(f"✓ Sent test data: {test_data}")
        
        ser.close()
        return True
        
    except Exception as e:
        print(f"✗ Serial connection failed: {e}")
        return False

def test_dmx_with_break():
    """Test DMX with proper break and MAB"""
    try:
        print("\nTesting DMX with proper timing...")
        ser = serial.Serial(
            port=PORT,
            baudrate=250000,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=2,
            timeout=1
        )
        
        for test_num in range(3):
            print(f"DMX Test {test_num + 1}...")
            
            # Send BREAK (low for 100+ microseconds)
            ser.break_condition = True
            time.sleep(0.0002)  # 200 microseconds
            ser.break_condition = False
            
            # Mark After Break (high for 12+ microseconds)
            time.sleep(0.00002)  # 20 microseconds
            
            # Create DMX packet
            dmx_data = [0] * 513  # Start code + 512 channels
            dmx_data[0] = 0       # Start code
            dmx_data[1] = 255 if test_num == 0 else 0    # Channel 1 - full red
            dmx_data[2] = 255 if test_num == 1 else 0    # Channel 2 - strobe
            dmx_data[3] = 255 if test_num == 2 else 127  # Channel 3 - motor
            
            # Send packet
            packet = bytes(dmx_data)
            ser.write(packet)
            
            print(f"  Sent: Ch1={dmx_data[1]}, Ch2={dmx_data[2]}, Ch3={dmx_data[3]}")
            time.sleep(2)
        
        # Turn everything off
        print("Turning off...")
        ser.break_condition = True
        time.sleep(0.0002)
        ser.break_condition = False
        time.sleep(0.00002)
        
        dmx_data = [0] * 513
        ser.write(bytes(dmx_data))
        
        ser.close()
        print("✓ DMX test complete")
        
    except Exception as e:
        print(f"✗ DMX test failed: {e}")

def test_different_baudrates():
    """Test different baud rates"""
    baudrates = [9600, 38400, 57600, 115200, 250000]
    
    print("\nTesting different baud rates...")
    for baud in baudrates:
        try:
            ser = serial.Serial(
                port=PORT,
                baudrate=baud,
                timeout=1
            )
            ser.write(b"test")
            ser.close()
            print(f"✓ {baud} baud - OK")
        except Exception as e:
            print(f"✗ {baud} baud - Failed: {e}")

def test_continuous_dmx():
    """Send continuous DMX stream"""
    try:
        print("\nStarting continuous DMX stream...")
        print("Press Ctrl+C to stop")
        
        ser = serial.Serial(
            port=PORT,
            baudrate=250000,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=2,
            timeout=1
        )
        
        frame_count = 0
        while True:
            # DMX Break
            ser.break_condition = True
            time.sleep(0.0001)  # 100 microseconds
            ser.break_condition = False
            time.sleep(0.00001)  # 10 microseconds
            
            # Create packet
            dmx_data = [0] * 513
            
            # Cycle through colors
            color_cycle = frame_count % 300
            if color_cycle < 100:
                dmx_data[1] = 100  # Red
            elif color_cycle < 200:
                dmx_data[1] = 150  # Green-ish
            else:
                dmx_data[1] = 200  # Blue-ish
            
            dmx_data[3] = 100  # Motor speed
            
            ser.write(bytes(dmx_data))
            
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Sent {frame_count} DMX frames")
            
            time.sleep(0.02)  # ~50Hz refresh rate
            
    except KeyboardInterrupt:
        print("\nStopping continuous DMX...")
        # Send all zeros
        dmx_data = [0] * 513
        ser.write(bytes(dmx_data))
        ser.close()
    except Exception as e:
        print(f"✗ Continuous DMX failed: {e}")

def main():
    print("DMX Debug Tool")
    print("=" * 40)
    
    # Test 1: Basic serial connection
    if not test_serial_connection():
        return
    
    # Test 2: Different baud rates
    test_different_baudrates()
    
    # Test 3: DMX with proper timing
    test_dmx_with_break()
    
    # Test 4: Ask user if they want continuous stream
    response = input("\nRun continuous DMX stream test? (y/n): ")
    if response.lower().startswith('y'):
        test_continuous_dmx()

if __name__ == "__main__":
    main()