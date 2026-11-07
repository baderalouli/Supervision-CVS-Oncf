import random
from dataclasses import dataclass


@dataclass
class CVSData:

    timestamp: str
    input_voltage: float
    output_voltage: float
    current: float
    power: float
    igbt_temperature: float
    internal_temperature: float
    vibration: float
    fan: bool
    battery: float
    efficiency: float
    load: float


class CVSModel:

    def __init__(self):

        self.protection_active = False

        self.input_voltage = 3000.0
        self.output_voltage = 400.0

        self.current = 80.0

        self.igbt_temperature = 45.0
        self.internal_temperature = 35.0

        self.vibration = 0.8

        self.fan = True

        self.battery = 98.0

        self.efficiency = 94.0

        self.load = 0.5

    # ==================================================
    # UPDATE PRINCIPAL
    # ==================================================

    def update(self, scenario="normal"):

        if scenario == "normal":

            self._normal_mode()

        elif scenario == "overtemperature":

            self._overtemperature_mode()

        elif scenario == "overcurrent":

            self._overcurrent_mode()

        elif scenario == "overvoltage":

            self._overvoltage_mode()

        elif scenario == "low_output_voltage":

            self._low_output_voltage_mode()

        elif scenario == "high_vibration":

            self._high_vibration_mode()

        elif scenario == "fan_failure":

            self._fan_failure_mode()

        elif scenario == "low_efficiency":

            self._low_efficiency_mode()

        elif scenario == "combined":

            self._combined_mode()

        else:

            self._normal_mode()

        # ==============================================
        # PROTECTION
        # ==============================================

        self.protection_active = (

            self.igbt_temperature >= 100
            or self.current > 100
            or self.input_voltage > 3300
            or self.output_voltage < 350
        )

        # ==============================================
        # PUISSANCE
        # ==============================================

        self.power = (
            self.output_voltage *
            self.current
        )

        return {

            "input_voltage":
                round(
                    self.input_voltage,
                    2
                ),

            "output_voltage":
                round(
                    self.output_voltage,
                    2
                ),

            "current":
                round(
                    self.current,
                    2
                ),

            "power":
                round(
                    self.power,
                    2
                ),

            "igbt_temperature":
                round(
                    self.igbt_temperature,
                    2
                ),

            "internal_temperature":
                round(
                    self.internal_temperature,
                    2
                ),

            "vibration":
                round(
                    self.vibration,
                    2
                ),

            "fan":
                self.fan,

            "battery":
                round(
                    self.battery,
                    2
                ),

            "efficiency":
                round(
                    self.efficiency,
                    2
                ),

            "load":
                round(
                    self.load,
                    2
                ),

            "protection_active":
                self.protection_active
        }

    # ==================================================
    # MODE NORMAL
    # ==================================================

    def _normal_mode(self):

        self.load = random.uniform(
            0.4,
            0.7
        )

        self.current = random.uniform(
            70,
            85
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            395,
            405
        )

        self.igbt_temperature += (
            (
                random.uniform(
                    50,
                    65
                )
                -
                self.igbt_temperature
            )
            * 0.15
        )

        self.internal_temperature = (
            self.igbt_temperature - 10
        )

        self.vibration = random.uniform(
            0.5,
            1.5
        )

        self.fan = True

        self.battery += 0.01

        if self.battery > 100:

            self.battery = 100

        self.efficiency = random.uniform(
            92,
            96
        )

    # ==================================================
    # SURCHAUFFE IGBT
    # ==================================================

    def _overtemperature_mode(self):

        self.load = random.uniform(
            0.7,
            0.9
        )

        self.current = random.uniform(
            90,
            100
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            395,
            405
        )

        self.igbt_temperature = random.uniform(
            102,
            115
        )

        self.internal_temperature = (
            self.igbt_temperature + 8
        )

        self.vibration = random.uniform(
            1.0,
            2.5
        )

        self.fan = True

        self.efficiency = random.uniform(
            85,
            90
        )

    # ==================================================
    # SURINTENSITE
    # ==================================================

    def _overcurrent_mode(self):

        self.load = random.uniform(
            0.9,
            1.1
        )

        self.current = random.uniform(
            105,
            125
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            395,
            405
        )

        self.igbt_temperature = random.uniform(
            85,
            100
        )

        self.internal_temperature = (
            self.igbt_temperature + 8
        )

        self.vibration = random.uniform(
            1.0,
            2.5
        )

        self.fan = True

        self.efficiency = random.uniform(
            85,
            90
        )

    # ==================================================
    # SURTENSION ENTREE
    # ==================================================

    def _overvoltage_mode(self):

        self.load = random.uniform(
            0.5,
            0.8
        )

        self.current = random.uniform(
            70,
            95
        )

        self.input_voltage = random.uniform(
            3350,
            3500
        )

        self.output_voltage = random.uniform(
            410,
            425
        )

        self.igbt_temperature = random.uniform(
            60,
            75
        )

        self.internal_temperature = (
            self.igbt_temperature + 8
        )

        self.vibration = random.uniform(
            0.5,
            2.0
        )

        self.fan = True

        self.efficiency = random.uniform(
            90,
            94
        )

    # ==================================================
    # SOUS-TENSION SORTIE
    # ==================================================

    def _low_output_voltage_mode(self):

        self.load = random.uniform(
            0.6,
            0.8
        )

        self.current = random.uniform(
            80,
            100
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            320,
            345
        )

        self.igbt_temperature = random.uniform(
            60,
            75
        )

        self.internal_temperature = (
            self.igbt_temperature + 8
        )

        self.vibration = random.uniform(
            1.0,
            2.0
        )

        self.fan = True

        self.efficiency = random.uniform(
            88,
            93
        )

    # ==================================================
    # VIBRATION ELEVEE
    # ==================================================

    def _high_vibration_mode(self):

        self.load = random.uniform(
            0.5,
            0.8
        )

        self.current = random.uniform(
            80,
            100
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            395,
            405
        )

        self.igbt_temperature = random.uniform(
            55,
            70
        )

        self.internal_temperature = (
            self.igbt_temperature + 8
        )

        self.vibration = random.uniform(
            5.0,
            7.0
        )

        self.fan = True

        self.efficiency = random.uniform(
            90,
            94
        )

    # ==================================================
    # DEFAUT VENTILATION
    # ==================================================

    def _fan_failure_mode(self):

        self.load = random.uniform(
            0.6,
            0.8
        )

        self.current = random.uniform(
            85,
            100
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            395,
            405
        )

        self.fan = False

        self.igbt_temperature = random.uniform(
            88,
            108
        )

        self.internal_temperature = (
            self.igbt_temperature + 10
        )

        self.vibration = random.uniform(
            1.0,
            2.5
        )

        self.efficiency = random.uniform(
            85,
            92
        )

    # ==================================================
    # RENDEMENT FAIBLE
    # ==================================================

    def _low_efficiency_mode(self):

        self.load = random.uniform(
            0.7,
            0.9
        )

        self.current = random.uniform(
            90,
            110
        )

        self.input_voltage = random.uniform(
            2950,
            3150
        )

        self.output_voltage = random.uniform(
            390,
            405
        )

        self.igbt_temperature = random.uniform(
            75,
            95
        )

        self.internal_temperature = (
            self.igbt_temperature + 8
        )

        self.vibration = random.uniform(
            1.0,
            2.5
        )

        self.fan = True

        self.efficiency = random.uniform(
            78,
            88
        )

    # ==================================================
    # PANNE COMBINEE
    # ==================================================

    def _combined_mode(self):

        self.load = random.uniform(
            0.9,
            1.1
        )

        self.current = random.uniform(
            105,
            125
        )

        self.input_voltage = random.uniform(
            3350,
            3500
        )

        self.output_voltage = random.uniform(
            320,
            345
        )

        self.igbt_temperature = random.uniform(
            103,
            118
        )

        self.internal_temperature = (
            self.igbt_temperature + 10
        )

        self.vibration = random.uniform(
            5.0,
            7.0
        )

        self.fan = False

        self.battery = random.uniform(
            90,
            98
        )

        self.efficiency = random.uniform(
            78,
            85
        )