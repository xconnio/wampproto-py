from __future__ import annotations

from wamp.messages import error, util
from wamp.messages.message import Message


class Authenticate(Message):
    AUTHENTICATE_TEXT = "CHALLENGE"
    MESSAGE_TYPE = 5

    def __init__(self, signature: str, extra: dict | None = None):
        super().__init__()
        self.signature = signature
        self.extra = {} if extra is None else extra

    @staticmethod
    def parse(msg: list) -> Authenticate:
        util.validate_message_or_raise(msg, Authenticate.AUTHENTICATE_TEXT)

        if msg[0] != Authenticate.MESSAGE_TYPE:
            raise error.ProtocolError(f"invalid message type for {Authenticate.AUTHENTICATE_TEXT}")

        signature = msg[1]
        if not isinstance(signature, str):
            raise error.ProtocolError(
                f"invalid type {type(signature)} for 'signature' in {Authenticate.AUTHENTICATE_TEXT}"
            )

        extra = util.validate_details_or_raise(msg[2], Authenticate.AUTHENTICATE_TEXT)

        return Authenticate(signature, extra)

    def marshal(self):
        return [Authenticate.MESSAGE_TYPE, self.signature, self.extra]
