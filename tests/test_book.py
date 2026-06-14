import pytest

from src.ws_client import KrakenWS


@pytest.fixture
def book_message():
    client = KrakenWS()
    client.connect()
    client.subscribe(channel="book", symbol="BTC/USD")
    messages = client.receive_message("channel", "book")
    client.close_connection()
    return messages


def test_subscribe_to_book_channel(book_message):
    assert book_message["channel"] == "book"


def test_book_contains_bids_and_asks(book_message):
    data = book_message["data"][0]

    assert len(data["bids"]) > 0
    assert len(data["asks"]) > 0


def test_book_does_not_contain_crosses(book_message):
    data = book_message["data"][0]

    best_ask = data["asks"][0]["price"]
    best_bid = data["bids"][0]["price"]

    assert best_bid < best_ask


def test_book_prices_are_sorted(book_message):
    data = book_message["data"][0]
    bid_prices = [level["price"] for level in data["bids"]]
    ask_prices = [level["price"] for level in data["asks"]]

    assert bid_prices == sorted(bid_prices, reverse=True)
    assert ask_prices == sorted(ask_prices)

def test_book_quantities_are_positive(book_message):
    data = book_message["data"][0]