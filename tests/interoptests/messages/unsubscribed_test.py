import pytest

from tests.interoptests.helpers import run_command
from wampproto import messages
from wampproto.serializers import JSONSerializer, CBORSerializer, MsgPackSerializer


def is_equal(msg1: messages.UnSubscribed, msg2: messages.UnSubscribed) -> bool:
    return msg1.request_id == msg2.request_id


@pytest.mark.asyncio
async def test_json_serializer():
    msg = messages.UnSubscribed(messages.UnSubscribedFields(1))
    command = f"wampproto message unsubscribed {msg.request_id} --serializer json"

    output = await run_command(command)

    serializer = JSONSerializer()
    message = serializer.deserialize(output)

    assert is_equal(msg, message)


@pytest.mark.asyncio
async def test_cbor_serializer():
    msg = messages.UnSubscribed(messages.UnSubscribedFields(1))
    command = f"wampproto message unsubscribed {msg.request_id} --serializer cbor --output hex"

    output = await run_command(command)
    output_bytes = bytes.fromhex(output)

    serializer = CBORSerializer()
    message = serializer.deserialize(output_bytes)

    assert is_equal(msg, message)


@pytest.mark.asyncio
async def test_msgpack_serializer():
    msg = messages.UnSubscribed(messages.UnSubscribedFields(1))
    command = f"wampproto message unsubscribed {msg.request_id} --serializer msgpack --output hex"

    output = await run_command(command)
    output_bytes = bytes.fromhex(output)

    serializer = MsgPackSerializer()
    message = serializer.deserialize(output_bytes)

    assert is_equal(msg, message)
