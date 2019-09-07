#include <Arduino.h>
#include <NeoPixelBus.h>
#include <math.h>

enum class cmd_t {
  CMD_RESET = 'r',
};

const uint8_t STRIP_COUNT = 50;
const uint16_t LED_COUNT = STRIP_COUNT * 2;  // 60LED/m
const uint16_t LED_PIN = 2;
const float LED_BRIGHTNESS = 0.25;

const RgbColor COLOR_OFF(0, 0, 0);

NeoPixelBus<NeoRgbFeature, Neo800KbpsMethod> strip(LED_COUNT, LED_PIN);

const double DECAY_PERIOD = 0.01;  // brightness lost per ms

uint8_t serial_buf[100];
uint8_t serial_buf_len = 0;

void setup() {
  strip.Begin();
  Serial.begin(1000000);
}

void clearLeds() {
  strip.ClearTo(COLOR_OFF);
  strip.Show();
}

const double HUE_SHIFT_PER_LED = 1.0 / LED_COUNT;
const double HUE_SHIFT_PER_MS = 0.0005;

void updateLeds() {
  double now = millis();
  for (uint8_t i = 0; i < LED_COUNT; i++) {
    double hue = 0 + i * HUE_SHIFT_PER_LED + HUE_SHIFT_PER_MS * now;
    hue = fabs(fmod(hue, 1.0));
    HslColor color(hue, 1.0, LED_BRIGHTNESS);
    strip.SetPixelColor(i, color);
  }
  strip.Show();
}

void onSerialReceive() {
  switch (static_cast<cmd_t>(serial_buf[0])) {
    case cmd_t::CMD_RESET:
      clearLeds();
      break;
    default:
      Serial.print("Unknown command:");
      for (uint8_t i = 0; i < serial_buf_len; i++) {
        Serial.print(serial_buf[i]);
      }
      Serial.println();
      break;
  }
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    serial_buf[serial_buf_len++] = c;
    if (c == '\n' && serial_buf_len >= 2) {
      onSerialReceive();
      serial_buf_len = 0;
    }
  }
  updateLeds();
  // strip.SetPixelColor(0, RgbColor(0xFF, 0, 0));
  // strip.SetPixelColor(1, RgbColor(0, 0xFF, 0));
  // strip.SetPixelColor(2, RgbColor(0, 0, 0xFF));
  // strip.Show();
}
