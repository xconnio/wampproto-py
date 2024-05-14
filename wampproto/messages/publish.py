from __future__ import annotations

from typing import Any

from wampproto.messages.message import Message
from wampproto.messages import util


class Publish(Message):
    TEXT = "PUBLISH"
    TYPE = 16

    def __init__(
        self,
        request_id: int,
        uri: str,
        args: list | None = None,
        kwargs: dict | None = None,
        options: dict | None = None,
    ):
        super().__init__(request_id=request_id, options=options, uri=uri, args=args, kwargs=kwargs)

    @staticmethod
    def parse(msg: list[Any]) -> Publish:
        util.sanity_check(msg, 4, 6, Publish.TYPE, Publish.TEXT)

        request_id = util.validate_session_id_or_raise(msg[1], Publish.TEXT, "request ID")
        options = util.validate_details_or_raise(msg[2], Publish.TEXT, "options")
        uri = util.validate_uri_or_raise(msg[3], Publish.TEXT)

        args = []
        if len(msg) > 4:
            args = msg[4]

        kwargs = {}
        if len(msg) > 5:
            kwargs = msg[5]

        return Publish(request_id, uri, args, kwargs, options)

    def marshal(self) -> list[Any]:
        message = [Publish.TYPE, self.request_id, self.options, self.uri]
        if self.args is not None:
            message.append(self.args)

        if self.kwargs is not None:
            if self.args is None:
                message.append([])

            message.append(self.kwargs)

        return message
