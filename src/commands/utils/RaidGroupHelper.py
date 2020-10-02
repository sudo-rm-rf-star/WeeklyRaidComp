from commands.utils.PlayerInteraction import interact, InteractionMessage
from commands.utils.OptionInteraction import OptionInteraction
from commands.utils.DiscordRoleInteraction import DiscordRoleInteraction
from commands.utils.DiscordChannelInteraction import DiscordChannelInteraction
from client.entities.GuildMember import GuildMember
from logic.RaidGroup import RaidGroup
import uuid
import discord
from utils.WarcraftLogs import get_raidgroups


async def create_raidgroup(client: discord.Client, discord_guild: discord.Guild, member: GuildMember, wl_guild_id: int) -> RaidGroup:
    raidgroups = get_raidgroups(wl_guild_id)
    if raidgroups:
        raidgroup_name = await interact(member, OptionInteraction(client, discord_guild, "Please choose a raidgroup", list(raidgroups.keys())))
        raidgroup_id = raidgroups[raidgroup_name]
    else:
        raidgroup_name = await interact(member, InteractionMessage(client, discord_guild, "Please fill in the name for your raiding group."))
        raidgroup_id = None
    msg = f"Please select a Discord role for your raiders. These will receive personal messages for any updates for {raidgroup_name}"
    raider_rank = await interact(member, DiscordRoleInteraction(client, discord_guild, msg))
    msg = "Please select a Discord text channel to post all of the raid events for this raid group."
    events_channel = await interact(member, DiscordChannelInteraction(client, discord_guild, msg))
    return RaidGroup(name=raidgroup_name, raider_rank=raider_rank, group_id=uuid.uuid1().int,
                     events_channel=events_channel, wl_group_id=raidgroup_id)
