def diagnostiquer(data):
    """
    Moteur de diagnostic du CVS.
    Analyse les mesures et détecte les anomalies.
    """

    alarmes = []

    voltage = data.get("voltage", 0)
    output_voltage = data.get("output_voltage", 0)
    current = data.get("current", 0)
    temperature = data.get("temperature", 0)
    vibration = data.get("vibration", 0)
    efficiency = data.get("efficiency", 100)
    fan = data.get("fan", False)

    # ==========================================================
    # CVS-001 : SOUS-TENSION ENTREE
    # ==========================================================

    if voltage < 2700:

        alarmes.append({
            "code": "CVS-001",
            "type": "ELECTRICAL",
            "severity": "WARNING",
            "message": "Sous-tension de l'entrée CVS",
            "value": voltage
        })

    # ==========================================================
    # CVS-002 : SURTENSION ENTREE
    # ==========================================================

    if voltage > 3300:

        alarmes.append({
            "code": "CVS-002",
            "type": "ELECTRICAL",
            "severity": "CRITICAL",
            "message": "Surtension de l'entrée CVS",
            "value": voltage
        })

    # ==========================================================
    # CVS-003 : TEMPERATURE IGBT
    # ==========================================================

    if temperature >= 100:

        alarmes.append({
            "code": "CVS-003",
            "type": "THERMAL",
            "severity": "CRITICAL",
            "message": "Température IGBT critique",
            "value": temperature
        })

    elif temperature >= 85:

        alarmes.append({
            "code": "CVS-003",
            "type": "THERMAL",
            "severity": "WARNING",
            "message": "Température IGBT élevée",
            "value": temperature
        })

    # ==========================================================
    # CVS-004 : SURINTENSITE
    # ==========================================================

    if current > 100:

        alarmes.append({
            "code": "CVS-004",
            "type": "ELECTRICAL",
            "severity": "CRITICAL",
            "message": "Surintensité du CVS",
            "value": current
        })

    elif current > 90:

        alarmes.append({
            "code": "CVS-004",
            "type": "ELECTRICAL",
            "severity": "WARNING",
            "message": "Courant élevé",
            "value": current
        })

    # ==========================================================
    # CVS-005 : TENSION SORTIE
    # ==========================================================

    if output_voltage < 350:

        alarmes.append({
            "code": "CVS-005",
            "type": "ELECTRICAL",
            "severity": "CRITICAL",
            "message": "Sous-tension de sortie",
            "value": output_voltage
        })

    elif output_voltage > 430:

        alarmes.append({
            "code": "CVS-005",
            "type": "ELECTRICAL",
            "severity": "CRITICAL",
            "message": "Surtension de sortie",
            "value": output_voltage
        })

    # ==========================================================
    # CVS-006 : VIBRATION
    # ==========================================================

    if vibration > 4:

        alarmes.append({
            "code": "CVS-006",
            "type": "MECHANICAL",
            "severity": "WARNING",
            "message": "Niveau de vibration élevé",
            "value": vibration
        })

    # ==========================================================
    # CVS-007 : RENDEMENT
    # ==========================================================

    if efficiency < 85:

        alarmes.append({
            "code": "CVS-007",
            "type": "PERFORMANCE",
            "severity": "CRITICAL",
            "message": "Rendement du CVS insuffisant",
            "value": efficiency
        })

    elif efficiency < 90:

        alarmes.append({
            "code": "CVS-007",
            "type": "PERFORMANCE",
            "severity": "WARNING",
            "message": "Baisse du rendement",
            "value": efficiency
        })

    # ==========================================================
    # CVS-008 : VENTILATION
    # ==========================================================

    if temperature >= 85 and not fan:

        alarmes.append({
            "code": "CVS-008",
            "type": "THERMAL",
            "severity": "CRITICAL",
            "message": "Défaut de ventilation",
            "value": temperature
        })

    # ==========================================================
    # ETAT GENERAL DU CVS
    # ==========================================================

    if any(
        alarm["severity"] == "CRITICAL"
        for alarm in alarmes
    ):

        status = "CRITICAL"

    elif any(
        alarm["severity"] == "WARNING"
        for alarm in alarmes
    ):

        status = "WARNING"

    else:

        status = "NORMAL"

    return {
        "status": status,
        "alarms": alarmes
    }