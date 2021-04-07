from datetime import datetime
from typing import Tuple

from dokbot.RaidContext import RaidContext
from dokbot.entities.HelpMessage import HelpMessage
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.interactions.ChooseSpecMessage import ChooseSpecMessage
from dokbot.player_actions.Register import register
from exceptions.InvalidInputException import InvalidInputException
from logic.Character import Character
from logic.Player import Player
from logic.enums.SignupStatus import SignupStatus
from persistence.PlayersResource import PlayersResource
from persistence.RaidEventsResource import RaidEventsResource
from utils.Constants import DATETIMESEC_FORMAT

ADD_CHAR = 'Add a new character.'
REMOVE_CHAR = 'Remove a character.'


async def signup_character(ctx: RaidContext, signup_status: SignupStatus):
    if not ctx.raid_event.in_future():
        await ctx.reply(f"Sorry, but you cannot sign for {ctx.raid_event} as it has already started or finished.")
        return

    if signup_status == SignupStatus.Unknown:
        await HelpMessage.reply_to_author(ctx, actions=SignupStatus)
        return

    players_resource = PlayersResource()
    player = players_resource.get_player_by_id(ctx.author.id)
    if signup_status == SignupStatus.AddChar:
        await register(ctx=ctx)
        return

    if not player:
        player, character = await register(ctx=ctx)

    if signup_status == SignupStatus.RemoveChar:
        content = "Please choose the character you want to remove."
        _, character = await CharacterSelectionInteraction.interact(ctx=ctx, player=player, content=content)
        players_resource.remove_character(character)
        await ctx.reply(f"Removed {character}")
        return

    if signup_status == SignupStatus.SwitchChar:
        signup_status = ctx.raid_event.get_signup_choice(player)  # Save previous signup state
        content = "Please choose the character you want to signup with for raids."
        player, character = await CharacterSelectionInteraction.interact(ctx=ctx, player=player, content=content)
        player.set_selected_char(character.name)
        players_resource.update_player(player)

    if signup_status == SignupStatus.SwitchSpec:
        signup_status = ctx.raid_event.get_signup_choice(player)  # Save previous signup state
        character = player.get_selected_char()
        spec = await ChooseSpecMessage.interact(ctx=ctx, klass=character.klass)
        character.spec = spec
        players_resource.update_player(player)

    # Add player to raid_event
    # Retrieve the latest version of the raid event to avoid conflicts.
    raid_event = RaidEventsResource(ctx).synced(ctx.raid_event)
    character = raid_event.add_to_signees(player, signup_status)
    RaidEventsResource(ctx).update_raid(raid_event)

    # This is possible if it is the first time a character has signed or if a raid team chose a wrong realm.
    if ctx.raid_team.realm != character.realm or ctx.raid_team.region != character.region:
        character.realm = ctx.raid_team.realm
        character.region = ctx.raid_team.region
        players_resource.update_player(player)

    display_character = await ctx.bot.display_character(character)
    if character.get_signup_status() == SignupStatus.Accept:
        response = f'{display_character} - Thanks for accepting {raid_event}. See you then !'
    elif character.get_signup_status() == SignupStatus.Decline:
        response = f'{display_character} - You have declined {raid_event}.'
    elif character.get_signup_status() == SignupStatus.Tentative:
        response = f'{display_character} - Not 100% certain that you can join for {raid_event}. Please let me know whether you can join before the raid.'
    elif character.get_signup_status() == SignupStatus.Late:
        response = f'{display_character} - Thanks for accepting {raid_event}. Please let the raid leader know from when you are available.'
    elif character.get_signup_status() == SignupStatus.Bench:
        response = f'{display_character} - So you prefer to sit {raid_event} out, contact the raid leader to see if this is possible.'
    else:
        response = f"You will now sign up with {display_character}. You still need to sign for this raid."
    await ctx.reply_to_author(response)
    await (await ctx.get_signup_history_channel()).send(
        f'{datetime.now().strftime(DATETIMESEC_FORMAT)} **{display_character}** {await ctx.bot.emoji(signup_status.name)}')


class CharacterSelectionInteraction(OptionInteraction):
    def __init__(self, ctx: RaidContext, content: str, player: Player):
        self.player = player
        options = [char.name for char in player.characters]
        super().__init__(ctx=ctx, content=content, options=options)

    async def get_response(self) -> Tuple[Player, Character]:
        response = await super(CharacterSelectionInteraction, self).get_response()
        for character in self.player.characters:
            if response == character.name:
                return self.player, character
        raise InvalidInputException(f'Please choose on of: {self.options}')
