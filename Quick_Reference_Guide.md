# Quick Reference Guide for Real Time Radar

This quick reference guide provides essential commands, parameters, and troubleshooting tips for the Real Time Radar system.

## Essential Commands

### Starting the Applications

```bash
# Launch the main launcher application
python launcher.py

# Launch Range Profile application directly
python "Range Profile/rp_main.py"

# Launch Range Doppler application directly
python "Range Doppler/rd_main.py"

# Launch Range Angle application directly
python "Range Angle/ra_main.py"
```

### Python Environment

```bash
# Create virtual environment
python -m venv radar_env

# Activate virtual environment (Windows)
radar_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# List installed packages
pip list
```

### Network Testing

```bash
# Test connection to DCA1000 EVM
ping 192.168.33.180

# Check UDP ports (Windows)
netstat -a -p UDP | findstr "4096 4098"
```

## Key Configuration Parameters

### Radar Configuration Quick Reference

| Parameter | Description | Example Value | Impact |
|-----------|-------------|---------------|--------|
| startFreq | Starting frequency (GHz) | 77 | Center frequency of radar operation |
| freqSlopeConst | Frequency slope (MHz/μs) | 70 | Affects bandwidth and range resolution |
| numAdcSamples | ADC samples per chirp | 256 | Affects maximum range |
| numChirpsPerFrame | Chirps per frame | 16 | Affects velocity resolution |
| framePeriodicity | Frame period (ms) | 100 | Controls update rate |
| txMask | TX antenna mask | 15 (all 4 TX) | Controls which TX antennas are used |
| rxMask | RX antenna mask | 7 (first 3 RX) | Controls which RX antennas are used |

### Common Configuration Scenarios

#### Long Range Configuration
```
profileCfg 0 77 267 7 57.14 0 0 40 1 512 5209 0 0 30
frameCfg 0 2 16 0 100 1 0
```
- Lower frequency slope (40 MHz/μs)
- More ADC samples (512)
- Impact: Longer maximum range, reduced range resolution

#### High Resolution Configuration
```
profileCfg 0 77 267 7 57.14 0 0 100 1 256 5209 0 0 30
frameCfg 0 2 16 0 100 1 0
```
- Higher frequency slope (100 MHz/μs)
- Impact: Better range resolution, reduced maximum range

#### Fast Update Rate Configuration
```
profileCfg 0 77 267 7 57.14 0 0 70 1 256 5209 0 0 30
frameCfg 0 2 16 0 50 1 0
```
- Reduced frame periodicity (50 ms)
- Impact: Faster update rate, potentially increased CPU load

## Processing Parameters

### Window Functions

| Window Type | Characteristics | Best For |
|-------------|-----------------|----------|
| Blackman-Harris | Excellent sidelobe suppression, wider mainlobe | Scenarios with large dynamic range between targets |
| Hamming | Good balance between mainlobe width and sidelobe level | General purpose |
| Hanning | Similar to Hamming but with different coefficients | General purpose |
| Rectangular | Narrowest mainlobe, highest sidelobes | High resolution between targets of similar RCS |

### Range Padding

| Padding Factor | Effect |
|----------------|--------|
| 1x | No padding, fastest processing |
| 2x | Doubled range bins, smoother display |
| 4x | 4x range bins, much smoother display, slower processing |
| 8x | 8x range bins, very smooth display, slowest processing |

### CFAR Detection

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| Guard Cells | Cells around target to exclude from background | 4-8 |
| Training Cells | Cells used to estimate background | 8-16 |
| False Alarm Rate | Probability of false detection | 0.001-0.01 |

## Troubleshooting Checklist

### No Data Received

1. ✓ Check Ethernet connection and IP address (192.168.33.30)
2. ✓ Verify DCA1000 EVM is powered on
3. ✓ Confirm firewall allows UDP ports 4096 and 4098
4. ✓ Ensure radar is properly configured and started
5. ✓ Try restarting both the radar and the application

### COM Port Issues

1. ✓ Verify COM port in Device Manager
2. ✓ Check USB connection to XWR1843 EVM
3. ✓ Ensure FTDI drivers are installed
4. ✓ Close any other applications that might be using the COM port

### Application Performance Issues

1. ✓ Reduce range padding factor
2. ✓ Close other CPU-intensive applications
3. ✓ Increase frame periodicity (slower update rate)
4. ✓ Reduce number of ADC samples or chirps per frame

## Performance Optimization Tips

1. **Processing Speed**:
   - Use lower range padding factors
   - Select simpler window functions (e.g., Rectangular)
   - Close other applications to free up CPU resources

2. **Detection Sensitivity**:
   - Adjust CFAR parameters (lower false alarm rate for fewer false detections)
   - Enable static clutter removal for better detection of moving targets
   - Use Blackman-Harris window for better dynamic range

3. **Range Resolution**:
   - Increase bandwidth (higher frequency slope)
   - Use higher range padding factors for interpolated display

4. **Velocity Resolution**:
   - Increase number of chirps per frame
   - Ensure longer frame duration

## Common Error Messages

| Error Message | Possible Cause | Solution |
|---------------|----------------|----------|
| "Failed to open COM port" | COM port in use or incorrect | Check Device Manager, try different COM port |
| "Socket error" | Network configuration issue | Verify IP address and firewall settings |
| "Configuration error" | Invalid radar configuration | Check configuration file parameters |
| "Data capture error" | DCA1000 not receiving data | Check physical connections and power |
| "Processing error" | Invalid processing parameters | Reset to default parameters |
