class DiscordMessageIdentifier:
    def __init__(self, message_id: int, channel_id: int):
        self.message_id = message_id
        self.channel_id = channel_id

    def to_str(self) -> str:
        return f'{self.message_id}_{self.channel_id}'

    @staticmethod
    def from_str(string: str):
        return DiscordMessageIdentifier(*tuple(string.split('_')))
