from __future__ import annotations

from typing import Any

from wamp.messages import error, util
from wamp.messages.message import Message


class Abort(Message):
    ABORT_TEXT = "ABORT"
    MESSAGE_TYPE = 3

    def __init__(self, details: dict, reason: str):
        super().__init__()
        self.details = details
        self.reason = reason

    @staticmethod
    def parse(msg: list[Any]) -> Abort:
        util.sanity_check(msg, 3, 3, Abort.MESSAGE_TYPE, Abort.ABORT_TEXT)

        details = util.validate_details_or_raise(msg[1], Abort.ABORT_TEXT)

        reason = util.validate_uri_or_raise(msg[2], Abort.ABORT_TEXT)

        return Abort(details, reason)

    def marshal(self) -> list[Any]:
        return [Abort.MESSAGE_TYPE, self.details, self.reason]
