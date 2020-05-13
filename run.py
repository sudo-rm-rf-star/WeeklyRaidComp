#!/usr/bin/python3

import sys
from pathlib import Path
cwd = Path(__file__).parent / 'src'
sys.path.append(str(cwd))
from client.DiscordBot import run

if __name__ == '__main__':
    run()
