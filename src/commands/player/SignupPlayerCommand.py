from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegisterPlayer import register
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier
from client.entities.RaidMessage import RaidMessage
from utils.Constants import RAIDER_RANK
from utils.EmojiNames import EMOJI_SIGNUP_STATUS
import asyncio


class SignupPlayerCommand(PlayerCommand):
    def __init__(self):
        argformat = ""
        subname = 'signup'
        description = 'Schrijf je in voor een raid'
        super(SignupPlayerCommand, self).__init__(subname, description, argformat, required_rank=RAIDER_RANK)

    async def execute(self, **kwargs) -> None:
        notification_id = DiscordMessageIdentifier(self.raw_reaction.message_id, self.member.id)
        raid_event = self.events_resource.get_raid_by_notification_id(notification_id)
        player = self.players_resource.get_player_by_id(self.member.id)
        if raid_event:
            if player is None:
                player = await register(self.client, self.players_resource, self.member)
            signup_choice = EMOJI_SIGNUP_STATUS[self.raw_reaction.emoji.name]
            raid_event.add_player_to_signees(player, signup_choice)
            raid_message = RaidMessage(self.client, raid_event)
            raid_message.sync()
            self.events_resource.update_raid(raid_event)
            self.respond(f'You have signed up with "{signup_choice.name.lower()}" for {raid_event.get_name()} on {raid_event.get_datetime()}')
