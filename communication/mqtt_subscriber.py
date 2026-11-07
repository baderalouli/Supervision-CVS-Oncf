import json
import paho.mqtt.client as mqtt

from communication.mqtt_config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC_DATA,
    MQTT_TOPIC_ALARM,
    MQTT_CLIENT_SUBSCRIBER
)

from database.database import Database
from backend.diagnostic import diagnostiquer


class MQTTSubscriber:

    def __init__(self):

        self.database = Database()

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=MQTT_CLIENT_SUBSCRIBER
        )

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # ==========================================================
    # CONNEXION MQTT
    # ==========================================================

    def on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties
    ):

        if reason_code == 0:

            print("[MQTT] Subscriber connecté")

            client.subscribe(MQTT_TOPIC_DATA)
            client.subscribe(MQTT_TOPIC_ALARM)

            print("[MQTT] Abonné à :")
            print(f"  - {MQTT_TOPIC_DATA}")
            print(f"  - {MQTT_TOPIC_ALARM}")

        else:

            print(
                f"[MQTT] Erreur : {reason_code}"
            )

    # ==========================================================
    # RECEPTION MESSAGE
    # ==========================================================

    def on_message(
        self,
        client,
        userdata,
        message
    ):

        try:

            payload = json.loads(
                message.payload.decode()
            )

            print("\n" + "-" * 60)

            print("[MQTT] Message reçu")
            print(f"Topic : {message.topic}")

            # --------------------------------------------------
            # MESURE CVS
            # --------------------------------------------------

            if message.topic == MQTT_TOPIC_DATA:

                self.process_measurement(payload)

            # --------------------------------------------------
            # ALARME MQTT
            # --------------------------------------------------

            elif message.topic == MQTT_TOPIC_ALARM:

                self.process_alarm(payload)

        except Exception as error:

            print(
                f"[MQTT] Erreur traitement : {error}"
            )

    # ==========================================================
    # TRAITEMENT MESURE + DIAGNOSTIC
    # ==========================================================

    def process_measurement(
        self,
        payload
    ):

        try:

            data = payload["data"]

            # ==================================================
            # DIAGNOSTIC AUTOMATIQUE
            # ==================================================

            diagnostic = diagnostiquer(data)

            status = diagnostic["status"]

            alarmes = diagnostic["alarms"]

            # ==================================================
            # ENREGISTREMENT MESURE
            # ==================================================

            self.database.insert_measurement(
                data,
                status
            )

            print(
                f"[DATABASE] Mesure enregistrée "
                f"| État diagnostic : {status}"
            )

            # ==================================================
            # AFFICHAGE DES MESURES
            # ==================================================

            print(
                f"Tension entrée : "
                f"{data.get('voltage', 0):.2f} V"
            )

            print(
                f"Tension sortie : "
                f"{data.get('output_voltage', 0):.2f} V"
            )

            print(
                f"Courant : "
                f"{data.get('current', 0):.2f} A"
            )

            print(
                f"Température : "
                f"{data.get('temperature', 0):.2f} °C"
            )

            print(
                f"Vibration : "
                f"{data.get('vibration', 0):.2f} mm/s"
            )

            print(
                f"Rendement : "
                f"{data.get('efficiency', 0):.2f} %"
            )

            # ==================================================
            # RESULTAT DU DIAGNOSTIC
            # ==================================================

            if not alarmes:

                print(
                    "[DIAGNOSTIC] ✓ "
                    "Aucune anomalie détectée"
                )

            else:

                print(
                    f"[DIAGNOSTIC] "
                    f"{len(alarmes)} anomalie(s) détectée(s)"
                )

                for alarm in alarmes:

                    print(
                        f"  [{alarm['severity']}] "
                        f"{alarm['code']} - "
                        f"{alarm['message']} "
                        f"| Valeur : {alarm['value']}"
                    )

                    # ======================================================
                    # ENREGISTREMENT DE L'ALARME DANS SQLITE
                    # ======================================================

                    self.database.insert_alarm(
                        alarm,
                        data["timestamp"]
                    )

                    print(
                        f"[DATABASE] Alarme diagnostic enregistrée "
                        f"| {alarm['code']}"
                    )

        except Exception as error:

            print(
                f"[DIAGNOSTIC] Erreur : {error}"
            )

    # ==========================================================
    # TRAITEMENT ALARME MQTT
    # ==========================================================

    def process_alarm(
        self,
        payload
    ):

        try:

            alarm = payload["alarm"]

            timestamp = payload["timestamp"]

            self.database.insert_alarm(
                alarm,
                timestamp
            )

            print(
                f"[DATABASE] Alarme enregistrée "
                f"| {alarm['code']}"
            )

        except Exception as error:

            print(
                f"[DATABASE] Erreur alarme : {error}"
            )

    # ==========================================================
    # DEMARRAGE
    # ==========================================================

    def start(self):

        print(
            f"[MQTT] Connexion au broker "
            f"{MQTT_BROKER}:{MQTT_PORT}"
        )

        self.client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

        print(
            "[MQTT] En attente des messages..."
        )

        self.client.loop_forever()


# ==============================================================
# PROGRAMME PRINCIPAL
# ==============================================================

if __name__ == "__main__":

    subscriber = MQTTSubscriber()

    subscriber.start()