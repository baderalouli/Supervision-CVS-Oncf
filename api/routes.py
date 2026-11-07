from fastapi import APIRouter, HTTPException

from database.database import Database

from pathlib import Path
import json




router = APIRouter(
    prefix="/api",
    tags=["CVS Monitoring"]
)


database = Database()


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
def health():

    return {
        "status": "OK",
        "service": "CVS Monitoring API"
    }


# =========================================================
# DERNIERE MESURE
# =========================================================

@router.get("/measurements/latest")
def latest_measurement():

    measurements = database.get_measurements(1)

    if not measurements:

        raise HTTPException(
            status_code=404,
            detail="Aucune mesure disponible"
        )

    row = measurements[0]

    return format_measurement(row)


# =========================================================
# HISTORIQUE DES MESURES
# =========================================================

@router.get("/measurements")
def get_measurements(
    limit: int = 50
):

    if limit < 1 or limit > 1000:

        raise HTTPException(
            status_code=400,
            detail="limit doit être compris entre 1 et 1000"
        )

    measurements = database.get_measurements(
        limit
    )

    return [
        format_measurement(row)
        for row in measurements
    ]


# =========================================================
# ALARMES
# =========================================================

@router.get("/alarms")
def get_alarms(
    limit: int = 50
):

    if limit < 1 or limit > 1000:

        raise HTTPException(
            status_code=400,
            detail="limit doit être compris entre 1 et 1000"
        )

    alarms = database.get_alarms(
        limit
    )

    return [
        format_alarm(row)
        for row in alarms
    ]


# =========================================================
# DERNIERE ALARME
# =========================================================

@router.get("/alarms/latest")
def latest_alarm():

    alarms = database.get_alarms(1)

    if not alarms:

        raise HTTPException(
            status_code=404,
            detail="Aucune alarme disponible"
        )

    return format_alarm(
        alarms[0]
    )


# =========================================================
# STATISTIQUES
# =========================================================

@router.get("/statistics")
def statistics():

    measurements = database.get_measurements(
        1000
    )

    alarms = database.get_alarms(
        1000
    )

    if not measurements:

        return {
            "measurements_count": 0,
            "alarms_count": len(alarms),
            "critical_alarms": 0,
            "warning_alarms": 0
        }

    critical = sum(
        1
        for alarm in alarms
        if alarm[4] == "CRITICAL"
    )

    warning = sum(
        1
        for alarm in alarms
        if alarm[4] == "WARNING"
    )

    return {

        "measurements_count":
            len(measurements),

        "alarms_count":
            len(alarms),

        "critical_alarms":
            critical,

        "warning_alarms":
            warning
    }


# =========================================================
# SIMULATION DES PANNES
# =========================================================




SIMULATION_FILE = Path(
    "config/simulation_state.json"
)


SCENARIOS = {

    "normal":
        "Fonctionnement normal",

    "overtemperature":
        "Surchauffe IGBT",

    "overcurrent":
        "Surintensité",

    "overvoltage":
        "Surtension entrée",

    "low_output_voltage":
        "Sous-tension sortie",

    "high_vibration":
        "Vibration élevée",

    "fan_failure":
        "Défaut ventilation",

    "low_efficiency":
        "Rendement faible",

    "combined":
        "Panne combinée"
}


@router.get("/simulation/scenarios")
def get_scenarios():

    return SCENARIOS


@router.get("/simulation/scenario")
def get_current_scenario():

    try:

        if not SIMULATION_FILE.exists():

            SIMULATION_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            SIMULATION_FILE.write_text(
                json.dumps({
                    "scenario": "normal"
                }),
                encoding="utf-8"
            )

        data = json.loads(
            SIMULATION_FILE.read_text(
                encoding="utf-8"
            )
        )

        scenario = data.get(
            "scenario",
            "normal"
        )

        return {
            "scenario": scenario,
            "description":
                SCENARIOS.get(
                    scenario,
                    "Inconnu"
                )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/simulation/scenario/{scenario}")
def set_scenario(
    scenario: str
):

    if scenario not in SCENARIOS:

        raise HTTPException(
            status_code=400,
            detail="Scénario inconnu"
        )

    try:

        SIMULATION_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        SIMULATION_FILE.write_text(
            json.dumps({
                "scenario": scenario
            }),
            encoding="utf-8"
        )

        return {

            "success": True,

            "scenario":
                scenario,

            "description":
                SCENARIOS[scenario]
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# FONCTIONS DE FORMATAGE
# =========================================================

def format_measurement(row):

    return {

        "id": row[0],

        "timestamp": row[1],

        "voltage": row[2],

        "output_voltage": row[3],

        "current": row[4],

        "power": row[5],

        "temperature": row[6],

        "internal_temperature": row[7],

        "vibration": row[8],

        "fan": bool(row[9]),

        "battery": row[10],

        "efficiency": row[11],

        "protection_active":
            bool(row[12]),

        "status": row[13]
    }


def format_alarm(row):

    return {

        "id": row[0],

        "timestamp": row[1],

        "code": row[2],

        "type": row[3],

        "severity": row[4],

        "message": row[5],

        "value": row[6]
    }