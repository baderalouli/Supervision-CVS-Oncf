import json
import random
import time
from datetime import datetime
from pathlib import Path

import paho.mqtt.client as mqtt

from communication.mqtt_config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC_DATA,
    MQTT_CLIENT_PUBLISHER
)


#STATE_FILE = Path("config/simulation_state.json")
BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "config" / "simulation_state.json"

def get_scenario():

    try:

        if not STATE_FILE.exists():

            STATE_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            STATE_FILE.write_text(
                '{"scenario": "normal"}',
                encoding="utf-8"
            )

        content = STATE_FILE.read_text(
            encoding="utf-8"
        )

        state = json.loads(content)

        scenario = state.get(
            "scenario",
            "normal"
        )

        print(f"[STATE] Scénario lu : {scenario}")

        return scenario

    except Exception as error:

        print(f"[STATE] Erreur : {error}")

        return "normal"

def generate_measurement(scenario):

    # ==============================
    # VALEURS NORMALES
    # ==============================

    voltage = random.uniform(
        2950,
        3150
    )

    output_voltage = random.uniform(
        395,
        405
    )

    current = random.uniform(
        70,
        85
    )

    temperature = random.uniform(
        55,
        70
    )

    internal_temperature = (
        temperature + random.uniform(
            5,
            12
        )
    )

    vibration = random.uniform(
        1,
        2.5
    )

    battery = random.uniform(
        95,
        100
    )

    efficiency = random.uniform(
        92,
        96
    )

    fan = True

    protection_active = False


    # ==============================
    # SCENARIOS DE PANNE
    # ==============================

    if scenario == "overtemperature":

        temperature = random.uniform(
            102,
            115
        )

        internal_temperature = (
            temperature + random.uniform(
                5,
                15
            )
        )


    elif scenario == "overcurrent":

        current = random.uniform(
            105,
            125
        )


    elif scenario == "overvoltage":

        voltage = random.uniform(
            3350,
            3500
        )


    elif scenario == "low_output_voltage":

        output_voltage = random.uniform(
            320,
            345
        )


    elif scenario == "high_vibration":

        vibration = random.uniform(
            4.5,
            7
        )


    elif scenario == "fan_failure":

        fan = False

        temperature = random.uniform(
            88,
            108
        )

        internal_temperature = (
            temperature + random.uniform(
                8,
                15
            )
        )


    elif scenario == "low_efficiency":

        efficiency = random.uniform(
            78,
            88
        )


    elif scenario == "combined":

        voltage = random.uniform(
            3350,
            3500
        )

        current = random.uniform(
            105,
            125
        )

        temperature = random.uniform(
            103,
            118
        )

        internal_temperature = (
            temperature + random.uniform(
                8,
                15
            )
        )

        vibration = random.uniform(
            4.5,
            7
        )

        efficiency = random.uniform(
            78,
            85
        )

        fan = False

        output_voltage = random.uniform(
            320,
            345
        )


    # ==============================
    # PROTECTION
    # ==============================

    if (
        temperature >= 100
        or current > 100
        or voltage > 3300
        or output_voltage < 350
    ):

        protection_active = True


    # ==============================
    # PUISSANCE
    # ==============================

    power = (
        output_voltage
        * current
    ) / 1000


    return {

        "timestamp":
            datetime.now().isoformat(),

        "voltage":
            round(voltage, 2),

        "output_voltage":
            round(output_voltage, 2),

        "current":
            round(current, 2),

        "power":
            round(power, 2),

        "temperature":
            round(temperature, 2),

        "internal_temperature":
            round(
                internal_temperature,
                2
            ),

        "vibration":
            round(vibration, 2),

        "fan":
            fan,

        "battery":
            round(battery, 2),

        "efficiency":
            round(efficiency, 2),

        "protection_active":
            protection_active
    }


def main():

    print("=" * 70)
    print("       CVS SIMULATOR - SYSTEME DE SURVEILLANCE")
    print("=" * 70)

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_PUBLISHER
    )

    print(
        f"[MQTT] Connexion à "
        f"{MQTT_BROKER}:{MQTT_PORT}"
    )

    client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    client.loop_start()

    print("[MQTT] Connecté")
    print("[CVS] Simulation démarrée")
    print()

    try:

        while True:

            scenario = get_scenario()

            data = generate_measurement(
                scenario
            )

            # Statut général provisoire
            status = "NORMAL"

            if scenario != "normal":
                status = "FAULT_SIMULATION"

            payload = {

                "timestamp":
                    datetime.now().isoformat(),

                "status":
                    status,

                "data":
                    data
            }

            client.publish(
                MQTT_TOPIC_DATA,
                json.dumps(payload)
            )

            print(
                f"[CVS] Scénario : "
                f"{scenario}"
            )

            print(
                f"      Vin       : "
                f"{data['voltage']} V"
            )

            print(
                f"      Vout      : "
                f"{data['output_voltage']} V"
            )

            print(
                f"      Courant   : "
                f"{data['current']} A"
            )

            print(
                f"      Puissance : "
                f"{data['power']} kW"
            )

            print(
                f"      Temp.     : "
                f"{data['temperature']} °C"
            )

            print(
                f"      Vibration : "
                f"{data['vibration']}"
            )

            print(
                f"      Rendement : "
                f"{data['efficiency']} %"
            )

            print(
                f"      Ventil.   : "
                f"{'ON' if data['fan'] else 'OFF'}"
            )

            print("-" * 70)

            time.sleep(2)

    except KeyboardInterrupt:

        print()
        print("[CVS] Simulation arrêtée")

    finally:

        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":

    main()