import pytest

from src.ws_client import KrakenWS

@pytest.fixture
def ticker_subscribe():
    client = KrakenWS()
    client.connect()
    client.subscribe(channel="ticker", symbol="BTC/USD")
    output = client.receive_message("method", "subscribe")
    client.close_connection()
    return output

@pytest.fixture
def ticker_snapshot():
    client = KrakenWS()
    client.connect()
    client.subscribe(channel="ticker", symbol="BTC/USD")
    output = client.receive_message("channel", "ticker")
    client.close_connection()
    return output

def test_ticker_subscribe(ticker_subscribe):
    assert ticker_subscribe["method"] == "subscribe"
    assert ticker_subscribe["success"] is True

def test_ticker_subscribe_results(ticker_subscribe):
    assert ticker_subscribe["result"]["channel"] == "ticker"
    assert ticker_subscribe["result"]["symbol"] == "BTC/USD"
    assert ticker_subscribe["result"]["event_trigger"] == "trades"

def test_ticker_snapshot(ticker_snapshot):
    assert ticker_snapshot["channel"] == "ticker"
    assert ticker_snapshot["type"] in ["snapshot", "update"]

def test_ticker_snapshot_data(ticker_snapshot):
    data = ticker_snapshot["data"][0]

    assert data["symbol"] == "BTC/USD"
    assert data["bid"] > 0
    assert data["ask"] > 0
    assert data["last"] > 0
    assert data["volume"] >= 0
    assert "timestamp" in data

def test_ticker_bids_not_greater_than_asks(ticker_snapshot):
    data = ticker_snapshot["data"][0]
    assert data["low"] <= data["high"]
    assert data["bid"] <= data["ask"]
    assert data["low"] <= data["last"] <= data["high"]