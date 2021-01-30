from commands.utils.PlayerInteraction import interact, InteractionMessage
from commands.utils.DiscordRoleInteraction import DiscordRoleInteraction
from commands.utils.DiscordChannelInteraction import DiscordChannelInteraction
from client.entities.GuildMember import GuildMember
from logic.RaidTeam import RaidTeam
import uuid
import discord


async def create_raidgroup(client: discord.Client, discord_guild: discord.Guild, member: GuildMember) -> RaidTeam:
    msg = "Please fill in the name for your raiding group."
    raidgroup_name = await interact(member, InteractionMessage(client, discord_guild, msg))
    msg = f"Please choose a Discord role for your raiders. These will receive personal messages for any updates for {raidgroup_name} "
    raider_rank = await interact(member, DiscordRoleInteraction(client, discord_guild, msg))
    msg = "Please choose a Discord text channel to post all of the raid events for this raid group."
    events_channel = await interact(member, DiscordChannelInteraction(client, discord_guild, msg))
    return RaidTeam(name=raidgroup_name, raider_rank=raider_rank, group_id=uuid.uuid1().int,
                    events_channel=events_channel)
