from pydantic import BaseModel
from typing import Optional


class Measurement(BaseModel):

    id: int

    timestamp: str

    voltage: float

    output_voltage: float

    current: float

    power: float

    temperature: float

    internal_temperature: float

    vibration: float

    fan: bool

    battery: float

    efficiency: float

    protection_active: bool

    status: str


class Alarm(BaseModel):

    id: int

    timestamp: str

    code: str

    type: str

    severity: str

    message: str

    value: float


class SystemStatus(BaseModel):

    status: str

    temperature: Optional[float] = None

    efficiency: Optional[float] = None

    vibration: Optional[float] = None

    protection_active: Optional[bool] = None