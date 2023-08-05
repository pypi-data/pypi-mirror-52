MAX_WIDTH = 26

text_words = {
    "Attack " : 	b"\xD6\x00",
    "Angel " : 	b"\xD6\x01",
    "After " : 	b"\xD6\x02",
    "Aura " : 	b"\xD6\x03",
    "Ankor " : 	b"\xD6\x04",
    "Black " : 	b"\xD6\x05",
    "Bill: " : 	b"\xD6\x06",
    "Crystal " : 	b"\xD6\x07",
    "City " : 	b"\xD6\x08",
    "Come " : 	b"\xD6\x09",
    "Condor's " : 	b"\xD6\x0A",
    "Change " : 	b"\xD6\x0B",
    "Dark " : 	b"\xD6\x0C",
    "Don't " : 	b"\xD6\x0D",
    "Diamond " : 	b"\xD6\x0E",
    "Drifting, " : 	b"\xD6\x0F",
    "Eric: " : 	b"\xD6\x10",
    "Edward " : 	b"\xD6\x11",
    "Even " : 	b"\xD6\x12",
    "Elder2f " : 	b"\xD6\x13",
    "Earth " : 	b"\xD6\x14",
    "Freedan's " : 	b"\xD6\x15",
    "Great " : 	b"\xD6\x16",
    "Grandma " : 	b"\xD6\x17",
    "Good. " : 	b"\xD6\x18",
    "Gold " : 	b"\xD6\x19",
    "Grandpa " : 	b"\xD6\x1A",
    "Hieroglyph " : 	b"\xD6\x1B",
    "Hey, " : 	b"\xD6\x1C",
    "It's " : 	b"\xD6\x1D",
    "Inca " : 	b"\xD6\x1E",
    "I'll " : 	b"\xD6\x1F",
    "I've " : 	b"\xD6\x20",
    "Itorie " : 	b"\xD6\x21",
    "Jewels " : 	b"\xD6\x22",
    "Jewels! " : 	b"\xD6\x23",
    "Just " : 	b"\xD6\x24",
    "Kara: " : 	b"\xD6\x25",
    "Kara " : 	b"\xD6\x26",
    "King " : 	b"\xD6\x27",
    "Knight " : 	b"\xD6\x28",
    "Karen's " : 	b"\xD6\x29",
    "Lilly: " : 	b"\xD6\x2A",
    "Let's " : 	b"\xD6\x2B",
    "Lilly " : 	b"\xD6\x2C",
    "Lola's " : 	b"\xD6\x2D",
    "Lola: " : 	b"\xD6\x2E",
    "Mystery " : 	b"\xD6\x2F",
    "Maybe " : 	b"\xD6\x30",
    "Moon " : 	b"\xD6\x31",
    "Man: " : 	b"\xD6\x32",
    "Morris's " : 	b"\xD6\x33",
    "Melody " : 	b"\xD6\x34",
    "Morris: " : 	b"\xD6\x35",
    "Neil: " : 	b"\xD6\x36",
    "Neil's " : 	b"\xD6\x37",
    "Only " : 	b"\xD6\x38",
    "Once " : 	b"\xD6\x39",
    "Oink " : 	b"\xD6\x3A",
    "Please " : 	b"\xD6\x3B",
    "Psycho " : 	b"\xD6\x3C",
    "People " : 	b"\xD6\x3D",
    "Prayer " : 	b"\xD6\x3E",
    "Pyramid " : 	b"\xD6\x3F",
    "Purification " : 	b"\xD6\x40",
    "Plate " : 	b"\xD6\x41",
    "Quit " : 	b"\xD6\x42",
    "Rob: " : 	b"\xD6\x43",
    "Rolek " : 	b"\xD6\x44",
    "Soldier: " : 	b"\xD6\x45",
    "Strange " : 	b"\xD6\x46",
    "South " : 	b"\xD6\x47",
    "Statue " : 	b"\xD6\x48",
    "Somehow " : 	b"\xD6\x49",
    "Sometimes " : 	b"\xD6\x4A",
    "Something " : 	b"\xD6\x4B",
    "Shadow's " : 	b"\xD6\x4C",
    "Someone " : 	b"\xD6\x4D",
    "This " : 	b"\xD6\x4E",
    "Will: " : 	b"\xD6\x4F",
    "There's " : 	b"\xD6\x50",
    "Will's " : 	b"\xD6\x51",
    "There " : 	b"\xD6\x52",
    "That's " : 	b"\xD6\x53",
    "Tower " : 	b"\xD6\x54",
    "They " : 	b"\xD6\x55",
    "Then " : 	b"\xD6\x56",
    "Trip " : 	b"\xD6\x57",
    "Thank " : 	b"\xD6\x58",
    "Take " : 	b"\xD6\x59",
    "Will. " : 	b"\xD6\x5A",
    "That " : 	b"\xD6\x5B",
    "Will, " : 	b"\xD6\x5C",
    "They're " : 	b"\xD6\x5D",
    "These " : 	b"\xD6\x5E",
    "Vampire " : 	b"\xD6\x5F",
    "Village. " : 	b"\xD6\x60",
    "When " : 	b"\xD6\x61",
    "What " : 	b"\xD6\x62",
    "Well, " : 	b"\xD6\x63",
    "What's " : 	b"\xD6\x64",
    "Where " : 	b"\xD6\x65",
    "Woman: " : 	b"\xD6\x66",
    "You've " : 	b"\xD6\x67",
    "Your " : 	b"\xD6\x68",
    "You're " : 	b"\xD6\x69",
    "Yes, " : 	b"\xD6\x6A",
    "about " : 	b"\xD6\x6B",
    "anything " : 	b"\xD6\x6C",
    "around " : 	b"\xD6\x6D",
    "another " : 	b"\xD6\x6E",
    "ancient " : 	b"\xD6\x6F",
    "been " : 	b"\xD6\x70",
    "become " : 	b"\xD6\x71",
    "body " : 	b"\xD6\x72",
    "back " : 	b"\xD6\x73",
    "before " : 	b"\xD6\x74",
    "brought " : 	b"\xD6\x75",
    "beautiful " : 	b"\xD6\x76",
    "being " : 	b"\xD6\x77",
    "can't " : 	b"\xD6\x78",
    "come " : 	b"\xD6\x79",
    "could " : 	b"\xD6\x7A",
    "comet " : 	b"\xD6\x7B",
    "company " : 	b"\xD6\x7C",
    "children " : 	b"\xD6\x7D",
    "constellation " : 	b"\xD6\x7E",
    "changed " : 	b"\xD6\x7F",
    "came " : 	b"\xD6\x80",
    "coming " : 	b"\xD6\x81",
    "don't " : 	b"\xD6\x82",
    "didn't " : 	b"\xD6\x83",
    "doesn't " : 	b"\xD6\x84",
    "distant " : 	b"\xD6\x85",
    "different " : 	b"\xD6\x86",
    "demons " : 	b"\xD6\x87",
    "destroy " : 	b"\xD6\x88",
    "everyone " : 	b"\xD6\x89",
    "explorer " : 	b"\xD6\x8A",
    "everyone's " : 	b"\xD6\x8B",
    "enemies " : 	b"\xD6\x8C",
    "exposed " : 	b"\xD6\x8D",
    "from " : 	b"\xD6\x8E",
    "found " : 	b"\xD6\x8F",
    "find " : 	b"\xD6\x90",
    "feel " : 	b"\xD6\x91",
    "father's " : 	b"\xD6\x92",
    "going " : 	b"\xD6\x93",
    "good " : 	b"\xD6\x94",
    "great " : 	b"\xD6\x95",
    "ground " : 	b"\xD6\x96",
    "give " : 	b"\xD6\x97",
    "have " : 	b"\xD6\x98",
    "heard " : 	b"\xD6\x99",
    "human " : 	b"\xD6\x9A",
    "hear " : 	b"\xD6\x9B",
    "huge " : 	b"\xD6\x9C",
    "happened " : 	b"\xD6\x9D",
    "hieroglyph " : 	b"\xD6\x9E",
    "it's " : 	b"\xD6\x9F",
    "inventory " : 	b"\xD6\xA0",
    "into " : 	b"\xD6\xA1",
    "inside " : 	b"\xD6\xA2",
    "just " : 	b"\xD6\xA3",
    "know " : 	b"\xD6\xA4",
    "like " : 	b"\xD6\xA5",
    "long " : 	b"\xD6\xA6",
    "little " : 	b"\xD6\xA7",
    "light " : 	b"\xD6\xA8",
    "look " : 	b"\xD6\xA9",
    "looks " : 	b"\xD6\xAA",
    "looking " : 	b"\xD6\xAB",
    "leave " : 	b"\xD6\xAC",
    "labor " : 	b"\xD6\xAD",
    "left " : 	b"\xD6\xAE",
    "live " : 	b"\xD6\xAF",
    "life " : 	b"\xD6\xB0",
    "living " : 	b"\xD6\xB1",
    "must " : 	b"\xD6\xB2",
    "made " : 	b"\xD6\xB3",
    "melody " : 	b"\xD6\xB4",
    "move " : 	b"\xD6\xB5",
    "many " : 	b"\xD6\xB6",
    "more " : 	b"\xD6\xB7",
    "matter " : 	b"\xD6\xB8",
    "nothing " : 	b"\xD6\xB9",
    "need " : 	b"\xD6\xBA",
    "never " : 	b"\xD6\xBB",
    "next " : 	b"\xD6\xBC",
    "other " : 	b"\xD6\xBD",
    "over " : 	b"\xD6\xBE",
    "outside " : 	b"\xD6\xBF",
    "original " : 	b"\xD6\xC0",
    "people " : 	b"\xD6\xC1",
    "power " : 	b"\xD6\xC2",
    "present. " : 	b"\xD6\xC3",
    "playing " : 	b"\xD6\xC4",
    "raised " : 	b"\xD6\xC5",
    "right-hand " : 	b"\xD6\xC6",
    "strange " : 	b"\xD6\xC7",
    "something " : 	b"\xD6\xC8",
    "statue " : 	b"\xD6\xC9",
    "should " : 	b"\xD6\xCA",
    "started " : 	b"\xD6\xCB",
    "seems " : 	b"\xD6\xCC",
    "same " : 	b"\xD6\xCD",
    "such " : 	b"\xD6\xCE",
    "someone " : 	b"\xD6\xCF",
    "some " : 	b"\xD6\xD0",
    "save " : 	b"\xD6\xD1",
    "statues " : 	b"\xD6\xD2",
    "still " : 	b"\xD6\xD3",
    "said " : 	b"\xD6\xD4",
    "stands " : 	b"\xD6\xD5",
    "this " : 	b"\xD6\xD6",
    "that " : 	b"\xD6\xD7",
    "thought " : 	b"\xD6\xD8",
    "there " : 	b"\xD6\xD9",
    "think " : 	b"\xD6\xDA",
    "there's " : 	b"\xD6\xDB",
    "through " : 	b"\xD6\xDC",
    "tried " : 	b"\xD6\xDD",
    "terrible " : 	b"\xD6\xDE",
    "time " : 	b"\xD6\xDF",
    "things " : 	b"\xD6\xE0",
    "their " : 	b"\xD6\xE1",
    "town " : 	b"\xD6\xE2",
    "thing " : 	b"\xD6\xE3",
    "these " : 	b"\xD6\xE4",
    "temple " : 	b"\xD6\xE5",
    "them " : 	b"\xD6\xE6",
    "take " : 	b"\xD6\xE7",
    "turned, " : 	b"\xD6\xE8",
    "understand " : 	b"\xD6\xE9",
    "under " : 	b"\xD6\xEA",
    "underwater " : 	b"\xD6\xEB",
    "village " : 	b"\xD6\xEC",
    "very " : 	b"\xD6\xED",
    "voice " : 	b"\xD6\xEE",
    "will " : 	b"\xD6\xEF",
    "with " : 	b"\xD6\xF0",
    "want " : 	b"\xD6\xF1",
    "were " : 	b"\xD6\xF2",
    "would " : 	b"\xD6\xF3",
    "where " : 	b"\xD6\xF4",
    "world " : 	b"\xD6\xF5",
    "when " : 	b"\xD6\xF6",
    "what " : 	b"\xD6\xF7",
    "without " : 	b"\xD6\xF8",
    "wonder " : 	b"\xD6\xF9",
    "won't " : 	b"\xD6\xFA",
    "wouldn't " : 	b"\xD6\xFB",
    "wanted " : 	b"\xD6\xFC",
    "waiting " : 	b"\xD6\xFD",
    "your " : 	b"\xD6\xFE",
    "you're " : 	b"\xD6\xFF",
    "1994 " : 	b"\xD7\x00",
    "Actually, " : 	b"\xD7\x01",
    "Button " : 	b"\xD7\x02",
    "Buttons " : 	b"\xD7\x03",
    "Back " : 	b"\xD7\x04",
    "Child: " : 	b"\xD7\x05",
    "Defeating " : 	b"\xD7\x06",
    "Didn't " : 	b"\xD7\x07",
    "Desert " : 	b"\xD7\x08",
    "Erasquez: " : 	b"\xD7\x09",
    "Elder " : 	b"\xD7\x0A",
    "Earth's " : 	b"\xD7\x0B",
    "Eric's " : 	b"\xD7\x0C",
    "Everybody " : 	b"\xD7\x0D",
    "Flute: " : 	b"\xD7\x0E",
    "First " : 	b"\xD7\x0F",
    "Firebird, " : 	b"\xD7\x10",
    "From " : 	b"\xD7\x11",
    "Gaia, " : 	b"\xD7\x12",
    "Gorgon " : 	b"\xD7\x13",
    "Have " : 	b"\xD7\x14",
    "Hey! " : 	b"\xD7\x15",
    "Istar's " : 	b"\xD7\x16",
    "Ishtar's " : 	b"\xD7\x17",
    "Lilly's " : 	b"\xD7\x18",
    "Larai " : 	b"\xD7\x19",
    "Looking " : 	b"\xD7\x1A",
    "Main " : 	b"\xD7\x1B",
    "Man's " : 	b"\xD7\x1C",
    "Memory " : 	b"\xD7\x1D",
    "Mountain " : 	b"\xD7\x1E",
    "Morris " : 	b"\xD7\x1F",
    "Many " : 	b"\xD7\x20",
    "Native " : 	b"\xD7\x21",
    "Native's " : 	b"\xD7\x22",
    "Neil " : 	b"\xD7\x23",
    "Naska " : 	b"\xD7\x24",
    "Power " : 	b"\xD7\x25",
    "Prison " : 	b"\xD7\x26",
    "Play " : 	b"\xD7\x27",
    "Panther's " : 	b"\xD7\x28",
    "Rob's " : 	b"\xD7\x29",
    "Recently " : 	b"\xD7\x2A",
    "Restores " : 	b"\xD7\x2B",
    "Right " : 	b"\xD7\x2C",
    "Russian " : 	b"\xD7\x2D",
    "Rofsky " : 	b"\xD7\x2E",
    "Rearrange " : 	b"\xD7\x2F",
    "Special " : 	b"\xD7\x30",
    "Spin " : 	b"\xD7\x31",
    "Seaside " : 	b"\xD7\x32",
    "She's " : 	b"\xD7\x33",
    "Shall " : 	b"\xD7\x34",
    "Sorry " : 	b"\xD7\x35",
    "Select " : 	b"\xD7\x36",
    "Show " : 	b"\xD7\x37",
    "Soon " : 	b"\xD7\x38",
    "Will! " : 	b"\xD7\x39",
    "Will... " : 	b"\xD7\x3A",
    "Tell " : 	b"\xD7\x3B",
    "Uses " : 	b"\xD7\x3C",
    "Wind " : 	b"\xD7\x3D",
    "We'll " : 	b"\xD7\x3E",
    "We're " : 	b"\xD7\x3F",
    "With " : 	b"\xD7\x40",
    "We've " : 	b"\xD7\x41",
    "Wait " : 	b"\xD7\x42",
    "Watermia. " : 	b"\xD7\x43",
    "always " : 	b"\xD7\x44",
    "approaching " : 	b"\xD7\x45",
    "animals " : 	b"\xD7\x46",
    "almost " : 	b"\xD7\x47",
    "also " : 	b"\xD7\x48",
    "anything. " : 	b"\xD7\x49",
    "abolition " : 	b"\xD7\x4A",
    "breath " : 	b"\xD7\x4B",
    "birthday " : 	b"\xD7\x4C",
    "best " : 	b"\xD7\x4D",
    "bring " : 	b"\xD7\x4E",
    "bouquet " : 	b"\xD7\x4F",
    "better " : 	b"\xD7\x50",
    "behind " : 	b"\xD7\x51",
    "change " : 	b"\xD7\x52",
    "castle " : 	b"\xD7\x53",
    "called " : 	b"\xD7\x54",
    "comet's " : 	b"\xD7\x55",
    "condition. " : 	b"\xD7\x56",
    "care " : 	b"\xD7\x57",
    "door " : 	b"\xD7\x58",
    "destroyed " : 	b"\xD7\x59",
    "disappeared " : 	b"\xD7\x5A",
    "discovered " : 	b"\xD7\x5B",
    "dark " : 	b"\xD7\x5C",
    "ever " : 	b"\xD7\x5D",
    "elevator " : 	b"\xD7\x5E",
    "explorer. " : 	b"\xD7\x5F",
    "eyes " : 	b"\xD7\x60",
    "first " : 	b"\xD7\x61",
    "fish " : 	b"\xD7\x62",
    "followed " : 	b"\xD7\x63",
    "fountain " : 	b"\xD7\x64",
    "floor " : 	b"\xD7\x65",
    "finally " : 	b"\xD7\x66",
    "father " : 	b"\xD7\x67",
    "flower " : 	b"\xD7\x68",
    "forced " : 	b"\xD7\x69",
    "forget " : 	b"\xD7\x6A",
    "fate " : 	b"\xD7\x6B",
    "girl " : 	b"\xD7\x6C",
    "gets " : 	b"\xD7\x6D",
    "guess " : 	b"\xD7\x6E",
    "girl's " : 	b"\xD7\x6F",
    "house " : 	b"\xD7\x70",
    "hope " : 	b"\xD7\x71",
    "home " : 	b"\xD7\x72",
    "here " : 	b"\xD7\x73",
    "here. " : 	b"\xD7\x74",
    "home! " : 	b"\xD7\x75",
    "happen.... " : 	b"\xD7\x76",
    "houses " : 	b"\xD7\x77",
    "inventing " : 	b"\xD7\x78",
    "last " : 	b"\xD7\x79",
    "lost " : 	b"\xD7\x7A",
    "language. " : 	b"\xD7\x7B",
    "list " : 	b"\xD7\x7C",
    "life. " : 	b"\xD7\x7D",
    "laborer " : 	b"\xD7\x7E",
    "letter " : 	b"\xD7\x7F",
    "looked " : 	b"\xD7\x80",
    "lose " : 	b"\xD7\x81",
    "left-hand " : 	b"\xD7\x82",
    "mushrooms " : 	b"\xD7\x83",
    "make " : 	b"\xD7\x84",
    "mother " : 	b"\xD7\x85",
    "merchants " : 	b"\xD7\x86",
    "meet " : 	b"\xD7\x87",
    "most " : 	b"\xD7\x88",
    "only " : 	b"\xD7\x89",
    "ocean " : 	b"\xD7\x8A",
    "opened " : 	b"\xD7\x8B",
    "outskirts " : 	b"\xD7\x8C",
    "president " : 	b"\xD7\x8D",
    "please " : 	b"\xD7\x8E",
    "probably " : 	b"\xD7\x8F",
    "place " : 	b"\xD7\x90",
    "prison " : 	b"\xD7\x91",
    "pretty " : 	b"\xD7\x92",
    "palace " : 	b"\xD7\x93",
    "right " : 	b"\xD7\x94",
    "really " : 	b"\xD7\x95",
    "returned " : 	b"\xD7\x96",
    "running " : 	b"\xD7\x97",
    "ruins " : 	b"\xD7\x98",
    "right. " : 	b"\xD7\x99",
    "ruins, " : 	b"\xD7\x9A",
    "road " : 	b"\xD7\x9B",
    "rest " : 	b"\xD7\x9C",
    "stone " : 	b"\xD7\x9D",
    "seem " : 	b"\xD7\x9E",
    "scattered " : 	b"\xD7\x9F",
    "seemed " : 	b"\xD7\xA0",
    "softly " : 	b"\xD7\xA1",
    "soldiers " : 	b"\xD7\xA2",
    "shape " : 	b"\xD7\xA3",
    "since " : 	b"\xD7\xA4",
    "surprised " : 	b"\xD7\xA5",
    "sure " : 	b"\xD7\xA6",
    "seen " : 	b"\xD7\xA7",
    "shouldn't " : 	b"\xD7\xA8",
    "somewhere " : 	b"\xD7\xA9",
    "times " : 	b"\xD7\xAA",
    "they " : 	b"\xD7\xAB",
    "talk " : 	b"\xD7\xAC",
    "tell " : 	b"\xD7\xAD",
    "townspeople " : 	b"\xD7\xAE",
    "taken " : 	b"\xD7\xAF",
    "they're " : 	b"\xD7\xB0",
    "travelling " : 	b"\xD7\xB1",
    "trying " : 	b"\xD7\xB2",
    "turned " : 	b"\xD7\xB3",
    "temporary " : 	b"\xD7\xB4",
    "than " : 	b"\xD7\xB5",
    "then " : 	b"\xD7\xB6",
    "too, " : 	b"\xD7\xB7",
    "thousands " : 	b"\xD7\xB8",
    "turn " : 	b"\xD7\xB9",
    "treasure, " : 	b"\xD7\xBA",
    "used " : 	b"\xD7\xBB",
    "until " : 	b"\xD7\xBC",
    "village. " : 	b"\xD7\xBD",
    "vampire " : 	b"\xD7\xBE",
    "while " : 	b"\xD7\xBF",
    "water " : 	b"\xD7\xC0",
    "went " : 	b"\xD7\xC1",
    "wondered " : 	b"\xD7\xC2",
    "written " : 	b"\xD7\xC3",
    "woman " : 	b"\xD7\xC4",
    "wind " : 	b"\xD7\xC5",
    "years " : 	b"\xD7\xC6",
    "you. " : 	b"\xD7\xC7"
}

