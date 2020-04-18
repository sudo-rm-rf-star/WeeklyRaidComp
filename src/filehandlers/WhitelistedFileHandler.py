from src.disc.ServerUtils import get_members_for_role
from src.common.Constants import WHITELISTED_FILE, WHITELISTED_RANK
from src.common.Utils import parse_name
import json


def update_whitelisted(client):
    whitelisted_members = get_members_for_role(client, WHITELISTED_RANK)
    with open(WHITELISTED_FILE, encoding='utf-8', mode='w+') as whitelisted_file:
        json.dump([parse_name(member.nick if member.nick else member.name) for member in whitelisted_members], whitelisted_file)


def get_whitelisted():
    with open(WHITELISTED_FILE, encoding='utf-8') as whitelisted_file:
        return json.load(whitelisted_file)
