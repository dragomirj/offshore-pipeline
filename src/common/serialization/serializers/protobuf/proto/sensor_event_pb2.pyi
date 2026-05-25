from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Location(_message.Message):
    __slots__ = ("lat", "lon")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("device_id", "sensor_id", "firmware_version", "location")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    sensor_id: str
    firmware_version: str
    location: Location
    def __init__(self, device_id: _Optional[str] = ..., sensor_id: _Optional[str] = ..., firmware_version: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ...) -> None: ...

class Trace(_message.Message):
    __slots__ = ("event_id", "trace_id", "span_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    trace_id: str
    span_id: str
    def __init__(self, event_id: _Optional[str] = ..., trace_id: _Optional[str] = ..., span_id: _Optional[str] = ...) -> None: ...

class ChannelMetadata(_message.Message):
    __slots__ = ("spiking", "alert_threshold")
    SPIKING_FIELD_NUMBER: _ClassVar[int]
    ALERT_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    spiking: bool
    alert_threshold: float
    def __init__(self, spiking: bool = ..., alert_threshold: _Optional[float] = ...) -> None: ...

class SimulationInfo(_message.Message):
    __slots__ = ("simulation_type",)
    SIMULATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    simulation_type: str
    def __init__(self, simulation_type: _Optional[str] = ...) -> None: ...

class SensorEvent(_message.Message):
    __slots__ = ("occurred_at", "ingested_at", "device", "data", "channels", "trace", "tags", "simulation")
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class ChannelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ChannelMetadata
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ChannelMetadata, _Mapping]] = ...) -> None: ...
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    INGESTED_AT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_FIELD_NUMBER: _ClassVar[int]
    occurred_at: int
    ingested_at: int
    device: Device
    data: _containers.ScalarMap[str, float]
    channels: _containers.MessageMap[str, ChannelMetadata]
    trace: Trace
    tags: _containers.RepeatedScalarFieldContainer[str]
    simulation: SimulationInfo
    def __init__(self, occurred_at: _Optional[int] = ..., ingested_at: _Optional[int] = ..., device: _Optional[_Union[Device, _Mapping]] = ..., data: _Optional[_Mapping[str, float]] = ..., channels: _Optional[_Mapping[str, ChannelMetadata]] = ..., trace: _Optional[_Union[Trace, _Mapping]] = ..., tags: _Optional[_Iterable[str]] = ..., simulation: _Optional[_Union[SimulationInfo, _Mapping]] = ...) -> None: ...
