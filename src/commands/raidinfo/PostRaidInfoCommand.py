from commands.raidinfo.RaidInfoCommand import RaidInfoCommand
from utils.Constants import INFO_CHANNEL, RAID_INFO_EMBEDS
from commands.utils.CommandUtils import delete_bot_messages
import json
import discord


class PostRaidInfoCommand(RaidInfoCommand):
    def __init__(self):
        subname = 'post'
        description = f'Vernieuw het #{INFO_CHANNEL} kanaal'
        super(PostRaidInfoCommand, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        text_channel = self.client.get_channel(INFO_CHANNEL)
        await delete_bot_messages(self.client, text_channel)
        with open(RAID_INFO_EMBEDS) as raid_info_file:
            for embed_str in json.loads(raid_info_file.read()):
                await text_channel.send(embed=discord.Embed.from_dict(embed_str))
