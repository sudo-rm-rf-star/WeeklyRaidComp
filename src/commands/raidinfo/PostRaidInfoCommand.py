from src.commands.raidinfo.RaidInfoCommand import RaidInfoCommand
from src.common.Constants import INFO_CHANNEL, RAID_INFO_EMBEDS
from src.commands.utils.CommandUtils import delete_bot_messages
import discord
import json
from src.client.GuildClient import GuildClient
import discord


class PostRaidInfoCommand(RaidInfoCommand):
    def __init__(self):
        subname = 'post'
        description = f'Vernieuw het #{INFO_CHANNEL} kanaal'
        super(PostRaidInfoCommand, self).__init__(subname, description)

    async def run(self, client: GuildClient, message: discord.Message, **kwargs) -> None:
        text_channel = client.get_channel(INFO_CHANNEL)
        await delete_bot_messages(client, text_channel)
        with open(RAID_INFO_EMBEDS) as raid_info_file:
            for embed_str in json.loads(raid_info_file.read()):
                await text_channel.send(embed=discord.Embed.from_dict(embed_str))
