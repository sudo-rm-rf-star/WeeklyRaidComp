from commands.character.CharacterCommand import CharacterCommand
from client.entities.RaidMessage import RaidMessage
from utils.EmojiNames import EMOJI_SIGNUP_STATUS
from datetime import datetime

DEADLINE_SIGNUP = 3600

class SignupCharacterCommand(CharacterCommand):
    @classmethod
    def subname(cls) -> str: return "signup"

    @classmethod
    def description(cls) -> str: return "Signs you up for a raid. Currently this command is unusable manually"

    async def execute(self, **kwargs) -> None:
        raid_event = self.events_resource.get_raid_by_message(self.message_ref)
        if not raid_event:
            self.respond("The event you signed up for no longer exists...")
            return
        seconds_until_event = (datetime.now() - raid_event.get_datetime().to_datetime()).seconds
        if seconds_until_event < 0:
            self.respond(f"Sorry, but you cannot sign for {raid_event} as it has already started or finished.")
            return
        if seconds_until_event < DEADLINE_SIGNUP:
            self.respond(f"Sorry, but you can no longer sign for {raid_event} as it starts in less than one hour.")
            return
        # Add player to raid_event
        signup_choice = EMOJI_SIGNUP_STATUS[self.raw_reaction.emoji.name]
        raid_event.add_to_signees(self.player, signup_choice)
        raid_message = RaidMessage(self.client, self.discord_guild, raid_event)
        raid_message.sync()
        self.events_resource.update_raid(self.discord_guild, raid_event)
        self.respond(f'Thanks for signing up with {self.player.get_selected_char()} as {signup_choice.name.capitalize()} for '
                     f'{raid_event.get_name()} on {raid_event.get_datetime()}')
