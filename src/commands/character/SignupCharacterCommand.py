from commands.character import CharacterCommand
from client.entities.RaidMessage import RaidMessage
from utils.EmojiNames import EMOJI_SIGNUP_STATUS


class SignupCharacterCommand(CharacterCommand):
    @classmethod
    def subname(cls) -> str: return "signup"

    @classmethod
    def description(cls) -> str: return "Signs you up for a raid. Currently this command is unusable manually"

    async def execute(self, **kwargs) -> None:
        raid_event = self.events_resource.get_raid_by_message(self.message_ref)
        if raid_event:
            # Remove character from signees if any other of his characters have already signed
            for char in self.player.characters:
                if char != self.player.get_selected_char() and raid_event.has_signed(char.name):
                    raid_event.remove_from_raid(char.name)
            # Add player to raid_event
            signup_choice = EMOJI_SIGNUP_STATUS[self.raw_reaction.emoji.name]
            raid_event.add_to_signees(self.player, signup_choice)
            raid_message = RaidMessage(self.client, self.discord_guild, raid_event)
            raid_message.sync()
            self.events_resource.update_raid(self.discord_guild, raid_event)
            self.respond(f'Thanks for signing up with {self.player.get_selected_char()} as {signup_choice.name.capitalize()} for '
                         f'{raid_event.get_name()} on {raid_event.get_datetime()}')
