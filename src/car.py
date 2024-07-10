import time

import websocket
import threading


class Car:

    def __init__(self, address="ws://toy-tank.local:81"):
        self.ws = websocket.WebSocketApp(address,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.start()
        time.sleep(5)

    def move_forward(self, angle):
        command = f"moveForward{-angle}"
        self.ws.send(command)
        print(f"Sent: {command}")

    def move_backward(self, angle):
        command = f"moveBackward{angle}"
        self.ws.send(command)
        print(f"Sent: {command}")

    def stop(self):
        command = "stop"
        self.ws.send(command)
        print(f"Sent: {command}")

    def send_set_speed(self, speed):
        command = f"setSpeed{speed}"
        self.ws.send(command)
        print(f"Sent: {command}")

    def on_message(self, ws, message):
        print(f"Received: {message}")

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")


if __name__ == "__main__":
    car = Car()
    time.sleep(5)
    # car.move_forward(0)
