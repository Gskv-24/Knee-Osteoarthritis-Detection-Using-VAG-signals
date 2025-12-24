// ===============================
// ESP32 Data Acquisition Code
// Knee Joint Health Analyzer
// ===============================

// ADC pin connected to MAX9814 microphone output
#define MAX9814_PIN 34   // GPIO34 (ADC1_CH6)

// ADC pin connected to Piezoelectric Disc
#define PIEZO_PIN   35   // GPIO35 (ADC1_CH7)

void setup() {
  Serial.begin(115200);     // Initialize serial communication
}

void loop() {
  // Read analog values from sensors
  int mic_value   = analogRead(MAX9814_PIN);   // Knee joint sound
  int piezo_value = analogRead(PIEZO_PIN);     // Knee joint vibration

  // Send formatted data over Serial
  Serial.print("Mic: ");
  Serial.print(mic_value);
  Serial.print("\tPiezo: ");
  Serial.println(piezo_value);

  delay(10);   // Sampling interval (~100 Hz)
}
