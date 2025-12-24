import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch
from scipy.fft import fft, fftfreq


class KneeOADetector:
    def __init__(self, fs=5000):
        """
        fs : Sampling frequency (Hz)
        """
        self.fs = fs

        # Bandpass range based on VAG literature
        self.bandpass_range = (50, 600)

        # Powerline interference
        self.notch_freq = 50

        # Thresholds derived from research papers
        self.thresholds = {
            'piezo': {
                'healthy': (30, 80),
                'mild': (80, 120),
                'severe': (120, float('inf'))
            },
            'mic': {
                'healthy': (100, 350),
                'mild': (350, 450),
                'severe': (450, float('inf'))
            }
        }

    # ---------------------------------------------------
    # DATA LOADING
    # ---------------------------------------------------
    def load_data(self, file_path):
        """
        Supports:
        1) Lines like: Mic: 123 Piezo: 45
        2) CSV lines: mic,piezo
        """
        mic_data = []
        piezo_data = []

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    # Format: Mic: xxx Piezo: yyy
                    if "Mic" in line and "Piezo" in line:
                        parts = line.replace(':', ' ').split()
                        try:
                            mic_idx = parts.index("Mic") + 1
                            piezo_idx = parts.index("Piezo") + 1
                            mic_data.append(float(parts[mic_idx]))
                            piezo_data.append(float(parts[piezo_idx]))
                        except (ValueError, IndexError):
                            continue

                    # CSV format
                    elif "," in line:
                        try:
                            mic, piezo = map(float, line.split(","))
                            mic_data.append(mic)
                            piezo_data.append(piezo)
                        except ValueError:
                            continue

            return np.array(mic_data), np.array(piezo_data)

        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")

    # ---------------------------------------------------
    # SIGNAL PREPROCESSING
    # ---------------------------------------------------
    def preprocess(self, data, sensor_type):
        if len(data) < 10:
            return data

        # Bandpass filter
        b, a = butter(
            4,
            [self.bandpass_range[0] / (self.fs / 2),
             self.bandpass_range[1] / (self.fs / 2)],
            btype='band'
        )
        filtered = filtfilt(b, a, data)

        # 50 Hz notch
        b_notch, a_notch = iirnotch(self.notch_freq, 30, self.fs)
        filtered = filtfilt(b_notch, a_notch, filtered)

        # Remove harmonic (piezo sensitive)
        if sensor_type == 'piezo':
            b_h, a_h = iirnotch(100, 30, self.fs)
            filtered = filtfilt(b_h, a_h, filtered)

        return filtered

    # ---------------------------------------------------
    # FREQUENCY ANALYSIS
    # ---------------------------------------------------
    def analyze_signal(self, data):
        n = len(data)
        if n < 10:
            return None, None, None, None

        window = np.hanning(n)
        windowed = data * window

        fft_vals = np.abs(fft(windowed))
        fft_vals = fft_vals[:n // 2]
        freqs = fftfreq(n, 1 / self.fs)[:n // 2]

        # Normalize FFT for visualization
        fft_vals = fft_vals / np.max(fft_vals)

        # Dominant frequency (ignore DC)
        dominant_idx = np.argmax(fft_vals[10:]) + 10
        dominant_freq = freqs[dominant_idx]

        # Energy ratio (OA marker)
        low_band = (freqs >= 50) & (freqs < 150)
        high_band = (freqs >= 300) & (freqs < 600)

        energy_ratio = np.sum(fft_vals[high_band]) / (np.sum(fft_vals[low_band]) + 1e-9)

        return dominant_freq, freqs, fft_vals, energy_ratio

    # ---------------------------------------------------
    # SEVERITY LOGIC
    # ---------------------------------------------------
    def get_severity_level(self, freq, sensor):
        if freq >= self.thresholds[sensor]['severe'][0]:
            return 2
        elif freq >= self.thresholds[sensor]['mild'][0]:
            return 1
        else:
            return 0

    def diagnose(self, mic_freq, piezo_freq, mic_energy, piezo_energy):
        mic_level = self.get_severity_level(mic_freq, 'mic')
        piezo_level = self.get_severity_level(piezo_freq, 'piezo')

        if mic_level >= 1 and piezo_level == 0:
            diagnosis = "Early Osteoarthritis (KL Grade 1–2)"
            notes = [
                "Mic shows elevated frequency → cartilage roughening.",
                "Piezo normal → joint mechanics preserved.",
                "MRI suggested for confirmation."
            ]

        elif piezo_level >= 1 and mic_level == 0:
            diagnosis = "Subchondral Bone Changes (Pre-OA)"
            notes = [
                "Piezo frequency elevated → bone remodeling.",
                "Mic normal → cartilage intact.",
                "X-ray recommended."
            ]

        elif mic_level == piezo_level:
            if mic_level == 2:
                diagnosis = "Severe Osteoarthritis (KL Grade 3–4)"
                notes = ["Both sensors show pathological vibration."]
            elif mic_level == 1:
                diagnosis = "Moderate Osteoarthritis (KL Grade 2–3)"
                notes = ["Degeneration in progress."]
            else:
                diagnosis = "Healthy Knee (KL Grade 0)"
                notes = ["No abnormal vibro-acoustic activity detected."]

        else:
            diagnosis = "Inconclusive"
            notes = [
                "Sensor disagreement detected.",
                "Repeat test or use imaging methods."
            ]

        notes.extend([
            "\n--- Research Basis ---",
            "Tamura et al., 2013 – Mic >400 Hz correlates with KL3–4",
            "Chandran et al., 2021 – Piezo >120 Hz indicates sclerosis",
            "OARSI – Dual-sensor VAG improves OA detection"
        ])

        return diagnosis, notes

    # ---------------------------------------------------
    # VISUALIZATION
    # ---------------------------------------------------
    def plot_analysis(self, mic_raw, mic_filt, piezo_raw, piezo_filt,
                      mic_freqs, mic_fft, piezo_freqs, piezo_fft):

        time = np.arange(len(mic_raw)) / self.fs
        plt.figure(figsize=(14, 10))

        plt.subplot(2, 2, 1)
        plt.plot(time, mic_raw, alpha=0.4, label="Raw")
        plt.plot(time, mic_filt, label="Filtered")
        plt.title("Mic Signal – Time Domain")
        plt.legend()
        plt.grid()

        plt.subplot(2, 2, 2)
        plt.plot(time, piezo_raw, alpha=0.4, label="Raw")
        plt.plot(time, piezo_filt, label="Filtered")
        plt.title("Piezo Signal – Time Domain")
        plt.legend()
        plt.grid()

        plt.subplot(2, 2, 3)
        plt.plot(mic_freqs, mic_fft)
        plt.title("Mic FFT")
        plt.xlabel("Frequency (Hz)")
        plt.grid()

        plt.subplot(2, 2, 4)
        plt.plot(piezo_freqs, piezo_fft)
        plt.title("Piezo FFT")
        plt.xlabel("Frequency (Hz)")
        plt.grid()

        plt.tight_layout()
        plt.show()

    # ---------------------------------------------------
    # ABNORMALITY CHECK
    # ---------------------------------------------------
    def is_abnormal(self, signal):
        std = np.std(signal)
        return np.sum(np.abs(signal) > 3 * std) > 10


# =====================================================
# MAIN EXECUTION
# =====================================================
if __name__ == "__main__":

    file_path = "Jase_50_percent.txt"   # 🔁 Replace with your data file

    detector = KneeOADetector(fs=5000)

    try:
        mic_raw, piezo_raw = detector.load_data(file_path)

        mic_clean = detector.preprocess(mic_raw, 'mic')
        piezo_clean = detector.preprocess(piezo_raw, 'piezo')

        mic_freq, mic_freqs, mic_fft, mic_energy = detector.analyze_signal(mic_clean)
        piezo_freq, piezo_freqs, piezo_fft, piezo_energy = detector.analyze_signal(piezo_clean)

        detector.plot_analysis(
            mic_raw, mic_clean,
            piezo_raw, piezo_clean,
            mic_freqs, mic_fft,
            piezo_freqs, piezo_fft
        )

        diagnosis, notes = detector.diagnose(
            mic_freq, piezo_freq,
            mic_energy, piezo_energy
        )

        print("\n========== DIAGNOSIS ==========")
        print(f"Mic Dominant Frequency   : {mic_freq:.2f} Hz")
        print(f"Piezo Dominant Frequency : {piezo_freq:.2f} Hz")
        print(f"\n{diagnosis}\n")

        for n in notes:
            print(n)

    except Exception as e:
        print("Error:", e)