text_letters = {
    "?" : 	b"\x0D",
    "'" : 	b"\x0E",
    "0" : 	b"\x20",
    "1" : 	b"\x21",
    "2" : 	b"\x22",
    "3" : 	b"\x23",
    "4" : 	b"\x24",
    "5" : 	b"\x25",
    "6" : 	b"\x26",
    "7" : 	b"\x27",
    "8" : 	b"\x28",
    "9" : 	b"\x29",
    "." : 	b"\x2A",
    "," : 	b"\x2B",
    ">" : 	b"\x2C",
#    '"' : 	b"\x2D",
#    '"' : 	b"\x2E",
    ":" : 	b"\x2F",
    "A" : 	b"\x40",
    "B" : 	b"\x41",
    "C" : 	b"\x42",
    "D" : 	b"\x43",
    "E" : 	b"\x44",
    "F" : 	b"\x45",
    "G" : 	b"\x46",
    "H" : 	b"\x47",
    "I" : 	b"\x48",
    "J" : 	b"\x49",
    "K" : 	b"\x4A",
    "L" : 	b"\x4B",
    "M" : 	b"\x4C",
    "N" : 	b"\x4D",
    "O" : 	b"\x4E",
    "!" : 	b"\x4F",
    "P" : 	b"\x60",
    "Q" : 	b"\x61",
    "R" : 	b"\x62",
    "S" : 	b"\x63",
    "T" : 	b"\x64",
    "U" : 	b"\x65",
    "V" : 	b"\x66",
    "W" : 	b"\x67",
    "X" : 	b"\x68",
    "Y" : 	b"\x69",
    "Z" : 	b"\x6A",
    "/" : 	b"\x6B",
    "*" : 	b"\x6C",
    "-" : 	b"\x6D",
    "(" : 	b"\x6E",
    ")" : 	b"\x6F",
    "a" : 	b"\x80",
    "b" : 	b"\x81",
    "c" : 	b"\x82",
    "d" : 	b"\x83",
    "e" : 	b"\x84",
    "f" : 	b"\x85",
    "g" : 	b"\x86",
    "h" : 	b"\x87",
    "i" : 	b"\x88",
    "j" : 	b"\x89",
    "k" : 	b"\x8A",
    "l" : 	b"\x8B",
    "m" : 	b"\x8C",
    "n" : 	b"\x8D",
    "o" : 	b"\x8E",
    "p" : 	b"\xA0",
    "q" : 	b"\xA1",
    "r" : 	b"\xA2",
    "s" : 	b"\xA3",
    "t" : 	b"\xA4",
    "u" : 	b"\xA5",
    "v" : 	b"\xA6",
    "w" : 	b"\xA7",
    "x" : 	b"\xA8",
    "y" : 	b"\xA9",
    "z" : 	b"\xAA",
    "," : 	b"\xAB",
    " " : 	b"\xAC",
    "|" : 	b"\xCF"    # Prompts for advance
}

