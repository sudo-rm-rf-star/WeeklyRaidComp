from src.commands.BotCommand import BotCommand
from src.commands.CommandUtils import update_raids, update_whitelisted, get_roster_embed
from src.disc.ServerUtils import get_channel
from src.common.Constants import COMPS_CHANNEL
from src.logic.Raid import Raid
from src.logic.Rosters import Rosters


class RosterCommand(BotCommand):
    def __init__(self, subname, description, argformat, required_rank, allow_trough_approval=False):
        super(RosterCommand, self).__init__('roster', subname, description, argformat, required_rank,
                                            allow_trough_approval)

    async def update_datastores(self, client):
        await update_raids(client)
        update_whitelisted(client)

    def load_rosters(self, raid_name, raid_datetime):
        return Rosters.load(raid_name, raid_datetime)

    def get_roster_embed(self, client, rosters):
        raid = Raid.load(rosters.raid_name, rosters.raid_datetime)
        return get_roster_embed(client, rosters, raid)

    async def post_roster(self, client, rosters):
        text_channel = get_channel(client, COMPS_CHANNEL)
        message_id = rosters.message_id
        embed = self.get_roster_embed(client, rosters)
        if message_id:
            message = await text_channel.fetch_message(message_id)
            message.edit(embed=embed)
        else:
            msg = await text_channel.send(embed=embed)
            rosters.set_message_id(msg.id)

