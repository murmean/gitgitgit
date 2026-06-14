import websocket
import json
import logging
from constants import URL, default_timeout

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.INFO,
)


class KrakenWS:

    def __init__(self, timeout=default_timeout):
        self.timeout = timeout
        self.ws = None
        self.url = URL

    def setTrace(self, value: bool):
        websocket.enableTrace(value)
        log.info(f"New trace value:{value}")

    def connect(self):
        try:
            log.info("Establishing connection with server...")
            self.ws = websocket.WebSocket()
            self.ws.settimeout(self.timeout)
            self.ws.connect(self.url)
        except Exception as e:
            log.error(f"Failed to establish connection: {e}")
            raise

    def subscribe(self, channel, symbol, **args):
        if not self.ws:
            raise RuntimeError("Websocket connection is not initialised, use connect() to establish")

        payload = {
            "method": "subscribe",
            "params": {
                "channel": channel,
                "symbol": [symbol],
                **args
            }
        }
        self.ws.send(json.dumps(payload))

    def receive_message(self, key, value, max_messages=20):
        for _ in range(max_messages):
            message = json.loads(self.ws.recv())

            if message.get(key) == value:
                return message

        raise TimeoutError(
            f"Message with {key}={value} not found"
        )

    def load_multiple_messages(self, max_messages=20):
        messages = []

        for _ in range(max_messages):
            try:
                raw_txt = self.ws.recv()
                messages.append(json.loads(raw_txt))
            except Exception:
                break

        return messages

    def close_connection(self):
        if self.ws:
            log.info("Closing WebSocket")
            self.ws.close()
        else:
            log.info("No socket is open")
