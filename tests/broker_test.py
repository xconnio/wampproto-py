import pytest

from wampproto import messages
from wampproto.broker import Broker
from wampproto.types import MessageWithRecipient


def test_add_and_remove_session():
    broker = Broker()
    session_id = 1
    broker.add_session(session_id)

    # Adding duplicate session should throw an exception
    with pytest.raises(ValueError) as exc:
        broker.add_session(session_id)

    assert str(exc.value) == "cannot add session twice"

    broker.remove_session(session_id)

    # Removing non-existing session should throw an exception
    with pytest.raises(ValueError) as exc:
        broker.remove_session(3)

    assert str(exc.value) == "cannot remove non-existing session"


def test_subscribing_to_topic():
    broker = Broker()
    session_id = 1
    topic_name = "io.xconn.test"
    broker.add_session(session_id)

    subscribe = messages.Subscribe(1, topic_name)
    message_with_recipient = broker.receive_message(session_id, subscribe)

    assert message_with_recipient.recipient == session_id
    assert isinstance(message_with_recipient.message, messages.Subscribed)

    # Check subscription by topic
    has_subscription = broker.has_subscription(topic_name)
    assert has_subscription

    # Subscribe with invalid sessionID
    with pytest.raises(ValueError) as exc:
        broker.receive_message(3, subscribe)

    assert str(exc.value) == f"cannot subscribe, session 3 doesn't exist"


def test_unsubscribing_from_topic():
    broker = Broker()
    topic_name = "io.xconn.test"
    session_id = 1
    broker.add_session(session_id)

    subscribe = messages.Subscribe(1, topic_name)
    broker.receive_message(session_id, subscribe)

    unsubscribe = messages.UnSubscribe(1, 1)
    message_with_recipient = broker.receive_message(session_id, unsubscribe)

    assert message_with_recipient.recipient == 1
    assert isinstance(message_with_recipient.message, messages.UnSubscribed)

    # Check subscription by topic
    has_subscription = broker.has_subscription(topic_name)
    assert not has_subscription

    # Unsubscribe with invalid sessionID
    with pytest.raises(ValueError) as exc:
        broker.receive_message(2, unsubscribe)

    assert str(exc.value) == f"cannot unsubscribe, session 2 doesn't exist"

    # Unsubscribe with invalid subscriptionID
    invalid_unsubscribe = messages.UnSubscribe(1, 2)
    with pytest.raises(ValueError) as exc:
        broker.receive_message(1, invalid_unsubscribe)

    assert str(exc.value) == f"cannot unsubscribe, subscription {invalid_unsubscribe.subscription_id} doesn't exist"

    # Unsubscribe with non-existing subscriptionID
    with pytest.raises(ValueError) as exc:
        broker.receive_message(1, invalid_unsubscribe)

    assert str(exc.value) == "cannot unsubscribe, subscription 2 doesn't exist"


def test_receive_invalid_message():
    broker = Broker()
    call = messages.Call(1, "io.xconn.test")

    with pytest.raises(Exception) as exc:
        broker.receive_message(1, call)

    assert str(exc.value) == "message type not supported"


def test_publishing_to_topic():
    broker = Broker()
    topic_name = "io.xconn.test"
    broker.add_session(1)

    subscribe = messages.Subscribe(1, topic_name)
    broker.receive_message(1, subscribe)

    publish = messages.Publish(1, topic_name, args=[1, 2, 3])
    messages_with_recipient = broker.receive_publish(1, publish)

    assert len(messages_with_recipient.recipients) == 1
    assert isinstance(messages_with_recipient.event, messages.Event)
    assert messages_with_recipient.ack is None

    # Publish message to a topic with no subscribers
    publish_no_subscriber = messages.Publish(2, "topic1", args=[1, 2, 3])
    msgs = broker.receive_publish(1, publish_no_subscriber)

    assert len(msgs.recipients) == 0
    assert msgs.event is None
    assert msgs.ack is None

    # Publish with acknowledge true
    publish_acknowledge = messages.Publish(2, topic_name, args=[1, 2, 3], options={"acknowledge": True})
    msg_with_recipient = broker.receive_publish(1, publish_acknowledge)

    assert len(msg_with_recipient.recipients) == 1
    assert isinstance(msg_with_recipient.event, messages.Event)
    assert isinstance(msg_with_recipient.ack, MessageWithRecipient)

    # Publish message to invalid sessionID
    with pytest.raises(Exception) as exc:
        broker.receive_publish(5, publish)

    assert str(exc.value) == "cannot publish, session 5 doesn't exist"
