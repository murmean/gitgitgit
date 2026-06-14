from src.ws_client import KrakenWS


def test_connection_opens():
    client = KrakenWS()
    client.connect()

    assert client.ws is not None
    assert client.ws.connected is True

    client.close_connection()


def test_reconnect_recovers_stream():
    client = KrakenWS()
    client.connect()
    client.subscribe("ticker", "BTC/USD")

    first = client.receive_message("channel", "ticker")
    assert first["channel"] == "ticker"

    client.close_connection()

    client.connect()
    client.subscribe("ticker", "BTC/USD")

    second = client.receive_message("channel", "ticker")
    client.close_connection()

    assert second["channel"] == "ticker"


def test_multi_channel_subscription_receives_messages():
    client = KrakenWS()
    client.connect()

    client.subscribe("ticker", "BTC/USD")
    client.subscribe("trade", "BTC/USD")
    ticker_message = client.receive_message(
        "channel",
        "ticker"
    )
    trade_message = client.receive_message(
        "channel",
        "trade"
    )
    client.close_connection()

    assert ticker_message["channel"] == "ticker"
    assert trade_message["channel"] == "trade"
