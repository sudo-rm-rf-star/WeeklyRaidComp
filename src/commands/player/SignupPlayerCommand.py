from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegistrationHelper import register
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier
from client.entities.RaidMessage import RaidMessage
from utils.EmojiNames import EMOJI_SIGNUP_STATUS


class SignupPlayerCommand(PlayerCommand):
    @classmethod
    def subname(cls) -> str: return "signup"

    @classmethod
    def description(cls) -> str: return "Signs you up for a raid. Currently this command is unusable manually"

    async def execute(self, **kwargs) -> None:
        notification_id = DiscordMessageIdentifier(self.raw_reaction.message_id, self.member.id)
        player = self.players_resource.get_player_by_id(self.member.id)
        if player is None:
            await register(self.client, self.discord_guild, self.players_resource, self.member)
        raid_event = self.events_resource.get_raid_by_notification_id(self.discord_guild, notification_id)
        if raid_event:
            # Remove character from signees if any other of his characters have already signed
            for char in player.characters:
                if char != player.get_selected_char() and raid_event.has_signed(char.name):
                    raid_event.remove_from_raid(char.name)
            # Add player to raid_event
            signup_choice = EMOJI_SIGNUP_STATUS[self.raw_reaction.emoji.name]
            raid_event.add_to_signees(player, signup_choice)
            raid_message = RaidMessage(self.client, self.discord_guild, raid_event)
            raid_message.sync()
            self.events_resource.update_raid(self.discord_guild, raid_event)
            self.respond(f'Thanks for signing up with {player.get_selected_char()} as {signup_choice.name.capitalize()} for '
                         f'{raid_event.get_name()} on {raid_event.get_datetime()}')
