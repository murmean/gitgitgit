import datetime

from src.ws_client import KrakenWS
import pytest

@pytest.fixture
def trade_message():
    client = KrakenWS()
    client.connect()
    client.subscribe(channel="trade", symbol="BTC/USD")
    output = client.receive_message("channel", "trade")
    client.close_connection()
    return output

@pytest.fixture
def trade_messages():
    client = KrakenWS()
    client.connect()
    client.subscribe(channel="trade", symbol="BTC/USD")
    output = client.load_multiple_messages()
    client.close_connection()
    return [msg for msg in output if msg["channel"] == "trade"]

def test_trade_subscribe(trade_message):

    assert trade_message["channel"] == "trade"
    assert trade_message["type"] == "update"

def test_trade_data_contains_expected_fields(trade_message):
    data = trade_message["data"][0]
    assert data["symbol"] == "BTC/USD"
    assert data["side"] in ["buy", "sell"]
    assert data["price"] > 0
    assert data["qty"] > 0
    assert data["ord_type"] == "limit"
    assert data["trade_id"] > 0
    assert data["timestamp"]

def test_trade_timestamps_increase(trade_messages):
    timestamps = []
    for message in trade_messages:
        trade = message["data"][0]

        timestamps.append(datetime.fromisoformat(trade["timestamp"].replace("Z", "+00:00")))

    assert len(timestamps) > 1
    assert timestamps == sorted(timestamps)