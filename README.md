# Mini Kinta DMX Controller

Control your Chauvet Mini Kinta LED light via USB-DMX interface from your Mac.

## 🎯 Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install pyserial
   ```

2. **Connect hardware:**
   - USB-DMX interface → Mac USB port
   - DMX cable → USB-DMX OUT to Mini Kinta DMX IN
   - Power on Mini Kinta, set to DMX mode (display shows "A001")

3. **Run the controller:**
   ```bash
   python3 controller.py
   ```
   The scripts find the USB-DMX adapter on their own. To pick a port yourself, see [Choosing the serial port](#-choosing-the-serial-port).

## 🎛️ Controller Usage

### Quick Commands
- **Colors:** `r`=Red, `g`=Green, `b`=Blue, `w`=White, `all`=All Colors
- **Strobe:** `s0`=Off, `s1`=Slow, `s2`=Medium, `s3`=Fast  
- **Motor:** `m0`=Stop, `m1`=Slow, `m2`=Medium, `m3`=Fast
- **Presets:** `party`=Party Mode, `off`=All Off, `demo`=Demo Show

### Manual Control
- `c123` = Set color to value 123 (0-255)
- `st45` = Set strobe to value 45 (0-255)
- `mo67` = Set motor to value 67 (0-255)

### Example Session
```
Enter choice: r      # Red color
Enter choice: m2     # Medium motor speed
Enter choice: s1     # Add slow strobe  
Enter choice: party  # Switch to party mode
Enter choice: off    # Turn everything off
Enter choice: q      # Quit
```

## 📁 Project Files

### Core Files
- **`controller.py`** - Main interactive controller (use this!)
- **`test_connection.py`** - Test DMX connection and verify setup
- **`troubleshoot.py`** - Debug tools for connection issues
- **`dmx_port.py`** - Picks the serial port, shared by the three scripts above

### Documentation
- **`README.md`** - This file
- **`requirements.txt`** - Python dependencies

## 🔌 Choosing the serial port

Every script (`controller.py`, `test_connection.py`, `troubleshoot.py`) picks its port in this order:

1. `--port`, e.g. `python3 controller.py --port /dev/cu.usbserial-4`
2. The `MINIKINTA_DMX_PORT` environment variable, e.g. `MINIKINTA_DMX_PORT=/dev/cu.usbserial-4 python3 controller.py`
3. Auto-detect: if exactly one FTDI adapter is connected, that one is used
4. Fallback: `/dev/cu.usbserial-AQ02YN7D`, used when no FTDI adapter is detected

If auto-detect finds more than one FTDI port, the script stops and lists them, so pick one with option 1 or 2. Port names such as `usbserial-4` can change when the adapter is replugged, so don't hardcode them.

To list connected ports:
```bash
python3 -m serial.tools.list_ports -v
```

## 🔧 Troubleshooting

### Two ports for one adapter (script runs, light does nothing)

If `list_ports` shows two ports with the same serial number (for example `/dev/cu.usbserial-AQ02YN7D` and `/dev/cu.usbserial-4`), two drivers are attached to the one adapter. Only one of them drives the DMX line. On one of our Macs, a third-party FTDI driver extension took the `usbserial-AQ02YN7D` name. Sending to it raised no errors, but the light never reacted. Apple's built-in driver had been moved to `usbserial-4`, and that port worked.

Check which driver owns which port:
```bash
ioreg -r -n AppleUSBFTDI -l -w 0 | grep IOCalloutDevice
ioreg -p IOService -w0 | grep -iE "FTDI|FT232|IOUserSerial"
```

Fix it either way:
- Point the scripts at Apple's port with `--port` or `MINIKINTA_DMX_PORT`.
- Or turn off the extra driver in System Settings > General > Login Items & Extensions > Driver Extensions (it's listed under its app's name, such as an FTDI USB entry), then unplug and replug the adapter. Apple's driver then owns the adapter alone and auto-detect works.

### No Response from Mini Kinta?

1. **Test connection:**
   ```bash
   python3 test_connection.py
   ```

2. **Check Mini Kinta settings:**
   - Power ON
   - Display shows "A001" (DMX address 1)
   - In DMX mode (not Auto/Sound mode)

3. **Check cables:**
   - USB-DMX interface detected: `/dev/cu.usbserial-*`
   - DMX cable: 3-pin XLR, properly wired
   - Connection: USB-DMX OUT → Mini Kinta IN

4. **Run debug tools:**
   ```bash
   python3 troubleshoot.py
   ```

### Common Issues
- **Wrong cable:** Audio XLR vs DMX XLR (different wiring)
- **Swapped pins:** Pins 2&3 reversed in cheap cables
- **Wrong mode:** Mini Kinta in Auto mode instead of DMX
- **Address mismatch:** Mini Kinta not set to address 001

## 📖 DMX Channel Reference

The Mini Kinta uses 3 DMX channels:

| Channel | Function | Values | Description |
|---------|----------|--------|-------------|
| 1 | Color | 0-255 | 0=Off, 20=Red, 35=Green, 50=Blue, 65=White, 215=All |
| 2 | Strobe | 0-255 | 0=Off, 6-255=Strobe speed (slow to fast) |
| 3 | Motor | 0-255 | 0=Stop, 1-255=Rotation speed |

## 🛠️ Hardware Requirements

- **Mini Kinta:** Chauvet Mini Kinta LED effect light
- **USB-DMX Interface:** FT232R-based USB to DMX converter
- **DMX Cable:** 3-pin XLR male to female
- **Computer:** Mac with Python 3.x

## 🔌 Technical Details

- **DMX Protocol:** Standard DMX512 at 250,000 baud
- **Refresh Rate:** ~44Hz continuous transmission
- **USB Interface:** FTDI FT232R chip
- **Device Port:** auto-detected; defaults to `/dev/cu.usbserial-AQ02YN7D` (see [Choosing the serial port](#-choosing-the-serial-port))

## 🎪 Features

- ✅ Real-time DMX control
- ✅ Continuous background transmission
- ✅ Interactive menu interface
- ✅ Preset modes (Party, Demo, Off)
- ✅ Manual value control (0-255)
- ✅ Connection testing tools
- ✅ Cross-platform compatible

## 🚀 Next Steps

Want to add more DMX fixtures? The controller can easily be extended:

1. **Multiple fixtures:** Modify `dmx_address` parameter
2. **More channels:** Add channels 4+ for additional features  
3. **Light shows:** Create sequences in the demo function
4. **Web interface:** Build a web-based controller
5. **MIDI control:** Connect MIDI controllers for live performance

## 📝 License

This project is for educational and personal use. Enjoy your light show! 🎉