class FaultInjector:

    SCENARIOS = [
        "normal",
        "overtemperature",
        "overcurrent",
        "overvoltage",
        "low_output_voltage",
        "high_vibration",
        "fan_failure",
        "low_efficiency",
        "combined"
    ]

    @staticmethod
    def is_valid(scenario):
        return scenario in FaultInjector.SCENARIOS

    @staticmethod
    def list_scenarios():
        return FaultInjector.SCENARIOS