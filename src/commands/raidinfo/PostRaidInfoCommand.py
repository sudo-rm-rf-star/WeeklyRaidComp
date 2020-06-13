from commands.raidinfo.RaidInfoCommand import RaidInfoCommand
from utils.Constants import INFO_CHANNEL, RAID_INFO_EMBEDS
from commands.utils.CommandUtils import delete_bot_messages
import json
import discord


class PostRaidInfoCommand(RaidInfoCommand):
    @classmethod
    def subname(cls) -> str: return "post"

    @classmethod
    def description(cls) -> str: return "Update the raid-info channel. (This is an old command and hasn't been reviewed in a while)"

    async def execute(self, **kwargs) -> None:
        text_channel = self.client.get_channel(INFO_CHANNEL)
        await delete_bot_messages(self.client, text_channel)
        with open(RAID_INFO_EMBEDS) as raid_info_file:
            for embed_str in json.loads(raid_info_file.read()):
                await text_channel.send(embed=discord.Embed.from_dict(embed_str))
