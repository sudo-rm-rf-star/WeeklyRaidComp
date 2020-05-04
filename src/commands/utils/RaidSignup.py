from src.commands.utils.RegisterPlayer import register
from src.client.GuildClient import GuildClient
from src.logic.RaidEvents import RaidEvents
from src.logic.Players import Players
from src.commands.utils.CommandUtils import check_authority
from src.common.Constants import RAIDER_RANK
from src.common.EmojiNames import EMOJI_SIGNUP_STATUS
from src.client.entities.RaidMessage import RaidMessage
import discord
import asyncio


async def raid_signup(client: GuildClient, member_id: int, message_id: int, emoji: discord.PartialEmoji) -> None:
    raid_event = RaidEvents().get_raid_for_message(message_id)
    player = Players().get_by_id(member_id)
    member = client.get_member_by_id(member_id)
    if raid_event and emoji:
        check_authority(client, member, RAIDER_RANK)
        if player is None:
            await register(client, member)
        player = Players().get_by_id(member_id)
        signup_choice = EMOJI_SIGNUP_STATUS[emoji.name]
        raid_event.add_player_to_signees(player.name, signup_choice)
        response = f'You have signed up with "{signup_choice.name.lower()}" for {raid_event.get_name()} on {raid_event.get_datetime()}'
        raid_message = RaidMessage(client, raid_event)
        asyncio.create_task(raid_message.sync())
        await member.send(content=response)
        RaidEvents().store()
