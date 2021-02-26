from dokbot.interactions.TextInteractionMessage import TextInteractionMessage
from persistence.RaidEventsResource import RaidEventsResource
from exceptions.InvalidInputException import InvalidInputException
from dokbot.commands.raidteam.RaidTeamContext import RaidTeamContext
from dokbot.interactions.OptionInteraction import OptionInteraction
from utils.Constants import raid_names, DATE_FORMAT, TIME_FORMAT
from datetime import datetime

TRIES = 3


async def create_raid(ctx: RaidTeamContext):
    raid_name = await GetRaidNameMesage.interact(ctx)
    raid_date = await GetDateMessage.interact(ctx)
    raid_datetime = await GetDateTimeMessage.interact(ctx, date=raid_date)
    raid = RaidEventsResource().create_raid(raid_name=raid_name, raid_datetime=raid_datetime, guild_id=ctx.guild_id,
                                            team_name=ctx.team_name)
    await ctx.reply(f'Raid {raid} has been successfully created.')


class GetRaidNameMesage(OptionInteraction):
    def __init__(self, ctx: RaidTeamContext):
        content = "Please choose the name of the raid"
        options = raid_names.keys()
        super(GetRaidNameMesage, self).__init__(ctx=ctx, content=content, options=options)

    async def get_response(self) -> str:
        response = (await super(GetRaidNameMesage, self).get_response())
        try:
            return raid_names[response]
        except KeyError:
            raise InvalidInputException(f'{response} is not a valid raid name.')


class GetDateMessage(TextInteractionMessage):
    def __init__(self, ctx: RaidTeamContext):
        example = datetime.now().strftime(DATE_FORMAT)
        content = f"Please select the date for the raid, e.g. {example}"
        super(GetDateMessage, self).__init__(ctx=ctx, content=content)

    async def get_response(self):
        response = await super(GetDateMessage, self).get_response()
        date = datetime.strptime(response, DATE_FORMAT).date()
        if date < datetime.today().date():
            raise InvalidInputException(f"Date must be in future.")
        return date


class GetDateTimeMessage(TextInteractionMessage):
    def __init__(self, ctx: RaidTeamContext, date):
        example = datetime.now().strftime(TIME_FORMAT)
        content = f"Please select the time for the raid, e.g. {example}"
        self.date: datetime = date
        super(GetDateTimeMessage, self).__init__(ctx=ctx, content=content)

    async def get_response(self) -> datetime:
        response = await super(GetDateTimeMessage, self).get_response()
        time = datetime.strptime(response, TIME_FORMAT).time()
        dt = datetime.combine(self.date, time)
        if dt < datetime.now():
            raise InvalidInputException(f"Time must be in future.")
        return dt
