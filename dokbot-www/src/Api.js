export default function Api() {

  //fetch("https://dokbot.pupu.be/api/raids/615919624034451470/Kruisvaarders/ml/1626629400")
  //    .then(response => response.json())
  //    .then(x => console.log(x));

  return {
    get_raid: (id) => ({
      "data": {
        "created_at": 1626340709,
        "guild_id": "615919624034451470",
        "is_open": true,
        "message_refs": [
          {
            "channel_id": "632234743215423512",
            "guild_id": "615919624034451470",
            "kwargs": "{\"for_raid_leaders\": false}",
            "message_id": "865160386298249216",
            "raid_name": "ml",
            "team_name": "Kruisvaarders",
            "timestamp": "1626629400.0",
            "user_id": null
          },
          {
            "channel_id": "701149790154522704",
            "guild_id": "615919624034451470",
            "kwargs": "{\"for_raid_leaders\": true}",
            "message_id": "865160389155225650",
            "raid_name": "ml",
            "team_name": "Kruisvaarders",
            "timestamp": "1626629400.0",
            "user_id": null
          },
          {
            "channel_id": "701149790154522704",
            "guild_id": "615919624034451470",
            "kwargs": "{\"for_raid_leaders\": true}",
            "message_id": "865615800135974952",
            "raid_name": "ml",
            "team_name": "Kruisvaarders",
            "timestamp": "1626629400.0",
            "user_id": null
          }
        ],
        "name": "ml",
        "roster": {
          "characters": [
            {
              "class": "MAGE",
              "created_at": 1623093520,
              "discord_id": 105013005124677630,
              "name": "Soep",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552497
                ],
                [
                  "Accept",
                  1626552497
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552497
                ]
              ],
              "spec": "Arcane"
            },
            {
              "class": "ROGUE",
              "created_at": 1623094910,
              "discord_id": 641992727659020300,
              "name": "Bledhil",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552473
                ],
                [
                  "Accept",
                  1626552473
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552473
                ]
              ],
              "spec": "Combat"
            },
            {
              "class": "SHAMAN",
              "created_at": 1623255321,
              "discord_id": 528688161753399300,
              "name": "Shampetter",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552450
                ],
                [
                  "Accept",
                  1626552450
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552450
                ]
              ],
              "spec": "Restoration"
            },
            {
              "class": "HUNTER",
              "created_at": 1626088925,
              "discord_id": 631544206527299600,
              "name": "Scroogé",
              "roster_statuses": [
                [
                  "Undecided",
                  1626340717
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626340717
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "WARRIOR",
              "created_at": 1623128374,
              "discord_id": 527433092521132000,
              "name": "Tankié",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552393
                ],
                [
                  "Accept",
                  1626552393
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552393
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "PRIEST",
              "created_at": 1623154461,
              "discord_id": 484055532605407200,
              "name": "Libera",
              "roster_statuses": [
                [
                  "Undecided",
                  1626395048
                ],
                [
                  "Decline",
                  1626395048
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626395048
                ],
                [
                  "Decline",
                  1626395048
                ]
              ],
              "spec": "Holy"
            },
            {
              "class": "WARLOCK",
              "created_at": 1623172395,
              "discord_id": 419227780949999600,
              "name": "Dotjé",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552527
                ],
                [
                  "Accept",
                  1626552527
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552527
                ]
              ],
              "spec": "Destruction"
            },
            {
              "class": "SHAMAN",
              "created_at": 1625195432,
              "discord_id": 626107072651591700,
              "name": "Khayami",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552456
                ],
                [
                  "Accept",
                  1626552456
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552456
                ]
              ],
              "spec": "Restoration"
            },
            {
              "class": "WARLOCK",
              "created_at": 1626085239,
              "discord_id": 650413720467669000,
              "name": "Olorun",
              "roster_statuses": [
                [
                  "Undecided",
                  1626340724
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626340724
                ]
              ],
              "spec": "Destruction"
            },
            {
              "class": "ROGUE",
              "created_at": 1624108423,
              "discord_id": 594992391048659000,
              "name": "Zeldrîs",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552288
                ],
                [
                  "Extra",
                  1626552288
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552288
                ]
              ],
              "spec": "Combat"
            },
            {
              "class": "PRIEST",
              "created_at": 1626085178,
              "discord_id": 455308431167848450,
              "name": "Bunnik",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552159
                ],
                [
                  "Extra",
                  1626552159
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552159
                ]
              ],
              "spec": "Shadow"
            },
            {
              "class": "PALADIN",
              "created_at": 1623263611,
              "discord_id": 422372246703702000,
              "name": "Valdr",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552562
                ],
                [
                  "Accept",
                  1626552562
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552562
                ]
              ],
              "spec": "Retribution"
            },
            {
              "class": "DRUID",
              "created_at": 1624106933,
              "discord_id": 329317046376595460,
              "name": "Nektor",
              "roster_statuses": [
                [
                  "Undecided",
                  1626342531
                ],
                [
                  "Decline",
                  1626342531
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626342531
                ],
                [
                  "Decline",
                  1626342531
                ]
              ],
              "spec": "Bear"
            },
            {
              "class": "WARRIOR",
              "created_at": 1623693725,
              "discord_id": 319418993184079900,
              "name": "Stonebreaker",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552546
                ],
                [
                  "Accept",
                  1626552546
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552546
                ]
              ],
              "spec": "Fury"
            },
            {
              "class": "PALADIN",
              "created_at": 1623069219,
              "discord_id": 229262793331703800,
              "name": "Dokk",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552383
                ],
                [
                  "Accept",
                  1626552383
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552383
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "SHAMAN",
              "created_at": 1624008335,
              "discord_id": 617734423055433700,
              "name": "Hexoffendér",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552297
                ],
                [
                  "Extra",
                  1626552297
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552297
                ]
              ],
              "spec": "Enhancement"
            },
            {
              "class": "MAGE",
              "created_at": 1624269840,
              "discord_id": 489351754400399360,
              "name": "Slaapkop",
              "roster_statuses": [
                [
                  "Accept",
                  1626552372
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552372
                ]
              ],
              "spec": "Frost"
            },
            {
              "class": "PRIEST",
              "created_at": 1623095123,
              "discord_id": 371051857616830460,
              "name": "Harmi",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552468
                ],
                [
                  "Accept",
                  1626552468
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552468
                ]
              ],
              "spec": "Discipline"
            },
            {
              "class": "WARLOCK",
              "created_at": 1623662879,
              "discord_id": 668061364576845800,
              "name": "Platvoet",
              "roster_statuses": [
                [
                  "Decline",
                  1626553552
                ]
              ],
              "signup_statuses": [
                [
                  "Decline",
                  1626553552
                ]
              ],
              "spec": "Destruction"
            },
            {
              "class": "DRUID",
              "created_at": 1623320768,
              "discord_id": 604789354749231100,
              "name": "Druantia",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552388
                ],
                [
                  "Accept",
                  1626552388
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552388
                ]
              ],
              "spec": "Bear"
            },
            {
              "class": "SHAMAN",
              "created_at": 1623351286,
              "discord_id": 365782620912484350,
              "name": "Thotbot",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552410
                ],
                [
                  "Accept",
                  1626552410
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552410
                ]
              ],
              "spec": "Elemental"
            },
            {
              "class": "DRUID",
              "created_at": 1625256634,
              "discord_id": 855356963947937800,
              "name": "Xania",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552435
                ],
                [
                  "Accept",
                  1626552435
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552435
                ]
              ],
              "spec": "Restoration"
            },
            {
              "class": "ROGUE",
              "created_at": 1623790421,
              "discord_id": 602620273526833200,
              "name": "Syrion",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552303
                ],
                [
                  "Extra",
                  1626552303
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552303
                ]
              ],
              "spec": "Combat"
            },
            {
              "class": "HUNTER",
              "created_at": 1623663104,
              "discord_id": 591349471846334500,
              "name": "Swagchamp",
              "roster_statuses": [
                [
                  "Undecided",
                  1626515300
                ],
                [
                  "Decline",
                  1626515300
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626515300
                ],
                [
                  "Decline",
                  1626515300
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "DRUID",
              "created_at": 1624122711,
              "discord_id": 117978992505520130,
              "name": "Tygrae",
              "roster_statuses": [
                [
                  "Undecided",
                  1626340739
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626340739
                ]
              ],
              "spec": "Bear"
            },
            {
              "class": "PALADIN",
              "created_at": 1623096975,
              "discord_id": 392361015133601800,
              "name": "Engoan",
              "roster_statuses": [
                [
                  "Extra",
                  1626557168
                ],
                [
                  "Decline",
                  1626557168
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626557168
                ],
                [
                  "Decline",
                  1626557168
                ]
              ],
              "spec": "Holy"
            },
            {
              "class": "PRIEST",
              "created_at": 1623188883,
              "discord_id": 295270348415303700,
              "name": "Marckus",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552342
                ],
                [
                  "Extra",
                  1626552342
                ]
              ],
              "signup_statuses": [
                [
                  "Tentative",
                  1626552342
                ]
              ],
              "spec": "Holy"
            },
            {
              "class": "HUNTER",
              "created_at": 1623276603,
              "discord_id": 279595069089120260,
              "name": "Nckkh",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552503
                ],
                [
                  "Accept",
                  1626552503
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552503
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "PRIEST",
              "created_at": 1623103703,
              "discord_id": 259756567711186940,
              "name": "Crohn",
              "roster_statuses": [
                [
                  "Undecided",
                  1626366981
                ],
                [
                  "Decline",
                  1626366981
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626366981
                ],
                [
                  "Decline",
                  1626366981
                ]
              ],
              "spec": "Holy"
            },
            {
              "class": "WARRIOR",
              "created_at": 1623135045,
              "discord_id": 253943342327398400,
              "name": "Fatoru",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552363
                ],
                [
                  "Extra",
                  1626552363
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552363
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "MAGE",
              "created_at": 1625431223,
              "discord_id": 254259466004987900,
              "name": "Quilix",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552405
                ],
                [
                  "Accept",
                  1626552405
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552405
                ]
              ],
              "spec": "Frost"
            },
            {
              "class": "PRIEST",
              "created_at": 1623493239,
              "discord_id": 237466774373662720,
              "name": "Shikaru",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552398
                ],
                [
                  "Accept",
                  1626552398
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552398
                ]
              ],
              "spec": "Shadow"
            },
            {
              "class": "MAGE",
              "created_at": 1623616890,
              "discord_id": 227373667275767800,
              "name": "Droeftoéter",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552314
                ],
                [
                  "Extra",
                  1626552314
                ]
              ],
              "signup_statuses": [
                [
                  "Tentative",
                  1626552314
                ]
              ],
              "spec": "Fire"
            },
            {
              "class": "MAGE",
              "created_at": 1623621816,
              "discord_id": 209594408406876160,
              "name": "Blinksome",
              "roster_statuses": [
                [
                  "Undecided",
                  1626514654
                ],
                [
                  "Decline",
                  1626514654
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626514654
                ]
              ],
              "spec": "Fire"
            },
            {
              "class": "DRUID",
              "created_at": 1623097421,
              "discord_id": 656190949684150300,
              "name": "Avelena",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552461
                ],
                [
                  "Accept",
                  1626552461
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552461
                ]
              ],
              "spec": "Restoration"
            },
            {
              "class": "WARLOCK",
              "created_at": 1623444779,
              "discord_id": 582301840260071400,
              "name": "Nabbe",
              "roster_statuses": [
                [
                  "Undecided",
                  1626466329
                ],
                [
                  "Decline",
                  1626466329
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626466329
                ],
                [
                  "Decline",
                  1626466329
                ]
              ],
              "spec": "Destruction"
            },
            {
              "class": "HUNTER",
              "created_at": 1623754021,
              "discord_id": 194394707168722940,
              "name": "Yodah",
              "roster_statuses": [
                [
                  "Undecided",
                  1626359410
                ],
                [
                  "Decline",
                  1626359410
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626359410
                ],
                [
                  "Decline",
                  1626359410
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "PALADIN",
              "created_at": 1623689205,
              "discord_id": 154686979768844300,
              "name": "Valystres",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552444
                ],
                [
                  "Accept",
                  1626552444
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552444
                ]
              ],
              "spec": "Holy"
            },
            {
              "class": "HUNTER",
              "created_at": 1625084528,
              "discord_id": 132083662635270140,
              "name": "Wurv",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552537
                ],
                [
                  "Accept",
                  1626552537
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552537
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "PALADIN",
              "created_at": 1623099060,
              "discord_id": 635044528125902800,
              "name": "Nichtrijder",
              "roster_statuses": [
                [
                  "Extra",
                  1626552838
                ]
              ],
              "signup_statuses": [
                [
                  "Tentative",
                  1626552838
                ],
                [
                  "Accept",
                  1626552838
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "DRUID",
              "created_at": 1623428742,
              "discord_id": 357257402204160000,
              "name": "Zaidin",
              "roster_statuses": [
                [
                  "Undecided",
                  1626357409
                ],
                [
                  "Decline",
                  1626357409
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626357409
                ],
                [
                  "Decline",
                  1626357409
                ]
              ],
              "spec": "Restoration"
            },
            {
              "class": "HUNTER",
              "created_at": 1624224248,
              "discord_id": 217426857677684740,
              "name": "Oedipus",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552517
                ],
                [
                  "Accept",
                  1626552517
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552517
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "PALADIN",
              "created_at": 1624828259,
              "discord_id": 413767285052932100,
              "name": "Mercerone",
              "roster_statuses": [
                [
                  "Undecided",
                  1626340834
                ],
                [
                  "Decline",
                  1626340834
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626340834
                ],
                [
                  "Decline",
                  1626340834
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "HUNTER",
              "created_at": 1624140237,
              "discord_id": 233705518743420930,
              "name": "Akuza",
              "roster_statuses": [
                [
                  "Undecided",
                  1626340763
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626340763
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "HUNTER",
              "created_at": 1623098566,
              "discord_id": 713161099251286100,
              "name": "Tcgxo",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552507
                ],
                [
                  "Accept",
                  1626552507
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552507
                ]
              ],
              "spec": "BeastMastery"
            },
            {
              "class": "WARLOCK",
              "created_at": 1623351255,
              "discord_id": 224750610719834100,
              "name": "Ethegrio",
              "roster_statuses": [
                [
                  "Undecided",
                  1626449153
                ],
                [
                  "Decline",
                  1626449153
                ]
              ],
              "signup_statuses": [
                [
                  "Unknown",
                  1626449153
                ]
              ],
              "spec": "Affliction"
            },
            {
              "class": "WARLOCK",
              "created_at": 1625640744,
              "discord_id": 242040222613897200,
              "name": "Gwaihirr",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552533
                ],
                [
                  "Accept",
                  1626552533
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552533
                ]
              ],
              "spec": "Destruction"
            },
            {
              "class": "PRIEST",
              "created_at": 1624907550,
              "discord_id": 692477928935522400,
              "name": "Nazguls",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552337
                ],
                [
                  "Extra",
                  1626552337
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552337
                ]
              ],
              "spec": "Holy"
            },
            {
              "class": "MAGE",
              "created_at": 1623094210,
              "discord_id": 228447732728201200,
              "name": "Vlammenzee",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552172
                ],
                [
                  "Extra",
                  1626552172
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552172
                ]
              ],
              "spec": "Fire"
            },
            {
              "class": "DRUID",
              "created_at": 1624194992,
              "discord_id": 210857501527244800,
              "name": "Queldor",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552330
                ],
                [
                  "Extra",
                  1626552330
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552330
                ]
              ],
              "spec": "Restoration"
            },
            {
              "class": "MAGE",
              "created_at": 1623659776,
              "discord_id": 144373556078313470,
              "name": "Darvon",
              "roster_statuses": [
                [
                  "Undecided",
                  1626449722
                ],
                [
                  "Extra",
                  1626449722
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626449722
                ]
              ],
              "spec": "Frost"
            },
            {
              "class": "ROGUE",
              "created_at": 1625747327,
              "discord_id": 339380837877415940,
              "name": "Amonet",
              "roster_statuses": [
                [
                  "Accept",
                  1626552554
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552554
                ]
              ],
              "spec": "Combat"
            },
            {
              "class": "PALADIN",
              "created_at": 1626207683,
              "discord_id": 225621422322614270,
              "name": "Drkz",
              "roster_statuses": [
                [
                  "Undecided",
                  1626437327
                ],
                [
                  "Decline",
                  1626437327
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626437327
                ],
                [
                  "Decline",
                  1626437327
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "WARRIOR",
              "created_at": 1625428827,
              "discord_id": 289020483544809500,
              "name": "Reckton",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552353
                ],
                [
                  "Extra",
                  1626552353
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552353
                ]
              ],
              "spec": "Protection"
            },
            {
              "class": "SHAMAN",
              "created_at": 1626355457,
              "discord_id": 231851561226076160,
              "name": "Mîqa",
              "roster_statuses": [
                [
                  "Undecided",
                  1626552424
                ],
                [
                  "Accept",
                  1626552424
                ]
              ],
              "signup_statuses": [
                [
                  "Accept",
                  1626552424
                ]
              ],
              "spec": "Restoration"
            }
          ]
        },
        "team_name": "Kruisvaarders",
        "timestamp": 1626629400,
        "updated_at": 1626557168
      }
    })
  }
}

/*
[
    {
      id: 123,
      title: "Magtheridon's Lair",
      size: 25,
      eventAt: new Date(2021, 7, 8, 19, 30),
      signups: [
        {
          name: "Druantia",
          class: "druid",
          spec: "feral",
          role: "tank"
        },
        {
          name: "Tankié",
          class: "warrior",
          spec: "protection",
          role: "tank"
        },
        {
          name: "Dokk",
          class: "paladin",
          spec: "protection",
          role: "tank"
        },
        {
          name: "Harmi",
          class: "priest",
          spec: "holy",
          role: "healer"
        },
        {
          name: "Shampetter",
          class: "shaman",
          spec: "restoration",
          role: "healer"
        },
        {
          name: "Bledhil",
          class: "rogue",
          spec: "combat",
          role: "melee_dps"
        },
        {
          name: "Nckkh",
          class: "hunter",
          spec: "beast_mastery",
          role: "ranged_dps"
        },
        {
          name: "Soep",
          class: "mage",
          spec: "arcane",
          role: "caster_dps"
        },
        {
          name: "Shikaru",
          class: "priest",
          spec: "shadow",
          role: "caster_dps"
        },
      ]
    }
  ]
*/