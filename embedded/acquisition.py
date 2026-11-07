from datetime import datetime


class DataAcquisition:

    def __init__(self):
        self.measurement_counter = 0

    def acquire(self, sensor_data):

        self.measurement_counter += 1

        data = {
            "timestamp": datetime.now().isoformat(),

            "voltage": float(sensor_data["voltage"]),
            "output_voltage": float(sensor_data["output_voltage"]),

            "current": float(sensor_data["current"]),
            "power": float(sensor_data["power"]),

            "temperature": float(sensor_data["temperature"]),
            "internal_temperature": float(
                sensor_data["internal_temperature"]
            ),

            "vibration": float(sensor_data["vibration"]),

            "fan": bool(sensor_data["fan"]),

            "battery": float(sensor_data["battery"]),


            "efficiency": float(sensor_data["efficiency"]),

            "protection_active": bool(
                sensor_data.get("protection_active", False)
            )
        }

        return data

    def validate(self, data):

        errors = []

        if data["voltage"] < 0:
            errors.append("Tension invalide")

        if data["current"] < 0:
            errors.append("Courant invalide")

        if data["temperature"] < -50:
            errors.append("Température invalide")

        if not 0 <= data["battery"] <= 100:
            errors.append("Niveau batterie invalide")

        if not 0 <= data["efficiency"] <= 100:
            errors.append("Rendement invalide")

        return errors

    def get_measurement_count(self):

        return self.measurement_counter