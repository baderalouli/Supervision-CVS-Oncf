import time
import json
from pathlib import Path

from simulator.cvs_model import CVSModel
from simulator.sensor_simulator import SensorSimulator
from communication.mqtt_publisher import MQTTPublisher

from embedded.acquisition import DataAcquisition
from embedded.filtering import MovingAverageFilter
from embedded.diagnostic import CVSDiagnostic


# =====================================================
# CHEMINS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_FILE = (
    BASE_DIR
    / "config"
    / "simulation_state.json"
)

THRESHOLDS_FILE = (
    BASE_DIR
    / "config"
    / "thresholds.yaml"
)


# =====================================================
# LECTURE DU SCENARIO
# =====================================================

def get_scenario():

    try:

        if not STATE_FILE.exists():

            STATE_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            STATE_FILE.write_text(
                json.dumps({
                    "scenario": "normal"
                }),
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

        return scenario

    except Exception as error:

        print(
            f"[STATE ERROR] {error}"
        )

        return "normal"


# =====================================================
# AFFICHAGE
# =====================================================

def print_data(
    data,
    status,
    alarms,
    scenario
):

    print("\n" + "=" * 70)

    print(
        "              CVS MONITORING SYSTEM"
    )

    print("=" * 70)

    print(
        f"Scénario             : {scenario}"
    )

    print(
        f"État                 : {status}"
    )

    print(
        f"Tension entrée       : "
        f"{data['voltage']:.2f} V"
    )

    print(
        f"Tension sortie       : "
        f"{data['output_voltage']:.2f} V"
    )

    print(
        f"Courant              : "
        f"{data['current']:.2f} A"
    )

    print(
        f"Puissance            : "
        f"{data['power']:.2f} W"
    )

    print(
        f"Température IGBT     : "
        f"{data['temperature']:.2f} °C"
    )

    print(
        f"Température interne  : "
        f"{data['internal_temperature']:.2f} °C"
    )

    print(
        f"Vibration            : "
        f"{data['vibration']:.2f} mm/s"
    )

    print(
        f"Ventilateur          : "
        f"{'ON' if data['fan'] else 'OFF'}"
    )

    print(
        f"Batterie             : "
        f"{data['battery']:.2f} %"
    )

    print(
        f"Rendement            : "
        f"{data['efficiency']:.2f} %"
    )

    print(
        f"Protection CVS       : "
        f"{'ACTIVE' if data.get('protection_active', False) else 'INACTIVE'}"
    )

    if alarms:

        print("\nALARMES :")

        for alarm in alarms:

            print(
                f"[{alarm['severity']}] "
                f"{alarm['code']} - "
                f"{alarm['message']} "
                f"(valeur={alarm['value']})"
            )

    else:

        print(
            "\nALARMES : Aucune"
        )

    print("=" * 70)


# =====================================================
# PROGRAMME PRINCIPAL
# =====================================================

def main():

    print()
    print("=" * 70)
    print(
        "       CVS MONITORING - SIMULATION TEMPS REEL"
    )
    print("=" * 70)

    print(
        f"[STATE] Fichier : {STATE_FILE}"
    )

    # =================================================
    # INITIALISATION
    # =================================================

    cvs = CVSModel()

    sensors = SensorSimulator()

    acquisition = DataAcquisition()

    filtering = MovingAverageFilter(
        window_size=5
    )

    diagnostic = CVSDiagnostic(
        str(THRESHOLDS_FILE)
    )

    mqtt_publisher = MQTTPublisher()

    # =================================================
    # MQTT
    # =================================================

    print(
        "[MQTT] Connexion..."
    )

    mqtt_publisher.connect()

    print(
        "[MQTT] Connecté"
    )

    print(
        "[CVS] Simulation démarrée"
    )

    print(
        "[CVS] Les scénarios peuvent être "
        "modifiés depuis le Dashboard"
    )

    print("=" * 70)

    previous_scenario = None

    try:

        while True:

            # =========================================
            # 1. LECTURE DU SCENARIO
            # =========================================

            scenario = get_scenario()

            # =========================================
            # 2. DETECTION DU CHANGEMENT
            # =========================================

            if scenario != previous_scenario:

                print()
                print(
                    ">>> =================================="
                )

                print(
                    f">>> NOUVEAU SCENARIO : {scenario}"
                )

                print(
                    ">>> =================================="
                )

                previous_scenario = scenario

            # =========================================
            # 3. SIMULATION CVS
            # =========================================

            cvs_data = cvs.update(
                scenario
            )

            # =========================================
            # 4. SIMULATION DES CAPTEURS
            # =========================================

            sensor_data = sensors.read(
                cvs_data
            )

            # =========================================
            # 5. ACQUISITION
            # =========================================

            acquired_data = acquisition.acquire(
                sensor_data
            )

            errors = acquisition.validate(
                acquired_data
            )

            if errors:

                print(
                    "\nERREUR ACQUISITION :"
                )

                for error in errors:

                    print(
                        f"- {error}"
                    )

                time.sleep(1)

                continue

            # =========================================
            # 6. FILTRAGE
            # =========================================

            filtered_data = filtering.update(
                acquired_data
            )

            # =========================================
            # 7. DIAGNOSTIC
            # =========================================

            status, alarms = diagnostic.analyze(
                filtered_data
            )

            # =========================================
            # 8. PUBLICATION DES MESURES
            # =========================================

            mqtt_publisher.publish_data(
                filtered_data,
                status
            )

            # =========================================
            # 9. PUBLICATION DES ALARMES
            # =========================================

            for alarm in alarms:

                mqtt_publisher.publish_alarm(
                    alarm,
                    filtered_data["timestamp"]
                )

            # =========================================
            # 10. AFFICHAGE
            # =========================================

            print_data(
                filtered_data,
                status,
                alarms,
                scenario
            )

            # =========================================
            # 11. ATTENTE
            # =========================================

            time.sleep(1)

    except KeyboardInterrupt:

        print()
        print(
            "[CVS] Simulation arrêtée"
        )

    finally:

        mqtt_publisher.disconnect()

        print(
            "[MQTT] Déconnecté"
        )


if __name__ == "__main__":

    main()