from commands.character.CharacterCommand import CharacterCommand
from utils.EmojiNames import EMOJI_SIGNUP_STATUS
from datetime import datetime
from logic.enums.SignupStatus import SignupStatus
from commands.utils.CharacterSelectionInteraction import CharacterSelectionInteraction
from utils.DiscordUtils import get_emoji
from utils.EmojiNames import SIGNUP_STATUS_HELP, SIGNUP_STATUS_EMOJI


class SignupCharacterCommand(CharacterCommand):
    @classmethod
    def subname(cls) -> str:
        return "signup"

    @classmethod
    def description(cls) -> str:
        return "Signs you up for a raid. Currently this command is unusable manually"

    async def execute(self, **kwargs) -> None:
        raid_event = self.events_resource.get_raid_by_message(self.message_ref)
        if not raid_event:
            self.respond("The event you signed up for no longer exists...")
            return
        seconds_until_event = (datetime.now() - raid_event.get_datetime().to_datetime()).seconds
        if seconds_until_event < 0:
            self.respond(f"Sorry, but you cannot sign for {raid_event} as it has already started or finished.")
            return
        # People cannot sign trough manual reactions if the raid is not open.
        if self.raw_reaction.message_id in [message.message_id for message in
                                            raid_event.message_refs] and not raid_event.is_open:
            self.respond(f'You cannot sign for event without invitation.')
            return
        signup_choice = EMOJI_SIGNUP_STATUS[self.raw_reaction.emoji.name]

        if signup_choice == SignupStatus.SWITCH_CHAR:
            signup_choice = raid_event.get_signup_choice(self.player)  # Save previous signup state
            player, character = await self.interact(CharacterSelectionInteraction, self.players_resource, self.member,
                                                    self.player)
            self.player = player  # Player has possibly been updated
            self.player.set_selected_char(character.name)
            self.players_resource.update_player(self.player)

        if signup_choice == SignupStatus.UNDECIDED:
            help_response = "\n".join(
                [f"{get_emoji(self.client, SIGNUP_STATUS_EMOJI[signup_state])} {help_str}" for
                 signup_state, help_str in SIGNUP_STATUS_HELP.items()])
            self.respond(help_response)
            return

        # Add player to raid_event
        character = raid_event.add_to_signees(self.player, signup_choice)
        self.events_resource.update_raid(self.discord_guild, raid_event)
        self.respond(
            f'Thanks for signing up with {character} as {character.signup_status} '
            f'for {raid_event}')
