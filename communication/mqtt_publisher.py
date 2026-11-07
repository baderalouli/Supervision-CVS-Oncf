import json
import paho.mqtt.client as mqtt 

from communication.mqtt_config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC_DATA,
    MQTT_TOPIC_ALARM,
    MQTT_CLIENT_PUBLISHER
)


class MQTTPublisher:

    def __init__(self):

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=MQTT_CLIENT_PUBLISHER
        )

        self.connected = False

        self.client.on_connect = self.on_connect

    def on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties
    ):

        if reason_code == 0:

            self.connected = True

            print(
                "[MQTT] Publisher connecté au broker"
            )

        else:

            print(
                f"[MQTT] Erreur connexion : "
                f"{reason_code}"
            )

    def connect(self):

        print(
            f"[MQTT] Connexion à "
            f"{MQTT_BROKER}:{MQTT_PORT}"
        )

        self.client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

        self.client.loop_start()

    def publish_data(
        self,
        data,
        status
    ):

        payload = {

            "type": "measurement",

            "data": data,

            "status": status

        }

        message = json.dumps(
            payload
        )

        result = self.client.publish(
            MQTT_TOPIC_DATA,
            message
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:

            print(
                "[MQTT] Mesure publiée"
            )

        else:

            print(
                "[MQTT] Erreur publication"
            )

    def publish_alarm(
        self,
        alarm,
        timestamp
    ):

        payload = {

            "type": "alarm",

            "timestamp": timestamp,

            "alarm": alarm

        }

        message = json.dumps(
            payload
        )

        result = self.client.publish(
            MQTT_TOPIC_ALARM,
            message
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:

            print(
                "[MQTT] Alarme publiée"
            )

        else:

            print(
                "[MQTT] Erreur publication"
            )

    def disconnect(self):

        self.client.loop_stop()

        self.client.disconnect()

        print(
            "[MQTT] Publisher déconnecté"
        )