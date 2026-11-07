import yaml


class CVSDiagnostic:

    def __init__(self, config_file):

        with open(config_file, "r", encoding="utf-8") as file:
            self.thresholds = yaml.safe_load(file)

    def analyze(self, data):

        alarms = []

        temperature = data["temperature"]
        current = data["current"]
        voltage = data["voltage"]
        vibration = data["vibration"]
        battery = data["battery"]
        efficiency = data["efficiency"]
        fan = data["fan"]

        # Température
        if temperature >= self.thresholds["temperature"]["critical"]:
            alarms.append({
                "code": "CVS-003",
                "type": "SURCHAUFFE",
                "severity": "CRITICAL",
                "message": "Température IGBT critique",
                "value": temperature
            })

        elif temperature >= self.thresholds["temperature"]["warning"]:
            alarms.append({
                "code": "CVS-003",
                "type": "SURCHAUFFE",
                "severity": "WARNING",
                "message": "Température IGBT élevée",
                "value": temperature
            })

        # Courant
        if current >= self.thresholds["current"]["critical"]:
            alarms.append({
                "code": "CVS-002",
                "type": "SURINTENSITE",
                "severity": "CRITICAL",
                "message": "Courant critique",
                "value": current
            })

        elif current >= self.thresholds["current"]["warning"]:
            alarms.append({
                "code": "CVS-002",
                "type": "SURINTENSITE",
                "severity": "WARNING",
                "message": "Courant élevé",
                "value": current
            })

        # Tension
        if (
            voltage <= self.thresholds["voltage"]["critical_min"]
            or
            voltage >= self.thresholds["voltage"]["critical_max"]
        ):
            alarms.append({
                "code": "CVS-001",
                "type": "SURTENSION",
                "severity": "CRITICAL",
                "message": "Tension critique",
                "value": voltage
            })

        elif (
            voltage <= self.thresholds["voltage"]["warning_min"]
            or
            voltage >= self.thresholds["voltage"]["warning_max"]
        ):
            alarms.append({
                "code": "CVS-001",
                "type": "TENSION",
                "severity": "WARNING",
                "message": "Tension hors zone nominale",
                "value": voltage
            })

        # Ventilateur
        if not fan:
            alarms.append({
                "code": "CVS-004",
                "type": "VENTILATION",
                "severity": "WARNING",
                "message": "Défaut du ventilateur",
                "value": 0
            })

        # Batterie
        if battery <= self.thresholds["battery"]["critical"]:
            alarms.append({
                "code": "CVS-005",
                "type": "BATTERIE",
                "severity": "CRITICAL",
                "message": "Batterie critique",
                "value": battery
            })

        elif battery <= self.thresholds["battery"]["warning"]:
            alarms.append({
                "code": "CVS-005",
                "type": "BATTERIE",
                "severity": "WARNING",
                "message": "Batterie faible",
                "value": battery
            })

        # Vibration
        if vibration >= self.thresholds["vibration"]["critical"]:
            alarms.append({
                "code": "CVS-006",
                "type": "VIBRATION",
                "severity": "CRITICAL",
                "message": "Vibration anormale",
                "value": vibration
            })

        elif vibration >= self.thresholds["vibration"]["warning"]:
            alarms.append({
                "code": "CVS-006",
                "type": "VIBRATION",
                "severity": "WARNING",
                "message": "Vibration élevée",
                "value": vibration
            })

        # Rendement
        if efficiency <= self.thresholds["efficiency"]["critical"]:
            alarms.append({
                "code": "CVS-007",
                "type": "RENDEMENT",
                "severity": "CRITICAL",
                "message": "Rendement très faible",
                "value": efficiency
            })

        elif efficiency <= self.thresholds["efficiency"]["warning"]:
            alarms.append({
                "code": "CVS-007",
                "type": "RENDEMENT",
                "severity": "WARNING",
                "message": "Baisse du rendement",
                "value": efficiency
            })
            
        # Protection thermique
        if data.get("protection_active", False):

            alarms.append({
                "code": "CVS-008",
                "type": "PROTECTION_THERMIQUE",
                "severity": "CRITICAL",
                "message": "Protection thermique active",
                "value": temperature
            })

        # État général
        status = "NORMAL"

        if any(a["severity"] == "CRITICAL" for a in alarms):
            status = "CRITICAL"

        elif any(a["severity"] == "WARNING" for a in alarms):
            status = "WARNING"

        return status, alarms