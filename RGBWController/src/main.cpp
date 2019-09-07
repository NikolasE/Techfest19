#include <Arduino.h>
#include <NeoPixelBus.h>

enum class cmd_t {
  CMD_RESET = 'r',
  CMD_SEAT = 's',
  CMD_DIST = 'd',
  CMD_CHAIN = 'c',
  CMD_VEL = 'v',
  CMD_SETP_SEAT = 'S',
  CMD_SETP_CHAIN = 'C',
};

const bool REVERSE_LEDS = true;
const uint8_t STRIP_COUNT = 60;
const uint16_t LED_COUNT = STRIP_COUNT * 4;  // 60LED/m
const uint16_t LED_PIN = 16;

const uint8_t LED_OFFSET_UNDER_SEAT = 0;
const uint8_t LED_OFFSET_SEAT = 60;
const uint8_t LED_OFFSET_CHAIN = 120;
const uint8_t LED_OFFSET_VEL = 180;

const RgbwColor COLOR_SEAT_SETP(0, 0, 0, 0xFF);
const RgbwColor COLOR_SEAT_BACK(0, 0, 0xFF, 0);
const RgbwColor COLOR_SEAT_FRONT(0, 0xFF, 0, 0);
const RgbwColor COLOR_CHAIN_SETP(0, 0, 0, 0xFF);
const RgbwColor COLOR_CHAIN_FRONT(0xFF, 0, 0, 0);
const RgbwColor COLOR_CHAIN_BACK(0, 0, 0x05, 0);
const RgbwColor COLOR_OFF(0, 0, 0, 0);

NeoPixelBus<NeoGrbwFeature, Neo800KbpsMethod> strip(LED_COUNT, LED_PIN);

const double VEL_DECAY_PERIOD = 0.01;  // brightness lost per ms
const double VEL_DECAY_FACTOR = 0.99;  // brightness factor

uint8_t serial_buf[100];
uint8_t serial_buf_len = 0;

void setup() {
  strip.Begin();

  Serial.begin(1000000);
}

double map(double x, double in_min, double in_max, double out_min,
           double out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setPixel(uint16_t indexPixel, RgbwColor color) {
  if (REVERSE_LEDS) {
    strip.SetPixelColor(LED_COUNT - indexPixel - 1, color);
  } else {
    strip.SetPixelColor(indexPixel, color);
  }
}

RgbwColor getPixel(uint16_t indexPixel) {
  if (REVERSE_LEDS) {
    return strip.GetPixelColor(LED_COUNT - indexPixel - 1);
  } else {
    return strip.GetPixelColor(indexPixel);
  }
}

void setGraph(uint8_t val, uint8_t setpoint, uint8_t led_index_offset) {
  double dist_to_setpoint = fabs(val - setpoint);
  for (uint8_t i = 0; i < STRIP_COUNT; i++) {
    int8_t dist_to_center = abs(i - val);
    double brightness = 0;
    switch (dist_to_center) {
      case 5:
        brightness = 0.5 / 2.0 / 2.0 / 2.0 / 2.0 / 2.0;
        break;
      case 4:
        brightness = 0.5 / 2.0 / 2.0 / 2.0 / 2.0;
        break;
      case 3:
        brightness = 0.5 / 2.0 / 2.0 / 2.0;
        break;
      case 2:
        brightness = 0.5 / 2.0 / 2.0;
        break;
      case 1:
        brightness = 0.5 / 2.0;
        break;
      case 0:
        brightness = 0.5;
        break;
      default:
        brightness = 0.0;
        break;
    }
    double hue = map(dist_to_setpoint, 10.0, 0.0, 0.0, 120.0 / 360.0);
    hue = max(hue, 0.0);
    hue = min(hue, 120.0 / 360.0);
    HslColor color(hue, 1.0, brightness);
    setPixel(led_index_offset + i, color);
  }

  for (uint8_t i = 0; i < STRIP_COUNT; i++) {
    RgbwColor color = getPixel(led_index_offset + i);
    color.W = (i == setpoint) ? 0xFF : 0x00;
    setPixel(led_index_offset + i, color);
  }
}

uint8_t chain_setpoint = 255;
uint8_t chain_val = 255;
void setChainLeds(uint8_t val) {
  chain_val = val;
  setGraph(val, chain_setpoint, LED_OFFSET_CHAIN);
  strip.Show();
}

uint8_t seat_setpoint = 255;
uint8_t seat_val = 255;
void setSeatLeds(uint8_t val) {
  seat_val = val;
  setGraph(val, seat_setpoint, LED_OFFSET_SEAT);
  setGraph(val, seat_setpoint, LED_OFFSET_UNDER_SEAT);
  strip.Show();
}

void clearLeds() {
  strip.ClearTo(COLOR_OFF);
  strip.Show();
}

void setDistLeds(uint8_t val) {
  if (val != 255) {
    for (uint8_t i = 0; i < val; i++) {
      RgbwColor color = getPixel(LED_OFFSET_VEL + i);
      color.B = 255;
      setPixel(LED_OFFSET_VEL + i, color);
    }
    for (uint8_t i = val; i < STRIP_COUNT; i++) {
      RgbwColor color = getPixel(LED_OFFSET_VEL + i);
      color.B = 0;
      setPixel(LED_OFFSET_VEL + i, color);
    }
  }
}

uint32_t vel_last_update = 0;
double vel_brightness = 0;
void updateVelLeds() {
  uint32_t now = millis();
  if (vel_brightness >= 0) {
    vel_brightness *=
        pow(VEL_DECAY_FACTOR, (now - vel_last_update) * VEL_DECAY_PERIOD);
    for (uint8_t i = 0; i < STRIP_COUNT; i++) {
      RgbwColor color = getPixel(LED_OFFSET_VEL + i);
      color.W = round(vel_brightness);
      setPixel(LED_OFFSET_VEL + i, color);
    }
    strip.Show();
  }
}

void setVelLeds(uint8_t val) {
  vel_last_update = millis();
  vel_brightness = val;
  updateVelLeds();
}

void onSerialReceive() {
  switch (static_cast<cmd_t>(serial_buf[0])) {
    case cmd_t::CMD_RESET:
      clearLeds();
      break;
    case cmd_t::CMD_SEAT:
      setSeatLeds(serial_buf[1]);
      break;
    case cmd_t::CMD_CHAIN:
      setChainLeds(serial_buf[1]);
      break;
    case cmd_t::CMD_DIST:
      setDistLeds(serial_buf[1]);
      break;
    case cmd_t::CMD_VEL:
      setVelLeds(serial_buf[1]);
      break;
    case cmd_t::CMD_SETP_SEAT:
      seat_setpoint = serial_buf[1];
      setSeatLeds(seat_val);
      break;
    case cmd_t::CMD_SETP_CHAIN:
      chain_setpoint = serial_buf[1];
      setChainLeds(chain_val);
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
  updateVelLeds();
}
