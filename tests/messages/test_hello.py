import pytest

from wamp.messages import error, util
from wamp.messages.hello import Hello


def test_marshal_with_no_roles_and_details():
    realm = "realm"
    roles = {}
    details = {}
    message = Hello(realm, roles, **details).marshal()

    assert isinstance(message, list)
    assert len(message) == 3

    assert isinstance(message[0], int)
    assert message[0] == Hello.MESSAGE_TYPE

    assert isinstance(message[1], str)
    assert message[1] == realm

    assert isinstance(message[2], dict)
    assert message[2] == {"roles": {}}


def test_marshal_with_role_and_no_details():
    realm = "realm"
    roles = {"callee": {}}
    details = {}
    message = Hello(realm, roles, **details).marshal()

    assert isinstance(message, list)
    assert len(message) == 3

    assert isinstance(message[0], int)
    assert message[0] == Hello.MESSAGE_TYPE

    assert isinstance(message[1], str)
    assert message[1] == realm

    assert isinstance(message[2], dict)
    assert message[2] == {"roles": roles}


def test_marshal_with_authid():
    realm = "realm"
    roles = {"callee": {}}
    details = {"authid": "mahad"}
    message = Hello(realm, roles, **details).marshal()

    assert isinstance(message, list)
    assert len(message) == 3

    assert isinstance(message[0], int)
    assert message[0] == Hello.MESSAGE_TYPE

    assert isinstance(message[1], str)
    assert message[1] == realm

    assert isinstance(message[2], dict)
    assert message[2] == {"roles": roles, "authid": "mahad"}


def test_marshal_with_authrole():
    realm = "realm"
    roles = {"callee": {}}
    details = {"authrole": "admin"}
    message = Hello(realm, roles, **details).marshal()

    assert isinstance(message, list)
    assert len(message) == 3

    assert isinstance(message[0], int)
    assert message[0] == Hello.MESSAGE_TYPE

    assert isinstance(message[1], str)
    assert message[1] == realm

    assert isinstance(message[2], dict)
    assert message[2] == {"roles": roles, "authrole": "admin"}


def test_marshal_with_role_authid_and_authrole():
    realm = "realm"
    roles = {"callee": {}}
    details = {"authid": "mahad", "authrole": "admin"}
    message = Hello(realm, roles, **details).marshal()

    assert isinstance(message, list)
    assert len(message) == 3

    assert isinstance(message[0], int)
    assert message[0] == Hello.MESSAGE_TYPE

    assert isinstance(message[1], str)
    assert message[1] == realm

    assert isinstance(message[2], dict)
    assert message[2] == {"roles": roles, "authid": "mahad", "authrole": "admin"}


def test_parse_with_string():
    message = "msg"
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert (
        str(exc_info.value) == f"invalid message type '{type(message)}' for {Hello.HELLO_TEXT}, type should be a list"
    )


def test_parse_with_invalid_list_length():
    message = [1]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert (
        str(exc_info.value)
        == f"invalid message length '{len(message)}' for {Hello.HELLO_TEXT}, length should be equal to three"
    )


def test_parse_with_invalid_message_type():
    message = [2, "realm", {}]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"invalid message type for {Hello.HELLO_TEXT}"


def test_parse_with_realm_none():
    message = [1, None, {}]
    with pytest.raises(error.InvalidRealmError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"realm cannot be null for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_realm_type():
    message = [1, {"realm": "realm1"}, {}]
    with pytest.raises(error.InvalidRealmError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"realm must be of type string for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_details_type():
    message = [1, "realm1", "details"]
    with pytest.raises(error.InvalidDetailsError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"details must be of type dictionary for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_details_dict_key():
    message = [1, "realm1", {1: "v"}]
    with pytest.raises(error.InvalidDetailsError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"invalid type for key '1' in extra details for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_role_type():
    message = [1, "realm1", {"roles": "new_role"}]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"invalid type for 'roles' in details for {Hello.HELLO_TEXT}"


def test_parse_with_empty_role():
    message = [1, "realm1", {"roles": {}}]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"roles are missing in details for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_role_key():
    message = [1, "realm1", {"roles": {"new_role": {}}}]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"invalid role 'new_role' in 'roles' details for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_authid():
    message = [1, "realm1", {"roles": {"callee": {}}, "authid": []}]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"authid must be a type string for {Hello.HELLO_TEXT}"


def test_parse_with_invalid_authrole():
    message = [1, "realm1", {"roles": {"callee": {}}, "authrole": []}]
    with pytest.raises(error.ProtocolError) as exc_info:
        Hello.parse(message)

    assert str(exc_info.value) == f"authrole must be a type string for {Hello.HELLO_TEXT}"


def test_parse_with_valid_roles():
    realm = "realm1"
    for role in util.AllowedRoles.get_allowed_roles():
        details = {"roles": {role: {}}}
        hello = Hello.parse([Hello.MESSAGE_TYPE, realm, details])

        assert isinstance(hello, Hello)
        assert isinstance(hello.realm, str)
        assert hello.realm == realm

        assert isinstance(hello.roles, dict)
        assert hello.roles == details["roles"]

        assert hello.authid is None
        assert hello.authrole is None


def test_parse_with_multiple_roles():
    realm = "realm1"
    details = {"roles": {"callee": {}, "caller": {}}}
    hello = Hello.parse([Hello.MESSAGE_TYPE, realm, details])

    assert isinstance(hello, Hello)
    assert isinstance(hello.realm, str)
    assert hello.realm == realm

    assert isinstance(hello.roles, dict)
    assert hello.roles == details["roles"]

    assert hello.authid is None
    assert hello.authrole is None


def test_parse_with_authid():
    realm = "realm1"
    details = {"roles": {"callee": {}}, "authid": "mahad"}
    hello = Hello.parse([Hello.MESSAGE_TYPE, realm, details])

    assert isinstance(hello, Hello)
    assert isinstance(hello.realm, str)
    assert hello.realm == realm

    assert isinstance(hello.roles, dict)
    assert hello.roles == details["roles"]

    assert isinstance(hello.authid, str)
    assert hello.authid == details["authid"]
    assert hello.authrole is None


def test_parse_with_authrole():
    realm = "realm1"
    details = {"roles": {"callee": {}}, "authrole": "admin"}
    hello = Hello.parse([Hello.MESSAGE_TYPE, realm, details])

    assert isinstance(hello, Hello)
    assert isinstance(hello.realm, str)
    assert hello.realm == realm

    assert isinstance(hello.roles, dict)
    assert hello.roles == details["roles"]

    assert isinstance(hello.authrole, str)
    assert hello.authrole == details["authrole"]
    assert hello.authid is None


def test_parse_with_authid_and_authrole():
    realm = "realm1"
    details = {"roles": {"callee": {}}, "authid": "mahad", "authrole": "admin"}
    hello = Hello.parse([Hello.MESSAGE_TYPE, realm, details])

    assert isinstance(hello, Hello)
    assert isinstance(hello.realm, str)
    assert hello.realm == realm

    assert isinstance(hello.roles, dict)
    assert hello.roles == details["roles"]

    assert isinstance(hello.authid, str)
    assert hello.authid == details["authid"]

    assert isinstance(hello.authrole, str)
    assert hello.authrole == details["authrole"]
