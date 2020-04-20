from src.commands.RaidInfoCommand import RaidInfoCommand
from src.common.Constants import INFO_CHANNEL, RAID_INFO_EMBEDS
from src.disc.ServerUtils import get_channel
from src.commands.CommandUtils import delete_bot_messages
import discord
import json


class PostRaidInfoCommand(RaidInfoCommand):
    def __init__(self):
        subname = 'post'
        description = f'Vernieuw het #{INFO_CHANNEL} kanaal'
        argformat = None
        super(PostRaidInfoCommand, self).__init__(subname, description, argformat)

    async def run(self, client, message, **kwargs):
        text_channel = get_channel(client, INFO_CHANNEL)
        await delete_bot_messages(client, text_channel)
        with open(RAID_INFO_EMBEDS) as raid_info_file:
            for embed_str in json.loads(raid_info_file.read()):
                await text_channel.send(embed=discord.Embed.from_dict(embed_str))
