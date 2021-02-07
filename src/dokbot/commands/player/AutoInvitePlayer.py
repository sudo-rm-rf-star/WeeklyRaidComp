from dokbot.commands.player.PlayerCommand import PlayerCommand


class AutoInvitePlayer(PlayerCommand):
    @classmethod
    def sub_name(cls) -> str: return "autoinvite"

    @classmethod
    def argformat(cls) -> str: return "player [on_or_off]"

    @classmethod
    def description(cls) -> str: return "Auto-invites a player to your raids, " \
                                        "only use if the player does not have the raider rank."

    async def execute(self, player: str, on_or_off: bool, **kwargs) -> None:
        player = self.players_resource.get_player_by_name(player, self.guild)
        if not player:
            self.respond(f"Could not find player {player}")
            return

        player.autoinvited = True if on_or_off is None else on_or_off
        self.players_resource.update_player(player)
        self.respond(f'Succesfully set autoinvite for {player} to {player.autoinvited}')
