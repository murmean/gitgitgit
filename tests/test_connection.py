from src.ws_client import KrakenWS
import pytest


@pytest.fixture
def connected_client():
    client = KrakenWS()
    client.connect()

    yield client

    client.close_connection()


def test_heartbeat_messages_are_received(connected_client):
    connected_client.subscribe(
        "ticker",
        "BTC/USD"
    )

    heartbeat = connected_client.receive_message(
        "channel",
        "heartbeat"
    )

    assert heartbeat["channel"] == "heartbeat"


def test_connection_opens(connected_client):
    assert connected_client.ws is not None
    assert connected_client.ws.connected is True


def test_reconnect_recovers_stream(connected_client):
    connected_client.subscribe("ticker", "BTC/USD")

    first = connected_client.receive_message("channel", "ticker")
    assert first["channel"] == "ticker"

    connected_client.close_connection()

    connected_client.connect()

    connected_client.subscribe("ticker", "BTC/USD")

    second = connected_client.receive_message("channel", "ticker")

    assert second["channel"] == "ticker"


def test_multi_channel_subscription_receives_messages(connected_client):
    connected_client.subscribe("ticker", "BTC/USD")
    connected_client.subscribe("trade", "BTC/USD")
    ticker_message = connected_client.receive_message(
        "channel",
        "ticker"
    )
    trade_message = connected_client.receive_message(
        "channel",
        "trade"
    )

    assert ticker_message["channel"] == "ticker"
    assert trade_message["channel"] == "trade"
