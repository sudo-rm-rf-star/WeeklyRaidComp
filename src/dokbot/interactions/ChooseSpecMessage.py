from dokbot.DokBotContext import DokBotContext
from dokbot.interactions.EmojiInteractionMessage import EmojiInteractionMessage
from logic.enums.Class import Class


class ChooseSpecMessage(EmojiInteractionMessage):
    def __init__(self, ctx: DokBotContext, klass: Class):
        self.klass = klass
        content = "Please select the specialisation of your character"
        icons = [klass.get_icon(spec[0]) for spec in klass.specs]
        super().__init__(ctx=ctx, content=content, reactions=icons)

    async def get_response(self):
        spec = await super(ChooseSpecMessage, self).get_response()
        spec = spec.split('_')[0]
        return spec
