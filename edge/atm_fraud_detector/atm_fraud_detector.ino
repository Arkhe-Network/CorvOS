// Substrato 200: ATM Fraud Detector (TinyML para ESP32)
// Detecta anomalias físicas e lógicas em ATMs usando um modelo reduzido.

#include <Arduino.h>

// Mock de variáveis do modelo TinyML
const float THRESHOLD = 0.85;

void setup() {
  Serial.begin(115200);
  Serial.println("🤖 Inicializando ATM Fraud Detector (TinyML)...");
  // Inicialização de sensores e carregamento do modelo TensorFlow Lite
  delay(1000);
  Serial.println("✅ Modelo carregado e pronto.");
}

void loop() {
  // Simula leitura de sensores do ATM (teclado, câmera, leitor de cartão)
  float sensor_readings[3] = {random(0, 100) / 100.0, random(0, 100) / 100.0, random(0, 100) / 100.0};

  // Simula inferência do modelo
  float anomaly_score = (sensor_readings[0] + sensor_readings[1] + sensor_readings[2]) / 3.0;

  if (anomaly_score > THRESHOLD) {
    Serial.print("⚠️ ALERTA DE FRAUDE DETECTADA NO ATM! Score: ");
    Serial.println(anomaly_score);
    // Aqui seria acionado o bloqueio do ATM e enviado alerta via MQTT/CoAP para a nuvem
  } else {
    // Operação normal
    // Serial.println("✅ Operação normal.");
  }

  delay(5000); // Aguarda antes da próxima inferência
}
