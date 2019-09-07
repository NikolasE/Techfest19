#include <Arduino.h>
#include <NeoPixelBus.h>

enum class cmd_t {
  CMD_RESET = 'r',
  CMD_SEAT = 's',
  CMD_CHAIN = 'c',
  CMD_VEL = 'v',
  CMD_SETP_SEAT = 'S',
  CMD_SETP_CHAIN = 'C',
};

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

uint8_t serial_buf[100];
uint8_t serial_buf_len = 0;

void setup() {
  strip.Begin();

  Serial.begin(1000000);
}

uint8_t seat_setpoint = 255;
uint8_t seat_val = 255;
void setSeatLeds(uint8_t val) {
  seat_val = val;
  if (seat_val != 255) {
    for (uint8_t i = 0; i < val; i++) {
      strip.SetPixelColor(LED_OFFSET_UNDER_SEAT + i, COLOR_SEAT_BACK);
      strip.SetPixelColor(LED_OFFSET_SEAT + i, COLOR_SEAT_BACK);
    }
    for (uint8_t i = val; i < STRIP_COUNT; i++) {
      strip.SetPixelColor(LED_OFFSET_UNDER_SEAT + i, COLOR_SEAT_FRONT);
      strip.SetPixelColor(LED_OFFSET_SEAT + i, COLOR_SEAT_FRONT);
    }
  }

  if (seat_setpoint != 255) {
    strip.SetPixelColor(LED_OFFSET_SEAT + seat_setpoint, COLOR_SEAT_SETP);
    strip.SetPixelColor(LED_OFFSET_UNDER_SEAT + seat_setpoint, COLOR_SEAT_SETP);
  }

  strip.Show();
}

uint8_t chain_setpoint = 255;
uint8_t chain_val = 255;
void setChainLeds(uint8_t val) {
  chain_val = val;
  if (chain_val != 255) {
    for (uint8_t i = 0; i < val; i++) {
      strip.SetPixelColor(LED_OFFSET_CHAIN + i, COLOR_CHAIN_FRONT);
    }
    for (uint8_t i = val; i < STRIP_COUNT; i++) {
      strip.SetPixelColor(LED_OFFSET_CHAIN + i, COLOR_CHAIN_BACK);
    }
  }

  if (chain_setpoint != 255) {
    strip.SetPixelColor(LED_OFFSET_CHAIN + chain_setpoint, COLOR_CHAIN_SETP);
  }
  strip.Show();
}

void clearLeds() {
  strip.ClearTo(COLOR_OFF);
  strip.Show();
}

uint32_t vel_last_update = 0;
RgbwColor vel_color(0, 0, 0, 0);
void setVelLeds(uint8_t val) {
  vel_color.W = val;
  for (uint8_t i = 0; i < STRIP_COUNT; i++) {
    strip.SetPixelColor(LED_OFFSET_VEL + i, vel_color);
  }
  vel_last_update = millis();

  strip.Show();
}

void updateVelLeds() {
  uint32_t now = millis();
  if (vel_color.W > 0) {
    double new_bright =
        vel_color.W - (now - vel_last_update) * VEL_DECAY_PERIOD;
    vel_color.W = new_bright;
    for (uint8_t i = 0; i < STRIP_COUNT; i++) {
      strip.SetPixelColor(LED_OFFSET_VEL + i, vel_color);
    }
    strip.Show();
  }
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
