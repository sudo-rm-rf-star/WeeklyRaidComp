from dokbot.RaidContext import RaidContext
from dokbot.DokBotContext import DokBotContext
from persistence.RaidEventsResource import RaidEventsResource
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
from exceptions.CancelInteractionException import CancelInteractionException

YES = "Yes"
NO = "No"


async def remove_raid(ctx: RaidContext):
    await ConfirmAction.interact(ctx)
    RaidEventsResource(ctx).remove_raid(ctx.raid_event)
    await ctx.reply(f"Removed {ctx.raid_event}")


class ConfirmAction(EmojiInteractionMessage):
    def __init__(self, ctx: DokBotContext):
        content = "Are you sure you want to continue?"
        icons = [YES, NO]
        super().__init__(ctx=ctx, content=content, reactions=icons)

    async def get_response(self):
        response = await super(ConfirmAction, self).get_response()
        if response == NO:
            raise CancelInteractionException("Aborting.")
