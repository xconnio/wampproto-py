from __future__ import annotations

from typing import Any

from wampproto.messages import util, exceptions
from wampproto.messages.message import Message


class Welcome(Message):
    TEXT = "WELCOME"
    TYPE = 2

    def __init__(
        self,
        session_id: int,
        roles: dict[str, Any],
        authid: str | None = None,
        authrole: str | None = None,
        authmethod: str | None = None,
        authextra: dict[str, Any] | None = None,
    ):
        super().__init__(
            session_id=session_id,
            roles=roles,
            authid=authid,
            authrole=authrole,
            authmethod=authmethod,
            authextra=authextra,
        )

    @staticmethod
    def parse(msg: list[Any]) -> Welcome:
        util.sanity_check(msg, 3, 3, Welcome.TYPE, Welcome.TEXT)

        session_id = util.validate_session_id_or_raise(msg[1], Welcome.TEXT)
        details = util.validate_details_or_raise(msg[2], Welcome.TEXT)

        roles = details.get("roles", {})
        if not isinstance(roles, dict):
            raise exceptions.ProtocolError(f"invalid type for 'roles' in details for {Welcome.TEXT}")

        if len(roles) == 0:
            raise exceptions.ProtocolError(f"roles are missing in details for {Welcome.TEXT}")

        # for role in roles.keys():
        #     if role not in util.AllowedRoles.__members__.values():
        #         raise exceptions.ProtocolError(f"invalid role '{role}' in 'roles' details for {Welcome.WELCOME_TEXT}")

        authid = details.get("authid", None)
        if authid is not None:
            if not isinstance(authid, str):
                raise exceptions.ProtocolError(f"authid must be a type string for {Welcome.TEXT}")

        authrole = details.get("authrole", None)
        if authrole is not None:
            if not isinstance(authrole, str):
                raise exceptions.ProtocolError(f"authrole must be a type string for {Welcome.TEXT}")

        authmethod = details.get("authmethod", None)
        if authmethod is not None:
            if not isinstance(authmethod, str):
                raise exceptions.InvalidTypeError(str, type(authmethod), "authmethod", Welcome.TEXT)

        authextra = details.get("authextra", None)
        if authextra is not None:
            if not isinstance(authextra, dict):
                raise exceptions.InvalidTypeError(dict, type(authextra), "authextra", Welcome.TEXT)

        return Welcome(
            session_id=session_id,
            roles=roles,
            authid=authid,
            authrole=authrole,
            authmethod=authmethod,
            authextra=authextra,
        )

    def marshal(self) -> list[Any]:
        details: dict[str, Any] = {"roles": self.roles}

        if self.authid is not None:
            details["authid"] = self.authid

        if self.authrole is not None:
            details["authrole"] = self.authrole

        if self.authmethod is not None:
            details["authmethod"] = self.authmethod

        if self.authextra is not None:
            details["authextra"] = self.authextra

        return [self.TYPE, self.session_id, details]
