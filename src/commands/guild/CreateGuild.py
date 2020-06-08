from commands.guild.GuildCommand import GuildCommand
from commands.utils.PlayerInteraction import InteractionMessage, interact
from logic.Guild import Guild
from utils.Constants import BOT_NAME
from utils.DiscordUtils import get_roles, get_role
from exceptions.InvalidArgumentException import InvalidArgumentException
import discord


class CreateGuild(GuildCommand):
    def __init__(self):
        argformat = ""
        subname = 'add'
        description = 'Maak een guild aan'
        super(CreateGuild, self).__init__(subname, description, argformat, required_rank=None)

    async def execute(self, **kwargs) -> None:
        await self.member.send(
            f"Thanks for giving {BOT_NAME} a chance! I hope I'll prove useful for your guild. Let me give a brief introduction of my purpose. "
            f"(Insert Rick and Morty 'What is my purpose...' reference. My main purpose is to make raid organization for your guild as easy to "
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
        guild_name = await interact(self.member, InteractionMessage(self.client, "Please fill in the name of your guild."))
        realm = await interact(self.member, InteractionMessage(self.client, "Please fill in the realm of your guild."))
        manager_rank = await interact(self.member, DiscordRoleMessage(self.client, self.discord_guild, "Please select a Discord role to manage this guild"))
        wl_guild_id = await interact(self.member, InteractionMessage(self.client, "Please fill in your warcraft logs ID for your guild. For now I'm to lazy "
                                                                                  "to explain where to find this. You can leave this empty if you can't find "
                                                                                  "it, it's not super important."))
        await self.member.send(
            "Thanks for your cooperation so far! We just created your guild on Discord. But every guild can have one or more raid groups. You can see "
            "a raid group as a team who periodically comes together to tackle certain raids. You could have an A-team and a B-team for example, let's start"
            "with your first team. You can create more teams later with: !raidgroup create. Let's continue."
        )

        raidgroup_name = await interact(self.member, InteractionMessage(self.client, "Please fill in the name for your raiding group."))
        manager_rank = await interact(self.member, DiscordRoleMessage(self.client, self.discord_guild,
                                                                      f"Please select a Discord role for your raiders. These will receive personal messages for any updates for {raidgroup_name}"))
        wl_group_id = await interact(self.member, InteractionMessage(self.client,
                                                                     "Please fill in your warcraft logs ID for your raiding team. For now I'm to lazy to explain where to find this. You can leave this empty if you can't find it, it's not super important."))




class DiscordRoleMessage(InteractionMessage):
    def __init__(self, client: discord.Client, guild: discord.Guild, content: str, *args, **kwargs):
        content =
        self.options = '/'.join([' '.join([role.name for role in get_roles(guild)])])
        content += f': [{self.options}]'
        self.guild = guild
        super().__init__(client, content, *args, **kwargs)

    async def get_response(self) -> discord.Role:
        response = await super(DiscordRoleMessage, self).get_response()
        role = get_role(self.guild, response)
        if role:
            return role
        else:
            raise InvalidArgumentException(f'Please choose on of: {self.options}')
