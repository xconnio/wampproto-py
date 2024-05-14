from __future__ import annotations

from typing import Any

from wampproto.messages.message import Message
from wampproto.messages import util, exceptions


class Error(Message):
    TEXT = "ERROR"
    TYPE = 8

    def __init__(
        self,
        message_type: int,
        request_id: int,
        uri: str,
        args: list | None = None,
        kwargs: dict | None = None,
        details: dict | None = None,
    ):
        super().__init__(
            message_type=message_type, request_id=request_id, details=details, uri=uri, args=args, kwargs=kwargs
        )

    @staticmethod
    def parse(msg: list[Any]) -> Error:
        util.sanity_check(msg, 5, 7, Error.TYPE, Error.TEXT)

        message_type = util.validate_session_id_or_raise(msg[1], Error.TEXT, "error ID")
        request_id = util.validate_session_id_or_raise(msg[2], Error.TEXT, "request ID")
        details = util.validate_details_or_raise(msg[3], Error.TEXT, "details")
        uri = util.validate_uri_or_raise(msg[4], Error.TEXT)

        args = None
        if len(msg) > 5:
            args = msg[5]
            if not isinstance(args, list):
                raise exceptions.InvalidTypeError(list, type(msg[5]), "args", Error.TEXT)

        kwargs = None
        if len(msg) == 7:
            kwargs = msg[6]
            if not isinstance(kwargs, dict):
                raise exceptions.InvalidTypeError(dict, type(msg[6]), "kwargs", Error.TEXT)

        return Error(message_type, request_id, uri, args, kwargs, details)

    def marshal(self) -> list[Any]:
        message = [Error.TYPE, self.message_type, self.request_id, self.details, self.uri]
        if self.args is not None:
            message.append(self.args)

        if self.kwargs is not None:
            if self.args is None:
                message.append([])

            message.append(self.kwargs)

        return message
