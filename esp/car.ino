#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ESPmDNS.h>

// Motor Pins
const int enablePin1 = D1;  // ENA on the L298N
const int motor1Pin1 = D2; // IN1 on the L298N
const int motor1Pin2 = D3;  // IN2 on the L298N

const int enablePin2 = D4; // ENB on the L298N
const int motor2Pin1 = D5;  // IN3 on the L298N
const int motor2Pin2 = D6; // IN4 on the L298N

// Network credentials
const char* ssid = "*****";
const char* password = "*****";

WebSocketsServer webSocket = WebSocketsServer(81);

int speed = 255; // Speed range 0-255

// Function declarations
void onWebSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length);
void moveForward(int angle);
void stopMotors();
void setSpeed(int newSpeed);

void setup() {
  Serial.begin(115200);

  // Motor pin modes
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enablePin1, OUTPUT);
  pinMode(enablePin2, OUTPUT);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Start the WebSocket server
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);

  // Set up mDNS
  if (!MDNS.begin("toy-tank")) {
    Serial.println("Error setting up mDNS responder!");
  } else {
    Serial.println("mDNS responder started");
  }

  MDNS.addService("http", "tcp", 81);
}

void loop() {
  // Handle WebSocket connections
  webSocket.loop();
}

void onWebSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  if (type == WStype_TEXT) {
    String message = String((char *)payload).substring(0, length);
    Serial.println("Message: " + message);

    if (message.startsWith("moveForward")) {
      int angle = message.substring(11).toInt();
      moveForward(angle);
    } else if (message.startsWith("moveBackward")) {
      int angle = message.substring(11).toInt();
      moveBackward(angle);
    } else if (message.equals("stop")) {
      stopMotors();
    } else if (message.startsWith("setSpeed")) {
      int newSpeed = message.substring(8).toInt();
      setSpeed(newSpeed);
    }
  }
}

void moveForward(int angle) {
  int leftSpeed = speed;
  int rightSpeed = speed;

  if (angle < 0) {
    rightSpeed = map(angle, -90, 0, 0, speed);
  } else if (angle > 0) {
    leftSpeed = map(angle, 0, 90, speed, 0);
  }

  analogWrite(enablePin1, leftSpeed);
  analogWrite(enablePin2, rightSpeed);
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

void moveBackward(int angle) {
  int leftSpeed = speed;
  int rightSpeed = speed;

  if (angle < 0) {
    rightSpeed = map(angle, -90, 0, 0, speed);
  } else if (angle > 0) {
    leftSpeed = map(angle, 0, 90, speed, 0);
  }

  analogWrite(enablePin1, leftSpeed);
  analogWrite(enablePin2, rightSpeed);
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

void stopMotors() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
  analogWrite(enablePin1, 0);
  analogWrite(enablePin2, 0);
}

void setSpeed(int newSpeed) {
  speed = newSpeed;
}