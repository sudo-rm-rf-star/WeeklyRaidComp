from utils.EmojiNames import SIGNUP_STATUS_EMOJI
from logic.RaidEvent import RaidEvent
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
import discord
from logic.RaidTeam import RaidTeam


class RaidNotification(EmojiInteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, raid_event: RaidEvent, raidteam: RaidTeam):
        self.client = client
        self.raid_event = raid_event
        content = f"You have been invited for {raid_event} for {raidteam}. " \
                  f"Please sign by clicking one of the reaction boxes."
        emojis = SIGNUP_STATUS_EMOJI.values()
        super(RaidNotification, self).__init__(client, guild, content=content, emojis=emojis)
