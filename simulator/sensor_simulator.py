class SensorSimulator:

    def read(self, cvs_data):

        return {
            "voltage": cvs_data["input_voltage"],

            "output_voltage": cvs_data["output_voltage"],

            "current": cvs_data["current"],

            "temperature": cvs_data["igbt_temperature"],

            "internal_temperature":
                cvs_data["internal_temperature"],

            "vibration": cvs_data["vibration"],

            "fan": cvs_data["fan"],

            "battery": cvs_data["battery"],

            "power": cvs_data["power"],

            "efficiency": cvs_data["efficiency"],

            "protection_active":
                cvs_data.get("protection_active", False)
        }