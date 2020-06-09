from commands.guild.GuildCommand import GuildCommand
from commands.utils.PlayerInteraction import InteractionMessage, interact
from commands.utils.DiscordRoleInteraction import DiscordRoleInteraction
from commands.utils.DiscordChannelInteraction import DiscordChannelInteraction
from commands.utils.RaidGroupHelper import create_raidgroup
from utils.Constants import BOT_NAME
from logic.Guild import Guild


class CreateGuild(GuildCommand):
    def __init__(self):
        subname = 'add'
        description = 'Maak een guild aan'
        super(CreateGuild, self).__init__(subname=subname, description=description)

    async def execute(self, **kwargs) -> None:
        guild = self.guilds_resource.get_guild(self.discord_guild.id)
        if guild:
            self.respond(f"This channel already has a guild named {guild.name}. A channel can only have one guild.")
            return
        await self.member.send(
            f"Thanks for giving {BOT_NAME} a chance! I hope I'll prove useful for your guild. Let me give a brief introduction of my purpose. "
            f"(Insert Rick and Morty 'What is my purpose...' reference). My main purpose is to make raid organization for your guild as easy to "
            f"manage as possible. A lot of the time-consuming tasks with organizing raids should be either automatic or very quick to do trough "
            f"me. Next to just helping the raid leaders life, it also tries to help the raider by serving as a medium between the raider and "
            f"raid leader. You can use me as to create raids, I will send a personal message to every raider on Discord trough which they can "
            f"sign for the raid. I'll create a Discord message which contains all of the information of the raid which includes all of the "
            f"raider information such as their character name, their role, their class and how they signed for your raid. At any point after "
            f"raid creation you can decide to create a roster for your raid. The bot uses heuristics to create an optimal roster for you and "
            f"sends status updates to all of the raiders telling them whether they got a spot in your raid. Don't worry, you can manually make "
            f"any changes if you're not happy with the outcome. This is a quick summary on my main functionality, for a more detailed guide on "
            f"how to use me, please type: !dokbot help. For now, let's start with setting up your guild! Please answer the following questions :)"
        )
        guild_name = await interact(self.member, InteractionMessage(self.client, self.discord_guild, "Please fill in the name of your guild."))
        realm = await interact(self.member, InteractionMessage(self.client, self.discord_guild, "Please fill in the realm of your guild."))
        manager_rank = await interact(self.member, DiscordRoleInteraction(self.client, self.discord_guild, "Please select a Discord role to manage this guild"))
        msg = "Please select a Discord TextChannel to post all of the bot logs for this guild."
        logs_channel = await interact(self.member, DiscordChannelInteraction(self.client, self.discord_guild, msg))
        wl_guild_id = await interact(self.member, InteractionMessage(self.client, self.discord_guild,
                                                                     "Please fill in your warcraft logs ID for your guild. For now I'm to lazy "
                                                                     "to explain where to find this. You can leave this empty if you can't find "
                                                                     "it, it's not super important."
                                                                     ))
        await self.member.send(
            "Thanks for your cooperation so far! We just created your guild on Discord. But every guild can have one or more raid groups. You can see "
            "a raid group as a team who periodically comes together to tackle certain raids. You could have an A-team and a B-team for example, let's start"
            "with your first team. You can create more teams later with: !raidgroup create. Let's continue."
        )
        raidgroup = create_raidgroup(self.client, self.discord_guild, self.member)
        guild = Guild(name=guild_name, realm=realm, manager_rank=manager_rank, guild_id=self.discord_guild.id, logs_channel=logs_channel,
                      wl_guild_id=int(wl_guild_id) if wl_guild_id else None, groups=[raidgroup])
        self.guilds_resource.create_guild(guild)
        self.respond(f"Your guild {guild_name} has succesfully been created!")



