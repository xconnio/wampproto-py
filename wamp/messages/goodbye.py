from __future__ import annotations

from wamp.messages import error, util
from wamp.messages.message import Message


class Goodbye(Message):
    GOODBYE_TEXT = "GOODBYE"
    MESSAGE_TYPE = 6

    def __init__(self, details: dict, reason: str):
        super().__init__()
        self.details = details
        self.reason = reason

    @staticmethod
    def parse(msg: list) -> Goodbye:
        util.validate_message_or_raise(msg, Goodbye.GOODBYE_TEXT)

        if msg[0] != Goodbye.MESSAGE_TYPE:
            raise error.ProtocolError(f"invalid message type for {Goodbye.GOODBYE_TEXT}")

        details = util.validate_details_or_raise(msg[1], Goodbye.GOODBYE_TEXT)

        reason = util.validate_uri_or_raise(msg[2], Goodbye.GOODBYE_TEXT)

        return Goodbye(details, reason)

    def marshal(self):
        return [Goodbye.MESSAGE_TYPE, self.details, self.reason]
