from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CategoryPrediction(_message.Message):
    __slots__ = ["category", "prediction"]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_FIELD_NUMBER: _ClassVar[int]
    category: str
    prediction: float
    def __init__(self, category: _Optional[str] = ..., prediction: _Optional[float] = ...) -> None: ...