text_words_inv = {v: k for k, v in text_words.items()}
text_letters_inv = {v: k for k, v in text_letters.items()}

def get_text(addr,f,rom_offset=0):
    str_encoded = ""
    f.seek(addr+rom_offset)
    char = ""
    bytes = 0
    while char != b"\xC0" and char != b"\xCA":
        char = f.read(1)
        str_encoded += char
        bytes += 1

    str_decoded = ""
    i = 0
    while i < len(str_encoded):
        byte = str_encoded[i]
        i += 1
        if byte not in [b"\xD3",b"\xC0",b"\xCA"]:
            if byte in [b"\xD6",b"\xD7"]:
                word = byte + str_encoded[i]
                i += 1
                if word in text_words_inv:
                    str_decoded += text_words_inv[word]
                #else:
                    #print "WARNING: Word not recognized >>", word
            elif byte in text_letters_inv:
                str_decoded += text_letters_inv[byte]
            elif byte not in [b"\xcb"]:
                str_decoded += "?"
                #print "WARNING: Letter not recognized >>", byte

    #print str_decoded
    return [str_decoded, bytes]

def encode(unencoded_str,full_box=False):
    words = []
    word = ""
    i = 0
    while i < len(unencoded_str):
        char = unencoded_str[i]
        word += char
        if char == " " or i == len(unencoded_str)-1:
            words.append(word)
            word = ""
        i += 1

    #print words
    if full_box:
        str_encoded = b"\xd3"
    else:
        str_encoded = b""
    text_width = 0

    for word in words:
        if len(word) > MAX_WIDTH:
            print("ERROR: Word too long >>", word)
            return ""
        text_width += len(word)
        if text_width > MAX_WIDTH:
            str_encoded += b"\xCB"
            text_width = len(word)
        if word in text_words:
            str_encoded += text_words[word]
        else:
            i = 0
            while i < len(word):
                char = word[i]
                if char in text_letters:
                    str_encoded += text_letters[char]
                else:
                    str_encoded += b"\x0D"
                    print("WARNING: Character not recognized >>", char)
                i += 1

    if full_box:
        str_encoded += b"\xc0"

    #print str_encoded, len(str_encoded)
    return str_encoded
