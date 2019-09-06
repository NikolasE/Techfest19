#include <Arduino.h>
#include <NeoPixelBus.h>

const uint16_t LED_COUNT = 60 * 4;  // 60LED/m
const uint16_t LED_PIN = 16;
const uint16_t UPDATE_PERIOD = 50;

NeoPixelBus<NeoGrbwFeature, Neo800KbpsMethod> strip(LED_COUNT, LED_PIN);

RgbwColor red(0xFF, 0, 0, 0);
RgbwColor green(0, 0xFF, 0, 0);
RgbwColor blue(0, 0, 0xFF, 0);
RgbwColor white(0, 0, 0, 0xFF);
RgbwColor black(0);

uint16_t base_index = 0;
void setup() {
  strip.Begin();
  strip.ClearTo(black);
  strip.Show();

  Serial.begin(115200);
}

uint32_t next_update = 0;
uint8_t serial_buf[100];
uint8_t serial_buf_len = 0;
void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    serial_buf[serial_buf_len++] = c;
    if (c == '\n') {
      if (serial_buf_len >= 7) {
        uint16_t led_num = (serial_buf[0] << 8) + serial_buf[1];
        strip.SetPixelColor(led_num, RgbwColor(serial_buf[2], serial_buf[3],
                                               serial_buf[4], serial_buf[5]));
        strip.Show();
        serial_buf_len = 0;
      }
    }
  }
}