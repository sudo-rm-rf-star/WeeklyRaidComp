from commands.utils.PlayerInteraction import interact, InteractionMessage
from commands.utils.DiscordRoleInteraction import DiscordRoleInteraction
from commands.utils.DiscordChannelInteraction import DiscordChannelInteraction
from client.entities.GuildMember import GuildMember
from logic.RaidGroup import RaidGroup
import uuid
import discord


def create_raidgroup(client: discord.Client, discord_guild: discord.Guild, member: GuildMember) -> RaidGroup:
    raidgroup_name = await interact(member, InteractionMessage(client, discord_guild, "Please fill in the name for your raiding group."))
    msg = f"Please select a Discord role for your raiders. These will receive personal messages for any updates for {raidgroup_name}"
    raider_rank = await interact(member, DiscordRoleInteraction(client, discord_guild, msg))
    msg = "Please select a Discord TextChannel to post all of the raid events for this raid group."
    events_channel = await interact(member, DiscordChannelInteraction(client, discord_guild, msg))
    msg = "Please fill in your warcraft logs ID for your raiding team. For now I'm to lazy to explain where to find this. You can leave this empty if you " \
          "can't find it, it's not super important. "
    wl_group_id = await interact(member, InteractionMessage(client, discord_guild, msg))
    return RaidGroup(name=raidgroup_name, raider_rank=raider_rank, group_id=uuid.uuid1().int, events_channel=events_channel,
                     wl_group_id=int(wl_group_id) if wl_group_id else None)
