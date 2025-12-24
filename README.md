# Knee-Osteoarthritis-Detection-Using-VAG-signals

Knee Joint Health Analyzer using Vibroarthrography (VAG)
📌 Overview

This project presents a non-invasive, low-cost Knee Joint Health Analyzer designed to assist in the early detection of Knee Osteoarthritis (OA) using Vibroarthrography (VAG) signals.

The system captures joint vibrations and acoustic emissions during knee movement using a piezoelectric disc and a MAX9814 microphone amplifier, processes the signals using an ESP32, and analyzes them using filtering and FFT-based frequency-domain techniques.

This approach provides an affordable alternative to traditional imaging methods such as X-ray and MRI, especially for early-stage screening and continuous monitoring.

🎯 Objectives

Capture knee joint vibration and sound signals during flexion–extension

Analyze frequency-domain characteristics of healthy vs OA-affected knees

Identify dominant frequency shifts associated with cartilage degradation

Build a compact, portable, and cost-effective diagnostic prototype

🧠 Principle: Vibroarthrography (VAG)

Healthy knee joints produce low-amplitude, low-frequency vibrations

Osteoarthritic knees exhibit irregular, higher-frequency vibrations

These differences are captured externally using surface-mounted sensors

FFT analysis reveals distinct dominant frequency patterns correlated with OA severity

| Component             | Purpose                                     |
| --------------------- | ------------------------------------------- |
| ESP32 Dev Board       | Data acquisition, ADC, serial communication |
| MAX9814 Mic Amplifier | Captures knee joint acoustic emissions      |
| Piezoelectric Disc    | Captures mechanical joint vibrations        |
| Knee Strap / Mount    | Sensor placement near patella               |
| USB / 3.3V Supply     | Power source                                |

🔌 Hardware Connections
| MAX9814 Pin | ESP32 Pin | Description         |
| ----------- | --------- | ------------------- |
| VDD         | 3.3V      | Power supply        |
| GND         | GND       | Common ground       |
| OUT         | GPIO34    | Analog audio signal |
| GAIN        | Floating  | Sets ~60 dB gain    |
| AR          | Floating  | Default AGC release |


⚠️ GPIO34 & GPIO35 are input-only ADC pins, ideal for analog biomedical signals.

🧩 System Architecture

1.Knee motion generates vibrations and sounds

2.Piezo disc + microphone convert mechanical energy → electrical signals

3.ESP32 ADC samples signals in real time

4.Data streamed to PC via Serial

5.Python (Spyder) performs:

  Bandpass filtering

  Notch filtering (power-line noise)

  FFT analysis

  Dominant frequency extraction

6.Frequency thresholds used to infer OA severity

💻 Software Stack

Arduino IDE – ESP32 data acquisition

Python (Spyder) – Signal processing & visualization

Libraries Used

  NumPy

  SciPy

  Matplotlib

📈 Signal Processing Flow

Raw signal acquisition

Bandpass filtering (50–600 Hz)

50 Hz notch filtering

FFT computation

Dominant frequency identification

Frequency comparison with diagnostic thresholds


🚀 Applications

Early screening of knee osteoarthritis

Wearable joint health monitoring

Sports injury assessment

Post-surgery rehabilitation tracking

Biomedical signal processing research

🔮 Future Improvements

Machine learning–based OA classification

Wireless data transmission

Wearable enclosure design

Multi-sensor fusion (IMU + pressure)

Clinical-scale dataset validation



📜 Disclaimer

This project is intended for academic and research purposes only and is not a certified medical diagnostic device.
