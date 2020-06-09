from commands.player.PlayerCommand import PlayerCommand
from commands.utils.RegistrationHelper import register
from client.entities.DiscordMessageIdentifier import DiscordMessageIdentifier
from client.entities.RaidMessage import RaidMessage
from utils.EmojiNames import EMOJI_SIGNUP_STATUS


class SignupPlayerCommand(PlayerCommand):
    def __init__(self):
        subname = 'signup'
        description = 'Schrijf je in voor een raid. (Voorlopig is dit commando niet bruikbaar)'
        super(SignupPlayerCommand, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        notification_id = DiscordMessageIdentifier(self.raw_reaction.message_id, self.member.id)
        players = self.players_resource.get_characters_by_id(self.member.id)
        selected_character = self.players_resource.get_selected_character(players)
        raid_event = self.events_resource.get_raid_by_notification_id(self.discord_guild, notification_id)
        if raid_event:
            if selected_character is None:
                selected_character = await register(self.client, self.discord_guild, self.players_resource, self.member)
            # Remove character from signees if any other of his characters have already signed
            for player in players:
                if player != selected_character and raid_event.has_signed(player.name):
                    raid_event.remove_from_raid(player.name)
            # Add player to raid_event
            signup_choice = EMOJI_SIGNUP_STATUS[self.raw_reaction.emoji.name]
            raid_event.add_to_signees(selected_character, signup_choice)
            raid_message = RaidMessage(self.client, self.discord_guild, raid_event)
            raid_message.sync()
            self.events_resource.update_raid(self.discord_guild, raid_event)
            self.respond(f'Thanks for signing up with {selected_character.name} as {signup_choice.name.capitalize()} for '
                         f'{raid_event.get_name()} on {raid_event.get_datetime()}')
