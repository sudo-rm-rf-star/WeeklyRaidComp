from src.exceptions.InternalBotException import InternalBotException
from src.exceptions.NotAuthorizedException import NotAuthorizedException
from src.disc.ServerUtils import get_user_by_id, get_channel
from src.commands.ArgParser import ArgParser
from src.common.Constants import DATETIMESEC_FORMAT, LOGS_CHANNEL
from src.common.Utils import from_datetime, now


class BotCommand:
    def __init__(self, name, subname, description, argformat, required_rank=None, allow_trough_approval=False):
        self.name = name
        self.subname = subname
        self.argformat = argformat
        self.argparser = ArgParser(argformat)
        self.description = description
        self.required_rank = required_rank
        self.allow_trough_approval = allow_trough_approval

    async def run(self, client, message, **kwargs):
        raise InternalBotException("Please specify logic for this command. Do not call this method directly.")

    async def call(self, client, message, argv):
        needs_approval = not self.check_authority(client, message.author)
        if needs_approval:
            raise InternalBotException(f"Sorry {message.author}, this code path still needs to be implemented...")

        kwargs = self.argparser.parse(argv)
        response = await self.run(client, message, **kwargs)
        if response:
            await message.author.send(content=response)
            await get_channel(client, LOGS_CHANNEL).send(content=f'{from_datetime(now(), DATETIMESEC_FORMAT)} - {message.author} - {message.content} - {response}')

    def check_authority(self, client, author):
        member = get_user_by_id(client, author.id)
        if self.required_rank and self.required_rank not in [role.name for role in member.roles]:
            if not self.allow_trough_approval:
                raise NotAuthorizedException(author, self.required_rank)
            return False
        return True
