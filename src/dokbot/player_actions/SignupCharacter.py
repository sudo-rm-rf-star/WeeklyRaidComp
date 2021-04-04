from typing import Tuple

from dokbot.RaidContext import RaidContext
from dokbot.interactions.OptionInteraction import OptionInteraction
from dokbot.player_actions.Register import register
from dokbot.entities.HelpMessage import HelpMessage
from exceptions.InvalidInputException import InvalidInputException
from logic.Character import Character
from logic.Player import Player
from logic.enums.SignupStatus import SignupStatus
from persistence.PlayersResource import PlayersResource
from persistence.RaidEventsResource import RaidEventsResource

ADD_CHAR = 'Add a new character.'


async def signup_character(ctx: RaidContext, signup_status: SignupStatus):
    if not ctx.raid_event.in_future():
        await ctx.reply(f"Sorry, but you cannot sign for {ctx.raid_event} as it has already started or finished.")
        return

    if signup_status == SignupStatus.Unknown:
        await HelpMessage.reply_to_author(ctx, actions=SignupStatus)
        return

    players_resource = PlayersResource()
    player = players_resource.get_player_by_id(ctx.author.id)
    if player and signup_status == SignupStatus.SwitchChar:
        signup_status = ctx.raid_event.get_signup_choice(player)  # Save previous signup state
        player, character = await CharacterSelectionInteraction.interact(ctx=ctx, player=player)
        player.set_selected_char(character.name)
        players_resource.update_player(player)

    if not player:
        player, character = await register(ctx=ctx)

    # Add player to raid_event
    # Retrieve the latest version of the raid event to avoid conflicts.
    raid_event = RaidEventsResource(ctx).synced(ctx.raid_event)
    character = raid_event.add_to_signees(player, signup_status)
    RaidEventsResource(ctx).update_raid(raid_event)

    if character.get_signup_status() == SignupStatus.Accept:
        response = f'Thanks for accepting {raid_event}. See you then {character.name}!'
    elif character.get_signup_status() == SignupStatus.Decline:
        response = f'You have declined {raid_event}.'
    elif character.get_signup_status() == SignupStatus.Tentative:
        response = f'Not 100% certain that you can join for {raid_event}? No worries {character.name}, ' \
                   f'please let me know whether you can join before the raid!'
    elif character.get_signup_status() == SignupStatus.Late:
        response = f'Thanks for accepting {raid_event}. Please let the raid leader know from when you are available {character.name}'
    elif character.get_signup_status() == SignupStatus.Bench:
        response = f'So you prefer to sit {raid_event} out, contact the raid leader to see if this is possible {character.name}'
    else:
        response = f"You will now sign up with {character.name}. You still need to sign for this raid."
    await ctx.reply_to_author(response)


class CharacterSelectionInteraction(OptionInteraction):
    def __init__(self, ctx: RaidContext, player: Player):
        self.player = player
        options = [char.name for char in player.characters] + [ADD_CHAR]
        content = "Please choose the character you want to signup with for raids (Enter a number):"
        super().__init__(ctx=ctx, content=content, options=options)

    async def get_response(self) -> Tuple[Player, Character]:
        response = await super(CharacterSelectionInteraction, self).get_response()
        if response == ADD_CHAR:
            return await register(ctx=self.ctx)
        for character in self.player.characters:
            if response == character.name:
                return self.player, character
        raise InvalidInputException(f'Please choose on of: {self.options}')
