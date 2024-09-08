from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CustomerPOSTRequestBody(_message.Message):
    __slots__ = ("name", "phone_no")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NO_FIELD_NUMBER: _ClassVar[int]
    name: str
    phone_no: str
    def __init__(
        self, name: _Optional[str] = ..., phone_no: _Optional[str] = ...
    ) -> None: ...

class TokenData(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class CustomerRequest(_message.Message):
    __slots__ = ("customer", "token_data")
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_DATA_FIELD_NUMBER: _ClassVar[int]
    customer: CustomerPOSTRequestBody
    token_data: TokenData
    def __init__(
        self,
        customer: _Optional[_Union[CustomerPOSTRequestBody, _Mapping]] = ...,
        token_data: _Optional[_Union[TokenData, _Mapping]] = ...,
    ) -> None: ...

class CustomerResponse(_message.Message):
    __slots__ = ("id", "name", "phone_no", "coffee_shop_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NO_FIELD_NUMBER: _ClassVar[int]
    COFFEE_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    phone_no: str
    coffee_shop_id: int
    def __init__(
        self,
        id: _Optional[int] = ...,
        name: _Optional[str] = ...,
        phone_no: _Optional[str] = ...,
        coffee_shop_id: _Optional[int] = ...,
    ) -> None: ...

class CustomerResponseWrapper(_message.Message):
    __slots__ = ("customer", "status_code")
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    customer: CustomerResponse
    status_code: int
    def __init__(
        self,
        customer: _Optional[_Union[CustomerResponse, _Mapping]] = ...,
        status_code: _Optional[int] = ...,
    ) -> None: ...
