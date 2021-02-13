from utils.EmojiNames import EMOJI_SIGNUP_STATUS
from datetime import datetime
from logic.enums.SignupStatus import SignupStatus
from dokbot.interactions.CharacterSelectionInteraction import CharacterSelectionInteraction
from dokbot.DiscordUtils import get_emoji
from utils.EmojiNames import SIGNUP_STATUS_HELP, SIGNUP_STATUS_EMOJI
from persistence.RaidEventsResource import RaidEventsResource
from persistence.RaidTeamsResource import RaidTeamsResource
from persistence.MessagesResource import MessagesResource
from persistence.PlayersResource import PlayersResource
from dokbot.DiscordGuild import DiscordGuild
import discord


async def signup_character(client: discord.Client, reaction_event: discord.RawReactionActionEvent):
    message_ref = MessagesResource().get_message(reaction_event.message_id)
    raid_team = RaidTeamsResource().get_raidteam(guild_id=message_ref.guild_id, team_name=message_ref.team_name)
    discord_guild = await DiscordGuild.create_helper(client, raid_team)
    member = await discord_guild.get_member_by_id(reaction_event.user_id)

    def respond(content: str):
        discord_guild.respond(content=content, member=member, action=reaction_event)

    raid_event = RaidEventsResource().get_raid_by_message(message_ref)
    if not raid_event:
        respond("The event you signed up for no longer exists...")
        return
    seconds_until_event = (datetime.now() - raid_event.get_datetime()).seconds
    if seconds_until_event < 0:
        respond(f"Sorry, but you cannot sign for {raid_event} as it has already started or finished.")
        return
    # People cannot sign trough manual reactions if the raid is not open.
    if reaction_event.message_id in [message.message_id for message in
                                     raid_event.message_refs] and not raid_event.is_open:
        respond(f'You cannot sign for event without invitation.')
        return
    signup_choice = EMOJI_SIGNUP_STATUS[reaction_event.emoji.name]

    if signup_choice == SignupStatus.UNDECIDED:
        help_response = "\n".join(
            [f"{get_emoji(client, SIGNUP_STATUS_EMOJI[signup_state])} {help_str}" for
             signup_state, help_str in SIGNUP_STATUS_HELP.items()])
        respond(help_response)
        return

    players_resource = PlayersResource()
    player = players_resource.get_player_by_id(member.id)
    if signup_choice == SignupStatus.SWITCH_CHAR:
        signup_choice = raid_event.get_signup_choice(player)  # Save previous signup state
        player, character = await CharacterSelectionInteraction.interact(member=member, client=client,
                                                                         guild=discord_guild,
                                                                         player=player)
        player = player  # Player has possibly been updated
        player.set_selected_char(character.name)
        players_resource.update_player(player)

    # Add player to raid_event
    character = raid_event.add_to_signees(player, signup_choice)
    RaidEventsResource().update_raid(raid_event)

    if character.get_signup_status() == SignupStatus.ACCEPT:
        response = f'Thanks for accepting {raid_event}. See you then {character.name}!'
    elif character.get_signup_status() == SignupStatus.DECLINE:
        response = f'You have declined {raid_event}.'
    elif character.get_signup_status() == SignupStatus.TENTATIVE:
        response = f'Not 100% certain that you can join for {raid_event}? No worries {character.name}, ' \
                   f'please let me know whether you can join before the raid!'
    elif character.get_signup_status() == SignupStatus.LATE:
        response = f'Thanks for accepting {raid_event}. Please let the raid leader know from when you are available {character.name}'
    elif character.get_signup_status() == SignupStatus.BENCH:
        response = f'So you prefer to sit {raid_event} out, contact the raid leader to see if this is possible {character.name}'
    else:
        response = f"You will now sign up with {character.name}. You still need to sign for this raid."
    respond(response)
