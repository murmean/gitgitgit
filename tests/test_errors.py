from src.ws_client import KrakenWS


def test_invalid_symbol():
    client = KrakenWS()
    client.connect()
    client.subscribe("ticker", "BANANA/USD")
    output = client.receive_message("method", "subscribe")
    client.close_connection()

    assert output["method"] == "subscribe"
    assert output["success"] is False
    assert "error" in output


def test_invalid_channel():
    client = KrakenWS()
    client.connect()
    client.subscribe("BANANA", "BTC/USD")
    output = client.receive_message("method", "subscribe")
    client.close_connection()

    assert output["method"] == "subscribe"
    assert output["success"] is False
    assert "error" in output
