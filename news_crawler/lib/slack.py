from slack_sdk.webhook import WebhookClient


class SlackClient:
    def __init__(self, endpoint: str):
        self.webhook = WebhookClient(endpoint)

    def send_message(self, message: str):
        self.webhook.send(text=message)
