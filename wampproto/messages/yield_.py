from __future__ import annotations

from typing import Any

from wampproto.messages import util, exceptions
from wampproto.messages.message import Message


class Yield(Message):
    TEXT = "YIELD"
    TYPE = 70

    def __init__(
        self,
        request_id: int,
        args: list | None = None,
        kwargs: dict | None = None,
        options: dict | None = None,
    ):
        super().__init__(request_id=request_id, options=options, args=args, kwargs=kwargs)

    @staticmethod
    def parse(msg: list[Any]) -> Yield:
        util.sanity_check(msg, 3, 5, Yield.TYPE, Yield.TEXT)

        request_id = util.validate_session_id_or_raise(msg[1], Yield.TEXT, "request ID")
        options = util.validate_details_or_raise(msg[2], Yield.TEXT, "options")

        args = None
        if len(msg) > 3:
            args = msg[3]
            if not isinstance(args, list):
                raise exceptions.InvalidTypeError(list, type(msg[3]), "args", Yield.TEXT)

        kwargs = None
        if len(msg) > 4:
            kwargs = msg[4]
            if not isinstance(kwargs, dict):
                raise exceptions.InvalidTypeError(dict, type(msg[4]), "kwargs", Yield.TEXT)

        return Yield(request_id, args, kwargs, options)

    def marshal(self) -> list[Any]:
        message = [Yield.TYPE, self.request_id, self.options]
        if self.args is not None:
            message.append(self.args)

        if self.kwargs is not None:
            if self.args is None:
                message.append([])

            message.append(self.kwargs)

        return message
