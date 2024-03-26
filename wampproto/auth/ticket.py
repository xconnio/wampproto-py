from wampproto import messages, auth


class TicketAuthenticator(auth.IClientAuthenticator):
    TYPE = "ticket"

    def __init__(self, authid: str, ticket: str, auth_extra: dict | None = None):
        super().__init__(TicketAuthenticator.TYPE, authid, auth_extra)
        self._ticket = ticket

    def authenticate(self, challenge: messages.Challenge) -> messages.Authenticate:
        return messages.Authenticate(self._ticket, {})
