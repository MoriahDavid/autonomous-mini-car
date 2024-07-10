# using this app on Android device https://github.com/umer0586/SensorServer
import threading

import websocket
import json


class Sensors:
    sensors_types_map = {
        "accelerometer": "android.sensor.accelerometer",
        "gyroscope": "android.sensor.gyroscope",
        "magnetic_field": "android.sensor.magnetic_field",
    }

    def __init__(self, host, port=8081):
        self.ws = None
        self.sensors = {}
        self.url = self._generate_url(host, port)
        self.connect(self.url)

    def _generate_url(self, host, port):
        sensors_types_ids = ",".join([f'"{sensor}"' for sensor in self.sensors_types_map.values()])
        url = f"ws://{host}:{port}/sensors/connect?types=[{sensors_types_ids}]"

        return url

    def get_sensors(self):
        return self.sensors

    def on_message(self, ws, message):
        sensor_data = json.loads(message)
        sensor_type = sensor_data["type"]
        self.sensors[sensor_type] = sensor_data

        values = sensor_data["values"]
        x = values[0]
        y = values[1]
        z = values[2]
        # print(f"Sensor: {sensor_type}: \tx = {x:4.4f}f y = {y:2.4f} z = {z:2.4f}")

    def on_error(self, ws, error):
        print("error occurred ", error)

    def on_close(self, ws, close_code, reason):
        print("connection closed : ", reason)

    def on_open(self, ws):
        print("connected")

    def connect(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def close(self):
        self.ws.close()


if __name__ == "__main__":
    sonsors = Sensors("Galaxy-S10.fritz.box", 8080)
