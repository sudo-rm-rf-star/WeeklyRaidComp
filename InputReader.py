def read_signups():

def read_signups_helper(characters, kruisvaarders):
    cur_status = None
    characters = []
    for row in open(signups_filename, 'r').readlines():
        row = row.strip()
        status = read_status(row)
        if status:
            cur_status = status
        else:
            charname = read_signup(row)
            if not charname in characters:
                print(f"Please add {row} to the {characters_filename}.")
                exit(1)
            if not charname in kruisvaarders:
                print(f"Please add {row} to the {kruisvaarders_filename}.")
                is_kruisvaarder = False
            else:
                is_kruisvaarder = bool(kruisvaarders[charname])

            wowclass, wowrole = characters[charname]
            character = Character(charname, wowclass, wowrole, is_kruisvaarder, cur_status)
            characters.append(character)
    return characters

def read_characters():
    chars = defaultdict()
    for row in [row.split() for row in open(characters_filename, 'r').readlines()]:
        chars[row[0].lower()] = (row[1], row[2])
    return chars

def read_kruisvaarders():
    chars = defaultdict()
    for row in [row.split() for row in open(kruisvaarders_filename, 'r').readlines()]:
        chars[row[0].lower()] = row[1]
    return chars
