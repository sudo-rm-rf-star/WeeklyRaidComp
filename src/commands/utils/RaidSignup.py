from src.commands.utils.RegisterPlayer import register
from src.client.GuildClient import GuildClient
from src.logic.RaidEvents import RaidEvents
from src.logic.Players import Players
from src.logic.enums.SignupStatus import SignupStatus
from src.commands.utils.CommandUtils import check_authority
from src.common.Constants import RAIDER_RANK
from src.common.EmojiNames import EMOJI_SIGNUP_STATUS, SIGNUP_STATUS_EMOJI
from src.exceptions.InternalBotException import InternalBotException
from src.client.entities.RaidMessage import RaidMessage
import discord
import asyncio


async def raid_signup(client: GuildClient, member_id: int, message_id: int, channel_id, emoji: discord.PartialEmoji) -> None:
    raid_event = RaidEvents().get_by_message_id(message_id)
    player = Players().get_by_id(member_id)
    member = client.get_member_by_id(member_id)
    if raid_event and emoji:
        check_authority(client, member, RAIDER_RANK)
        if player is None:
            await register(client, member)
        signup_choice = EMOJI_SIGNUP_STATUS[emoji.name]
        old_signup_choice = raid_event.get_signup_choice(player.name)
        raid_event.add_player_to_signees(player.name, signup_choice)
        response = f'You have successfully signed up for {raid_event.get_name()} on {raid_event.get_datetime()}'
        raid_message = RaidMessage(client, raid_event)
        asyncio.create_task(raid_message.sync())
        if old_signup_choice:
            asyncio.create_task(remove_signup_reaction(client, member, old_signup_choice, message_id, channel_id))
        await member.send(content=response)


async def remove_signup_reaction(client: GuildClient, member: discord.Member, signup_choice: SignupStatus, message_id: int, channel_id: int) -> None:
    msg = await client.get_message((message_id, channel_id))
    emoji = client.get_emoji(SIGNUP_STATUS_EMOJI[signup_choice])
    await msg.remove_reaction(emoji, member)
