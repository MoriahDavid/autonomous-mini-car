import websocket
import time
import threading

# WebSocket address of the ESP32
ws_address = "ws://toy-tank.local:81/"


# Commands
def send_move_forward(ws, angle):
    command = f"moveForward{-angle}"
    ws.send(command)
    print(f"Sent: {command}")


def send_move_backward(ws, angle):
    command = f"moveBackward{-angle}"
    ws.send(command)
    print(f"Sent: {command}")


def send_stop(ws):
    command = "stop"
    ws.send(command)
    print(f"Sent: {command}")


def send_set_speed(ws, speed):
    command = f"setSpeed{speed}"
    ws.send(command)
    print(f"Sent: {command}")


def on_message(ws, message):
    print(f"Received: {message}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")


def on_open(ws):
    print("WebSocket opened")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_address,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

    time.sleep(1)  # Give some time for the connection to establish

    try:
        while True:
            command = input("Enter command (forward, stop, speed): ")
            if command == "f":
                angle = int(input("Enter angle (-90 to 90): "))
                send_move_forward(ws, angle)
            elif command == "b":
                angle = int(input("Enter angle (-90 to 90): "))
                send_move_backward(ws, angle)
            elif command == "s":
                send_stop(ws)
            elif command == "speed":
                speed = int(input("Enter speed (0 to 255): "))
                send_set_speed(ws, speed)
            else:
                print("Unknown command")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ws.close()
        ws_thread.join()
