import binascii, hmac, logging, os, random, tempfile, json, copy
from typing import BinaryIO

from .patch import Patch
from .classes import World
from .quintet_comp import compress as qt_compress
from .quintet_text import encode as qt_encode
from .errors import FileNotFoundError, OffsetError
from .models.randomizer_data import RandomizerData
from .models.enums.difficulty import Difficulty
from .models.enums.goal import Goal
from .models.enums.logic import Logic
from .models.enums.enemizer import Enemizer
from .models.enums.start_location import StartLocation

VERSION = "2.3.0"

KARA_EDWARDS = 1
KARA_MINE = 2
KARA_ANGEL = 3
KARA_KRESS = 4
KARA_ANKORWAT = 5

GEMS_EASY = 35
GEMS_NORMAL = 40
GEMS_HARD = 50

INV_FULL = b"\x5c\x8e\xc9\x80"
FORCE_CHANGE = b"\x22\x30\xfd\x88"

OUTPUT_FOLDER: str = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep + ".." + os.path.sep + "data" + os.path.sep + "output" + os.path.sep
BIN_PATH: str = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "bin" + os.path.sep


def __get_data_file__(data_filename: str) -> BinaryIO:
    path = BIN_PATH + data_filename
    return open(path, "rb")


def generate_filename(settings: RandomizerData, extension: str):
    def getDifficulty(difficulty):
        if difficulty.value == Difficulty.EASY.value:
            return "_easy"
        if difficulty.value == Difficulty.NORMAL.value:
            return "_normal"
        if difficulty.value == Difficulty.HARD.value:
            return "_hard"
        if difficulty.value == Difficulty.EXTREME.value:
            return "_extreme"

    def getGoal(goal, statues):
        if goal.value is Goal.DARK_GAIA.value:
            return "_DG" + statues[0]
        if goal.value is Goal.RED_JEWEL_HUNT.value:
            return "_RJ"

    def getLogic(logic):
        if logic.value == Logic.COMPLETABLE.value:
            return "_C"
        if logic.value == Logic.BEATABLE.value:
            return "_B"
        if logic.value == Logic.CHAOS.value:
            return "_X"

    def getStartingLocation(start_location):
        if start_location.value == StartLocation.SOUTH_CAPE.value:
            return ""
        if start_location.value == StartLocation.SAFE.value:
            return "_ss"
        if start_location.value == StartLocation.UNSAFE.value:
            return "_su"
        if start_location.value == StartLocation.FORCED_UNSAFE.value:
            return "_sf"

    def getEnemizer(enemizer):
        if enemizer.value == Enemizer.NONE.value:
            return ""
        if enemizer.value == Enemizer.BALANCED.value:
            return "_eb"
        if enemizer.value == Enemizer.LIMITED.value:
            return "_el"
        if enemizer.value == Enemizer.FULL.value:
            return "_ef"
        if enemizer.value == Enemizer.INSANE.value:
            return "_ei"

    def getSwitch(switch, param):
        if switch:
            return "_" + param
        return ""

    filename = "IoGR_v" + VERSION
    filename += getDifficulty(settings.difficulty)
    filename += getGoal(settings.goal, settings.statues)
    filename += getLogic(settings.logic)
    filename += getStartingLocation(settings.start_location)
    filename += getSwitch(settings.firebird, "f")
    filename += getSwitch(settings.ohko, "ohko")
    filename += getEnemizer(settings.enemizer)
    filename += "_" + str(settings.seed)
    filename += "."
    filename += extension

    return filename


class Randomizer:
    offset: int = 0
    statues_required = 0
    current_position = 0

    def __init__(self, rom_path: str):
        self.rom_path = rom_path
        self.output_folder = os.path.dirname(rom_path) + os.path.sep + "iogr" + os.path.sep

        data_file = open(self.rom_path, "rb")
        self.original_rom_data = data_file.read()
        data_file.close()

        log_file_path = os.path.dirname(rom_path) + os.path.sep + "iogr" + os.path.sep + "logs" + os.path.sep + "app.log"
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))

        logging.basicConfig(filename=log_file_path, filemode='w', format='%(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger("IOGR")

    def generate_rom(self, filename: str, settings: RandomizerData):
        patch = self.__generate_patch__()
        rom_offset = self.__get_offset__(patch)
        
        random.seed(settings.seed)
        statues_required = self.__get_required_statues__(settings)
        mode = settings.difficulty.value
        
        ##########################################################################
        #                             Early Firebird
        ##########################################################################
        # Write new Firebird logic into unused memory location
        f_firebird = open(BIN_PATH + "02f0c0_firebird.bin", "rb")
        self.seek(patch,  int("2f0c0", 16) + rom_offset)
        self.write(patch, f_firebird.read())
        f_firebird.close()

        if settings.firebird == 1:
            # Change firebird logic
            # Requires Shadow's form, Crystal Ring (switch #$3e) and Kara rescued (switch #$8a)
            self.seek(patch,  int("2cd07", 16) + rom_offset)
            self.write(patch, b"\x4c\xc0\xf0\xea\xea\xea")
            self.seek(patch,  int("2cd88", 16) + rom_offset)
            self.write(patch, b"\x4c\xe0\xf0\xea\xea\xea")
            self.seek(patch,  int("2ce06", 16) + rom_offset)
            self.write(patch, b"\x4c\x00\xf1\xea\xea\xea")
            self.seek(patch,  int("2ce84", 16) + rom_offset)
            self.write(patch, b"\x4c\x20\xf1\xea\xea\xea")

            # Load firebird assets into every map
            self.seek(patch,  int("3e03a", 16) + rom_offset)
            self.write(patch, b"\x80\x00")
            self.seek(patch,  int("eaf0", 16) + rom_offset)
            self.write(patch, b"\x20\xa0\xf4\xea\xea")
            self.seek(patch,  int("f4a0", 16) + rom_offset)
            self.write(patch, b"\x02\x3b\x71\xb2\xf4\x80\xa9\x00\x10\x04\x12\x60")
            self.seek(patch,  int("f4b0", 16) + rom_offset)
            self.write(patch, b"\x02\xc1\xad\xd4\x0a\xc9\x02\x00\xf0\x01\x6b\x02\x36\x02\x39\x80\xef")

        ##########################################################################
        #                            Modify ROM Header
        ##########################################################################
        # New game title
        self.seek(patch,  int("ffd1", 16) + rom_offset)
        self.write(patch, b"\x52\x41\x4E\x44\x4F")

        # Put randomizer hash code on start screen
        self.seek(patch, int("1da4c", 16) + rom_offset)
        self.write(patch, b"\x52\x41\x4E\x44\x4F\x90\x43\x4F\x44\x45\x90")

        hash_str = filename
        h = hmac.new(bytes(settings.seed), hash_str.encode())
        hash = h.digest()

        hash_dict = [b"\x20", b"\x21", b"\x28", b"\x29", b"\x2a", b"\x2b", b"\x2c", b"\x2d", b"\x2e", b"\x2f", b"\x30", b"\x31", b"\x32", b"\x33"]
        hash_dict += [b"\x34", b"\x35", b"\x36", b"\x37", b"\x38", b"\x39", b"\x3a", b"\x3b", b"\x3c", b"\x3d", b"\x3e", b"\x3f", b"\x42", b"\x43"]
        hash_dict += [b"\x44", b"\x46", b"\x47", b"\x48", b"\x4a", b"\x4b", b"\x4c", b"\x4d", b"\x4e", b"\x50", b"\x51", b"\x52", b"\x53", b"\x54"]
        hash_dict += [b"\x56", b"\x57", b"\x58", b"\x59", b"\x5a", b"\x5b", b"\x5c", b"\x5d", b"\x5e", b"\x5f", b"\x7c", b"\x80", b"\x81"]

        hash_len = len(hash_dict)

        i = 0
        hash_final = b""
        while i < 6:
            key = hash[i] % hash_len
            hash_final += hash_dict[key]
            i += 1

        # print binascii.hexlify(hash_final)
        self.seek(patch,  int("1da57", 16) + rom_offset)
        self.write(patch, hash_final)

        ##########################################################################
        #                           Negate useless switches
        #                 Frees up switches for the randomizer's use
        ##########################################################################
        self.seek(patch,  int("48a03", 16) + rom_offset)  # Switch 17 - Enter Seth's house
        self.write(patch, b"\x10")
        self.seek(patch,  int("4bca9", 16) + rom_offset)  # Switch 18 - Enter Will's house (1/2)
        self.write(patch, b"\x10")
        self.seek(patch,  int("4bccc", 16) + rom_offset)  # Switch 18 - Enter Will's house (2/2)
        self.write(patch, b"\x10")
        self.seek(patch,  int("4bcda", 16) + rom_offset)  # Switch 19 - Enter Lance's house
        self.write(patch, b"\x10")
        self.seek(patch,  int("4bce8", 16) + rom_offset)  # Switch 20 - Enter Erik's house
        self.write(patch, b"\x10")
        self.seek(patch, int("4be3d", 16) + rom_offset)  # Switch 21 - Enter seaside cave
        self.write(patch, b"\x10")
        self.seek(patch, int("4bcf6", 16) + rom_offset)  # Switch 23 - Complete seaside cave events
        self.write(patch, b"\x10")
        self.seek(patch, int("9bf95", 16) + rom_offset)  # Switch 58 - First convo with Lilly
        self.write(patch, b"\x10")
        self.seek(patch, int("4928a", 16) + rom_offset)  # Switch 62 - First convo with Lola (1/2)
        self.write(patch, b"\x10")
        self.seek(patch, int("49873", 16) + rom_offset)  # Switch 62 - First convo with Lola (1/2)
        self.write(patch, b"\x10")
        self.seek(patch, int("4e933", 16) + rom_offset)  # Switch 65 - Hear Elder's voice
        self.write(patch, b"\x10")
        self.seek(patch, int("58a29", 16) + rom_offset)  # Switch 78 - Talk to Gold Ship queen
        self.write(patch, b"\x10")
        self.seek(patch, int("4b067", 16) + rom_offset)
        self.write(patch, b"\x10\x00")
        self.seek(patch, int("4b465", 16) + rom_offset)
        self.write(patch, b"\x10\x00")
        self.seek(patch, int("4b8b6", 16) + rom_offset)
        self.write(patch, b"\x10\x00")
        self.seek(patch, int("686fa", 16) + rom_offset)  # Switch 111 - meet Lilly at Seaside Palace
        self.write(patch, b"\x10")
        self.seek(patch, int("78d76", 16) + rom_offset)
        self.write(patch, b"\x10")
        self.seek(patch, int("78d91", 16) + rom_offset)
        self.write(patch, b"\x10")
        self.seek(patch, int("7d7b1", 16) + rom_offset)  # Switch 159 - Mt. Kress on map
        self.write(patch, b"\x10")

        ##########################################################################
        #                           Update map headers
        ##########################################################################
        f_mapdata = open(BIN_PATH + "0d8000_mapdata.bin", "rb")
        self.seek(patch, int("d8000", 16) + rom_offset)
        self.write(patch, f_mapdata.read())
        f_mapdata.close

        if mode == 0:
            addr = self.find(patch, b"\x00\x07\x00\x02\x01", int("d8000", 16) + rom_offset)
            self.seek(patch, addr)
            self.write(patch, b"\x00\x09")
            addr = self.find(patch, b"\x00\x09\x00\x02\x08", int("d8000", 16) + rom_offset)
            self.seek(patch, addr)
            self.write(patch, b"\x00\x07")

        ##########################################################################
        #                        Update treasure chest data
        ##########################################################################
        # Remove fanfares from treasure chests
        f_chests = open(BIN_PATH + "01afa6_chests.bin", "rb")
        self.seek(patch, int("1afa6", 16) + rom_offset)
        self.write(patch, f_chests.read())
        f_chests.close

        # Update item acquisition messages and add messages for new items (29-2f)
        f_acquisition = open(BIN_PATH + "01fd24_acquisition.bin", "rb")
        self.seek(patch, int("1fd24", 16) + rom_offset)
        self.write(patch, f_acquisition.read())
        f_acquisition.close

        ##########################################################################
        #                            Update item events
        #    Adds new items that increase HP, DEF, STR and improve abilities
        ##########################################################################
        # Add pointers for new items @38491
        self.seek(patch, int("38491", 16) + rom_offset)
        self.write(patch, b"\x6f\x9f\x91\x9f\x1d\x88\x3a\x88\x5f\x88\x90\x9d\xd0\x9d")

        # Add start menu descriptions for new items
        f_startmenu = open(BIN_PATH + "01dabf_startmenu.bin", "rb")
        self.seek(patch, int("1dabf", 16) + rom_offset)
        self.write(patch, f_startmenu.read())
        f_startmenu.close
        f_itemdesc = open(BIN_PATH + "01e132_itemdesc.bin", "rb")
        self.seek(patch, int("1e132", 16) + rom_offset)
        self.write(patch, f_itemdesc.read())
        f_itemdesc.close

        # Update sprites for new items - first new item starts @108052, 7 new items
        # Points all items to unused sprite for item 4c ("76 83" in address table)
        self.seek(patch, int("108052", 16) + rom_offset)
        self.write(patch, b"\x76\x83\x76\x83\x76\x83\x76\x83\x76\x83\x76\x83\x76\x83")

        # Update item removal restriction flags
        self.seek(patch, int("1e12a", 16) + rom_offset)
        self.write(patch, b"\x9f\xff\x97\x37\xb0\x01")

        # Write STR, Psycho Dash, and Dark Friar upgrade items
        # Replaces code for item 05 - Inca Melody @3881d
        f_item05 = open(BIN_PATH + "03881d_item05.bin", "rb")
        self.seek(patch, int("3881d", 16) + rom_offset)
        self.write(patch, f_item05.read())
        f_item05.close

        # Modify Prison Key, now is destroyed when used
        self.seek(patch, int("385d4", 16) + rom_offset)
        self.write(patch, b"\x0a\x17\x0c\x18")
        self.seek(patch, int("385fe", 16) + rom_offset)
        self.write(patch, b"\x02\xd5\x02\x60")

        # Modify Lola's Melody, now is destroyed when used and only works in Itory
        f_item09 = open(BIN_PATH + "038bf5_item09.bin", "rb")
        self.seek(patch, int("38bf5", 16) + rom_offset)
        self.write(patch, f_item09.read())
        f_item09.close
        self.seek(patch, int("38bbc", 16) + rom_offset)
        self.write(patch, b"\x00")
        self.seek(patch, int("38bc1", 16) + rom_offset)
        self.write(patch, b"\x00")

        # Modify code for Memory Melody to heal Neil's memory
        f_item0d = open(BIN_PATH + "038f17_item0d.bin", "rb")
        self.seek(patch, int("38f17", 16) + rom_offset)
        self.write(patch, f_item0d.read())
        f_item0d.close

        # Modify Magic Dust, alters switch set and text
        self.seek(patch, int("393c3", 16) + rom_offset)
        self.write(patch, b"\x8a")

        # Modify Blue Journal, functions as an in-game tutorial
        self.seek(patch, int("3943b", 16) + rom_offset)
        self.write(patch, b"\xf0\x94")
        self.seek(patch, int("39440", 16) + rom_offset)
        self.write(patch, b"\x10\xf2")
        self.seek(patch, int("39445", 16) + rom_offset)
        self.write(patch, b"\x00\xf8")
        self.seek(patch, int("3944a", 16) + rom_offset)
        self.write(patch, b"\x00\xfb")

        self.seek(patch, int("3944e", 16) + rom_offset)
        self.write(patch, b"\xce" + qt_encode("       Welcome to") + b"\xcb\xcb" + qt_encode("  Bagu's Super-Helpful"))
        self.write(patch, b"\xcb" + qt_encode("  In-Game Tutorial!(TM)|"))
        self.write(patch, qt_encode("Whadaya wanna know about?") + b"\xcb" + qt_encode(" Beating the Game") + b"\xcb")
        self.write(patch, qt_encode(" Exploring the World") + b"\xcb" + qt_encode(" What If I'm Stuck?") + b"\xca")

        self.seek(patch, int("394f0", 16) + rom_offset)
        self.write(patch, b"\xce" + qt_encode("He closed the journal.") + b"\xc0")

        self.seek(patch, int("3f210", 16) + rom_offset)
        if settings.goal.value == Goal.DARK_GAIA.value:
            self.write(patch, b"\xce" + qt_encode("BEATING THE GAME:       You must do the following two things to beat the game:|"))
            self.write(patch, qt_encode("1. RESCUE KARA          Kara is trapped in a painting! You need Magic Dust to free her.|"))
            self.write(patch, qt_encode("She can be in either Edward's Prison, Diamond Mine, Angel Village, Mt. Temple, or Ankor Wat.|"))
            self.write(patch, qt_encode("You can search for her yourself, or find Lance's Letter to learn where she can be found.|"))
            self.write(patch, qt_encode("Once you find Kara, use the Magic Dust on her portrait to free her.|"))
            self.write(patch, qt_encode("2. GATHER MYSTIC STATUES Each time you play the game, you may be required to gather Mystic Statues.|"))
            self.write(patch, qt_encode("Talk to the teacher in the South Cape classroom to find out which Statues you need.|"))
            self.write(patch, qt_encode("Statue 1 is in the Inca Ruins. You need the Wind Melody, Diamond Block, and both Incan Statues.|"))
            self.write(patch, qt_encode("Statue 2 is in the Sky Garden. You'll need all four Crystal Balls to fight the boss Viper.|"))
            self.write(patch, qt_encode("Statue 3 is in Mu. You need both Statues of Hope and both Rama Statues to fight the Vampires.|"))
            self.write(patch, qt_encode("Statue 4 is in the Great Wall. You need Spin Dash and Dark Friar to face the boss Sand Fanger.|"))
            self.write(patch, qt_encode("Statue 5 is in the Pyramid. You'll need all six Hieroglyphs as well as your father's journal.|"))
            self.write(patch, qt_encode("Statue 6 is at the top of Babel Tower. You'll need the Aura and the Crystal Ring to get to the top.|"))
            self.write(patch, qt_encode("Alternatively, if you collect enough Red Jewels to face Solid Arm, he can also take you there.|"))
            self.write(patch, qt_encode("Once you've freed Kara and gathered the Statues you need, enter any Dark Space and talk to Gaia.|"))
            self.write(patch, qt_encode("She will give you the option to face Dark Gaia and beat the game. Good luck, and have fun!") + b"\xc0")
        elif settings.goal.value == Goal.RED_JEWEL_HUNT.value:
            self.write(patch, b"\xce" + qt_encode("BEATING THE GAME:       It's a Red Jewel hunt! The objective is super simple:|"))
            self.write(patch, qt_encode("Find the Red Jewels you need, and talk to the Jeweler. That's it!|"))
            self.write(patch, qt_encode("Check the Jeweler's inventory to find out how many Red Jewels you need to beat the game.|"))
            self.write(patch, qt_encode("Happy hunting!") + b"\xc0")

        self.seek(patch, int("3f800", 16) + rom_offset)
        self.write(patch, b"\xce" + qt_encode("EXPLORING THE WORLD:    When you start the game, you only have access to a few locations.|"))
        self.write(patch, qt_encode("As you gain more items, you will be able to visit other continents and access more locations.|"))
        self.write(patch, qt_encode("Here are some of the helpful travel items you can find in the game:|"))
        self.write(patch, qt_encode("- Lola's Letter         If you find this letter, read it and go see Erik in South Cape.|"))
        self.write(patch, qt_encode("- The Teapot            If you use the Teapot in the Moon Tribe camp, you can travel by Sky Garden.|"))
        self.write(patch, qt_encode("- Memory Melody         Play this melody in Neil's Cottage, and he'll fly you in his airplane.|"))
        self.write(patch, qt_encode("- The Will              Show this document to the stable masters in either Watermia or Euro.|"))
        self.write(patch, qt_encode("- The Large Roast       Give this to the hungry child in the Natives' Village.|"))
        self.write(patch, qt_encode("If you're ever stuck in a location, find a Dark Space. Gaia can always return you to South Cape.") + b"\xc0")

        self.seek(patch, int("3fb00", 16) + rom_offset)
        self.write(patch, b"\xce" + qt_encode("WHAT IF I'M STUCK?      There are a lot of item locations in this game! It's easy to get stuck.|"))
        self.write(patch, qt_encode("Here are some resources that might help you:|"))
        self.write(patch, qt_encode("- Video Tutorial        Search YouTube for a video guide of this randomizer.|"))
        self.write(patch, qt_encode("- Ask the Community     Find the IoGR community on Discord! Someone will be happy to help you.|"))
        if mode == 0:
            self.write(patch, qt_encode("- In-Game Tracker       Enter the east-most house in South Cape to check your collection rate.|"))
        else:
            self.write(patch, qt_encode("- In-Game Tracker       (Easy mode only)|"))
        self.write(patch, qt_encode("- Check the Spoiler Log Every seed comes with a detailed list of where every item can be found.") + b"\xc0")

        # Modify Lance's Letter
        # Prepare it to spoil Kara location
        f_item16 = open(BIN_PATH + "03950c_item16.bin", "rb")
        self.seek(patch, int("3950c", 16) + rom_offset)
        self.write(patch, f_item16.read())
        f_item16.close

        # Modify Teapot
        # Now activates in Moon Tribe camp instead of Euro
        f_item19 = open(BIN_PATH + "03983d_item19.bin", "rb")
        self.seek(patch, int("3983d", 16) + rom_offset)
        self.write(patch, f_item19.read())
        f_item19.close

        # Modify Black Glasses, now permanently worn and removed from inventory when used
        self.seek(patch, int("39981", 16) + rom_offset)
        self.write(patch, b"\x8a\x99\x02\xcc\xf5\x02\xd5\x1c\x60\xd3\x42\x8e\x8e\x8b\x8d\x84")
        self.write(patch, b"\xa3\xa3\xac\x88\x8d\xa4\x84\x8d\xa3\x88\x85\x88\x84\xa3\x4f\xc0")

        # Modify Aura, now unlocks Shadow's form when used
        self.seek(patch, int("39cdc", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\xe4\x9c\x02\xcc\xb4\x60\xd3")
        self.write(patch, b"\xd6\x4c\x85\x8e\xa2\x8c\xac\xa5\x8d\x8b\x8e\x82\x8a\x84\x83\x4f\xc0")

        # Write 2 Jewel and 3 Jewel items; Lola's Letter now teaches Morse Code
        # Replaces and modifies code for item 25 - Lola's Letter @39d09
        f_item25 = open(BIN_PATH + "039d09_item25.bin", "rb")
        self.seek(patch, int("39d09", 16) + rom_offset)
        self.write(patch, f_item25.read())
        f_item25.close

        # Have fun with text in Item 26 (Father's Journal)
        self.seek(patch, int("39ea8", 16) + rom_offset)
        self.write(patch, qt_encode("It reads: ") + b"\x2d" + qt_encode("He who is ") + b"\xcb" + qt_encode("valiant and pure of spirit...") + b"\xcf\x2d")
        self.write(patch, qt_encode("... may find the Holy Grail in the Castle of... Aauugghh") + b"\x2e\xcf")
        self.write(patch, qt_encode("Here a page is missing.") + b"\xc0")

        # Modify Crystal Ring, now permanently worn and removed from inventory when used
        self.seek(patch, int("39f32", 16) + rom_offset)
        self.write(patch, b"\x3b\x9f\x02\xcc\x3e\x02\xd5\x27\x60\xd3\x41\x8b")
        self.write(patch, b"\x88\x8d\x86\xac\x81\x8b\x88\x8d\x86\x2a\xc0")

        # Write HP and DEF upgrade items; make the Apple non-consumable
        # Replaces and modifies code for item 28 - Apple @39f5d
        f_item28 = open(BIN_PATH + "039f5d_item28.bin", "rb")
        self.seek(patch, int("39f5d", 16) + rom_offset)
        self.write(patch, f_item28.read())
        f_item28.close

        # Update herb HP fill based on difficulty
        self.seek(patch, int("3889f", 16) + rom_offset)
        if mode == 0:  # Easy mode = full HP
            self.write(patch, b"\x28")
        elif mode == 2:  # Hard mode = fill 4 HP
            self.write(patch, b"\x04")
        elif mode == 3:  # Extreme mode = fill 2 HP
            self.write(patch, b"\x02")

        # Update HP jewel HP fill based on difficulty
        self.seek(patch, int("39f7a", 16) + rom_offset)
        if mode == 0:  # Easy mode = full HP
            self.write(patch, b"\x28")

        # Change item functionality for game variants
        self.seek(patch, int("3fce0", 16) + rom_offset)
        self.write(patch, qt_encode("Will drops the HP Jewel. It shatters into a million pieces. Whoops.", True))
        self.seek(patch, int("3fd40", 16) + rom_offset)
        self.write(patch, qt_encode("As the Jewel disappears, Will feels his strength draining!", True))
        # In OHKO, the HP Jewels do nothing, and start @1HP
        if settings.ohko:
            self.seek(patch, int("8068", 16) + rom_offset)
            self.write(patch, b"\x01")
            self.seek(patch, int("39f71", 16) + rom_offset)
            self.write(patch, b"\xe0\xfc\x02\xd5\x29\x60")
        # In Red Jewel Madness, start @40 HP, Red Jewels remove -1 HP when used
        #    elif variant == "Red Jewel Madness":
        #        self.seek(patch, int("8068",16)+rom_offset)
        #        self.write(patch, b"\x28")
        #        self.seek(patch, int("384d5",16)+rom_offset)
        #        self.write(patch, b"\x4c\x30\xfd")
        #        self.seek(patch, int("3fd30",16)+rom_offset)
        #        self.write(patch, b"\x02\xbf\x40\xfd\xce\xca\x0a\xce\xce\x0a\x4c\xd9\x84")

        ##########################################################################
        #                  Update overworld map movement scripts
        #   Removes overworld animation and allows free travel within continents
        ##########################################################################
        # Update map choice scripts
        f_mapchoices = open(BIN_PATH + "03b401_mapchoices.bin", "rb")
        self.seek(patch, int("3b401", 16) + rom_offset)
        self.write(patch, f_mapchoices.read())
        f_mapchoices.close

        # Update map destination array
        f_mapdest = open(BIN_PATH + "03b955_mapdest.bin", "rb")
        self.seek(patch, int("3b955", 16) + rom_offset)
        self.write(patch, f_mapdest.read())
        f_mapdest.close

        ##########################################################################
        #                   Rewrite Red Jewel acquisition event
        #      Makes unique code for each instance (overwrites unused code)
        ##########################################################################
        # Fill block with new item acquisition code (16 items)
        f_redjewel = open(BIN_PATH + "00f500_redjewel.bin", "rb")
        self.seek(patch, int("f500", 16) + rom_offset)
        self.write(patch, f_redjewel.read())
        f_redjewel.close

        # Update event table instances to point to new events
        # New pointers include leading zero byte to negate event parameters
        self.seek(patch, int("c8318", 16) + rom_offset)  # South Cape: bell tower
        self.write(patch, b"\x00\x00\xf5\x80")
        self.seek(patch, int("c837c", 16) + rom_offset)  # South Cape: Lance's house
        self.write(patch, b"\x00\x80\xf5\x80")
        self.seek(patch, int("c8ac0", 16) + rom_offset)  # Underground Tunnel: barrel
        self.write(patch, b"\x00\x00\xf6\x80")
        self.seek(patch, int("c8b50", 16) + rom_offset)  # Itory Village: logs
        self.write(patch, b"\x00\x80\xf6\x80")
        self.seek(patch, int("c9546", 16) + rom_offset)  # Diamond Coast: jar
        self.write(patch, b"\x00\x00\xf7\x80")
        self.seek(patch, int("c97a6", 16) + rom_offset)  # Freejia: hotel
        self.write(patch, b"\x00\x80\xf7\x80")
        self.seek(patch, int("caf60", 16) + rom_offset)  # Angel Village: dance hall
        self.write(patch, b"\x00\x00\xf8\x80")
        self.seek(patch, int("cb3a6", 16) + rom_offset)  # Angel Village: Ishtar's room
        self.write(patch, b"\x00\x80\xf8\x80")
        self.seek(patch, int("cb563", 16) + rom_offset)  # Watermia: west Watermia
        self.write(patch, b"\x00\x00\xf9\x80")
        self.seek(patch, int("cb620", 16) + rom_offset)  # Watermia: gambling house
        self.write(patch, b"\x00\x80\xf9\x80")
        self.seek(patch, int("cbf55", 16) + rom_offset)  # Euro: behind house
        self.write(patch, b"\x00\x00\xfa\x80")
        self.seek(patch, int("cc17c", 16) + rom_offset)  # Euro: slave room
        self.write(patch, b"\x00\x80\xfa\x80")
        self.seek(patch, int("ccb14", 16) + rom_offset)  # Natives' Village: statue room
        self.write(patch, b"\x00\x00\xfb\x80")
        self.seek(patch, int("cd440", 16) + rom_offset)  # Dao: east Dao
        self.write(patch, b"\x00\x80\xfb\x80")
        self.seek(patch, int("cd57e", 16) + rom_offset)  # Pyramid: east entrance
        self.write(patch, b"\x00\x00\xfc\x80")
        self.seek(patch, int("ce094", 16) + rom_offset)  # Babel: pillow
        self.write(patch, b"\x00\x80\xfc\x80")

        ##########################################################################
        #                         Modify Game Start events
        ##########################################################################
        # Set beginning switches
        self.seek(patch, int("be51c", 16) + rom_offset)
        self.write(patch, b"\x80\x00\x12\x4c\x00\xfd")
        f_switches = open(BIN_PATH + "0bfd00_switches.bin", "rb")
        self.seek(patch, int("bfd00", 16) + rom_offset)
        self.write(patch, f_switches.read())
        f_switches.close

        ##########################################################################
        #                         Modify South Cape events
        ##########################################################################
        # Teacher sets switch #$38 and spoils Mystic Statues required
        f_teacher = open(BIN_PATH + "048a94_teacher.bin", "rb")
        self.seek(patch, int("48a94", 16) + rom_offset)
        self.write(patch, f_teacher.read())
        f_teacher.close

        # Force fisherman to always appear on E side of docks, and fix inventory full
        self.seek(patch, int("48377", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\x10\x01\xaa\x83")
        self.seek(patch, int("48468", 16) + rom_offset)
        self.write(patch, b"\x02\xBF\x79\x84\x02\xD4\x01\x75\x84\x02\xCC\xD7\x6B" + INV_FULL)

        # Disable Lola Melody cutscene
        self.seek(patch, int("49985", 16) + rom_offset)
        self.write(patch, b"\x6b")

        # Set flag 35 at Lola Melody acquisition
        self.seek(patch, int("499dc", 16) + rom_offset)
        self.write(patch, b"\xeb\x99\x02\xbf\xe5\x9b\x02\xd4\x09\xf0\x99")
        self.write(patch, b"\x02\xcc\x35\x6b\x02\xbf\x94\x9d\x6b")
        self.write(patch, INV_FULL)

        # Erik in Seaside Cave allows player to use Lola's Letter to travel by sea
        f_seaside = open(BIN_PATH + "04b9a5_seaside.bin", "rb")
        self.seek(patch, int("4b9a5", 16) + rom_offset)
        self.write(patch, f_seaside.read())
        f_seaside.close
        self.seek(patch, int("4b8b6", 16) + rom_offset)
        self.write(patch, b"\x10\x01\x62")
        self.seek(patch, int("4b96a", 16) + rom_offset)
        self.write(patch, b"\xa5")

        # Various NPCs can give you a tutorial
        f_tutorial = open(BIN_PATH + "04fb50_tutorial.bin", "rb")
        self.seek(patch, int("4fb50", 16) + rom_offset)
        self.write(patch, f_tutorial.read())
        f_tutorial.close
        self.seek(patch, int("49231", 16) + rom_offset)  # NPC in front of school
        self.write(patch, b"\x50\xfb")
        # self.seek(patch, int("49238",16)+rom_offset)   # Grants max stats
        # self.write(patch, b"\xA9\x28\x00\x8D\xCA\x0A\x8D\xCE\x0A\x8D\xDC\x0A\x8D\xDE\x0A\x02\xBF\x4C\x92\x6B")
        # self.write(patch, qt_encode("Max stats baby!",True))

        # Turns house in South Cape into item-tracking overworld map (Easy only)
        if mode == 0:
            self.seek(patch, int("18480", 16) + rom_offset)
            self.write(patch, b"\x07\x90\x00\xd0\x03\x00\x00\x44")
            self.seek(patch, int("1854e", 16) + rom_offset)
            self.write(patch, b"\x00\x3e\x40\x02")
            self.seek(patch, int("c846c", 16) + rom_offset)
            self.write(patch, b"\x00\x01\x00\x00\xde\x86\x00\xFF\xCA")

            f_collectioncheck = open(BIN_PATH + "06dd30_collectioncheck.bin", "rb")
            self.seek(patch, int("6dd30", 16) + rom_offset)
            self.write(patch, f_collectioncheck.read())
            f_collectioncheck.close
        else:
            self.seek(patch, int("491ed", 16) + rom_offset)
            self.write(patch, qt_encode("This room is a lot cooler in Easy mode.", True))

        ##########################################################################
        #                       Modify Edward's Castle events
        ##########################################################################
        # Shorten Edward conversation
        self.seek(patch, int("4c3d6", 16) + rom_offset)
        self.write(patch, b"\x06\xc4")
        f_edward = open(BIN_PATH + "04c4fb_edward.bin", "rb")
        self.seek(patch, int("4c4fb", 16) + rom_offset)
        self.write(patch, f_edward.read())
        f_edward.close

        self.seek(patch, int("4c4fb", 16) + rom_offset)
        self.write(patch, b"\xd3")

        # Talking to Edward doesn't soft lock you
        self.seek(patch, int("4c746", 16) + rom_offset)
        self.write(patch, b"\x10")

        # Move guard to allow roast location get
        f_castleguard = open(BIN_PATH + "04d1a0_castleguard.bin", "rb")
        self.seek(patch, int("4d1a0", 16) + rom_offset)
        self.write(patch, f_castleguard.read())
        f_castleguard.close
        self.seek(patch, int("c8551", 16) + rom_offset)
        self.write(patch, b"\x10")

        #  Update Large Roast event
        self.seek(patch, int("4d0da", 16) + rom_offset)
        self.write(patch, b"\x02\xc0\xe1\xd0\x02\xc1\x6b\x02\xd0\x46\x00\xe9\xd0\x02\xe0")
        self.write(patch, b"\x02\xbf\x41\xd1\x02\xd4\x0a\xf6\xd0\x02\xcc\x46\x6b")
        self.write(patch, INV_FULL)

        # Fix hidden guard text box
        self.seek(patch, int("4c297", 16) + rom_offset)
        self.write(patch, b"\xc0")
        self.seek(patch, int("4c20e", 16) + rom_offset)
        self.write(patch, b"\x02\xBF\x99\xC2\x02\xD4\x00\x1B\xC2\x02\xCC\xD8\x6B" + INV_FULL)

        ##########################################################################
        #                   Modify Edward's Prison/Tunnel events
        ##########################################################################
        # Skip long cutscene in prison
        self.seek(patch, int("4d209", 16) + rom_offset)
        self.write(patch, b"\x34\xd2")
        self.seek(patch, int("4d234", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\x23\x00\xcf\xd2\x02\xe0")
        self.seek(patch, int("4d335", 16) + rom_offset)
        self.write(patch, b"\x6b")

        # Move Dark Space, allows player to exit area without key
        # Set new X/Y coordinates in exit table
        self.seek(patch, int("18614", 16) + rom_offset)
        self.write(patch, b"\x12\x07")
        # Set new X/Y coordinates in event table
        self.seek(patch, int("C8635", 16) + rom_offset)
        self.write(patch, b"\x12\x08")

        # Progression triggers when Lilly is with you
        self.seek(patch, int("9aa45", 16) + rom_offset)
        self.write(patch, b"\x6f\x00")
        self.seek(patch, int("9aa4b", 16) + rom_offset)
        self.write(patch, b"\x02")
        self.seek(patch, int("9be74", 16) + rom_offset)
        self.write(patch, b"\xd7\x18")

        # Give appearing Dark Space the option of handling an ability
        self.seek(patch, int("9bf7f", 16) + rom_offset)
        self.write(patch, b"\xAC\xD6\x88\xA8\x00\xC0\x04\x00\x0B\x4c\x10\xf7")
        self.seek(patch, int("9f710", 16) + rom_offset)
        self.write(patch, b"\xA5\x0E\x85\x24\xA9\x00\x20\x85\x0E\x02\xE0")
        self.seek(patch, int("c8aa2", 16) + rom_offset)
        self.write(patch, b"\x03")

        # Fix forced form change
        self.seek(patch, int("9c037", 16) + rom_offset)
        self.write(patch, FORCE_CHANGE + b"\x02\xe0")

        ##########################################################################
        #                            Modify Itory events
        ##########################################################################
        # Lilly event becomes Lola's Melody handler
        f_itory = open(BIN_PATH + "04e2a3_itory.bin", "rb")
        self.seek(patch, int("4e2a3", 16) + rom_offset)
        self.write(patch, f_itory.read())
        f_itory.close

        # Lilly now joins if you give her the Necklace
        f_lilly = open(BIN_PATH + "04e5ff_lilly.bin", "rb")
        self.seek(patch, int("4e5ff", 16) + rom_offset)
        self.write(patch, f_lilly.read())
        f_lilly.close
        self.seek(patch, int("4e5a6", 16) + rom_offset)
        self.write(patch, b"\x6f")
        self.seek(patch, int("4e5ac", 16) + rom_offset)
        self.write(patch, b"\xff\xe5\x02\x0b\x6b")

        # Shorten Inca Statue get
        self.seek(patch, int("4f37b", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\x8d\xf3\x6b")

        # For elder to always give spoiler
        self.seek(patch, int("4e933", 16) + rom_offset)
        self.write(patch, b"\x10\x01")
        self.seek(patch, int("4e97a", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\xff\xe9\x6b")

        ##########################################################################
        #                          Modify Moon Tribe events
        ##########################################################################
        # Allows player to use Teapot to travel by Sky Garden
        f_moontribe = open(BIN_PATH + "09d11e_moontribe.bin", "rb")
        self.seek(patch, int("9d11e", 16) + rom_offset)
        self.write(patch, f_moontribe.read())
        f_moontribe.close

        # Lilly event serves as an overworld exit
        self.seek(patch, int("4f441", 16) + rom_offset)
        self.write(patch, b"\x00\x00\x30\x02\x45\x14\x1c\x17\x1d\x4d\xf4\x6b")
        self.write(patch, b"\x02\x40\x00\x04\x54\xf4\x6b\x02\x66\x90\x00\x60\x02\x01\x02\xC1\x6b")

        # Adjust timer by mode
        timer = 20
        if mode == "Easy":
            timer += 5
        if settings.enemizer.value != Enemizer.NONE.value:
            timer += 5
            if settings.enemizer.value != Enemizer.LIMITED.value:
                timer += 5
        self.seek(patch, int("4f8b8", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(str(timer)))

        # Shorten Inca Statue get
        self.seek(patch, int("4fae7", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\xf9\xfa\x6b")

        ##########################################################################
        #                          Modify Inca events
        ##########################################################################
        # Fix forced form change
        self.seek(patch, int("9cfaa", 16) + rom_offset)
        self.write(patch, FORCE_CHANGE + b"\xA9\xF0\xEF\x1C\x5A\x06\x02\xe0")

        # Put Gold Ship captain at Inca entrance
        self.seek(patch, int("c8c9c", 16) + rom_offset)
        self.write(patch, b"\x19\x1c\x00\x4e\x85\x85\x00")

        ##########################################################################
        #                          Modify Gold Ship events
        ##########################################################################
        # Move Seth from deserted ship to gold ship, allows player to acquire item
        # Write pointer to Seth event in new map
        self.seek(patch, int("c945c", 16) + rom_offset)
        self.write(patch, b"\x0b\x24\x00\x3e\x96\x85\x00\xff\xca")
        self.seek(patch, int("c805a", 16) + rom_offset)
        self.write(patch, b"\x65")
        # Modify Seth event to ignore switch conditions
        self.seek(patch, int("59643", 16) + rom_offset)
        self.write(patch, b"\x10\x00")
        # Add in inventory full text
        self.seek(patch, int("59665", 16) + rom_offset)
        self.write(patch, INV_FULL)

        # Entering Gold Ship doesn't lock out Castoth
        self.seek(patch, int("58188", 16) + rom_offset)
        self.write(patch, b"\x02\xc1\x02\xc1")
        self.seek(patch, int("18a09", 16) + rom_offset)
        self.write(patch, b"\xd0\x00\x40\x02\x03")

        # Have ladder NPC move aside only if Mystic Statue has been acquired
        self.seek(patch, int("583cb", 16) + rom_offset)
        self.write(patch, b"\x10")

        # Modify queen switches
        self.seek(patch, int("58a04", 16) + rom_offset)
        self.write(patch, b"\x10\x00")
        self.seek(patch, int("58a1f", 16) + rom_offset)
        self.write(patch, b"\x10")

        # Have crow's nest NPC warp directly to Diamond Coast
        # Also checks for Castoth being defeated
        f_goldship = open(BIN_PATH + "0584a9_goldship.bin", "rb")
        self.seek(patch, int("584a9", 16) + rom_offset)
        self.write(patch, f_goldship.read())
        f_goldship.close

        # Sleeping sends player to Diamond Coast
        self.seek(patch, int("586a3", 16) + rom_offset)
        self.write(patch, b"\x02\x26\x30\x48\x00\x20\x00\x03\x00\x21")

        ##########################################################################
        #                        Modify Diamond Coast events
        ##########################################################################
        # Allow Turbo to contact Seth
        self.seek(patch, int("c953e", 16) + rom_offset)
        self.write(patch, b"\x01")
        self.seek(patch, int("5aa76", 16) + rom_offset)
        self.write(patch, b"\x00\xff")
        self.seek(patch, int("5ff00", 16) + rom_offset)
        self.write(patch, b"\x02\xCC\x01\x02\xD0\x11\x01\x0E\xFF\x02\xBF\x60\xFF\x6B\x02\xD0\x12\x01\x1B\xFF")
        self.write(patch, b"\x02\xcc\x12\x02\xBF\x1F\xFF\x5C\xBD\xB9\x84")
        self.write(patch, b"\xd3" + qt_encode("Woof woof!") + b"\xcb")
        self.write(patch, qt_encode("(Oh good, you know Morse Code. Let's see what Seth's up to:)") + b"\xc0")
        self.write(patch, b"\xd3" + qt_encode("Woof woof!") + b"\xcb")
        self.write(patch, qt_encode("(You don't happen to know Morse Code, do you?)") + b"\xc0")

        # Kara event serves as an overworld exit
        self.seek(patch, int("5aa9e", 16) + rom_offset)
        self.write(patch, b"\x00\x00\x30\x02\x45\x03\x00\x06\x01\xaa\xaa\x6b")
        self.write(patch, b"\x02\x40\x00\x08\xb1\xaa\x6b\x02\x66\x50\x02\x50\x03\x07\x02\xC1\x6b")

        ##########################################################################
        #                           Modify Freejia events
        ##########################################################################
        # Trash can 1 gives you an item instead of a status upgrade
        # NOTE: This cannibalizes the following event @5cfbc (locked door)
        f_freejia = open(BIN_PATH + "05cf85_freejia.bin", "rb")
        self.seek(patch, int("5cf85", 16) + rom_offset)
        self.write(patch, f_freejia.read())
        f_freejia.close

        # Give full inventory text to trash can 2
        self.seek(patch, int("5cf37", 16) + rom_offset)
        self.write(patch, b"\x02\xBF\x49\xCF\x02\xD4\x12\x44\xCF\x02\xCC\x53\x6B" + INV_FULL)

        # Redirect event table to bypass deleted event
        # Changes locked door to a normal door
        self.seek(patch, int("c95bb", 16) + rom_offset)
        self.write(patch, b"\xf3\xc5\x80")

        # Update NPC dialogue to acknowledge change
        self.seek(patch, int("5c331", 16) + rom_offset)
        self.write(patch, b"\x42\xa2\x80\xa0\x2b\xac\x48\xac\xd6\xae\xa4\x87\x84\xac\xd7\x58\xcb\xa5")
        self.write(patch, b"\x8d\x8b\x8e\x82\x8a\x84\x83\xac\x80\x86\x80\x88\x8d\x2a\x2a\x2a\xc0")

        # Add inventory full option to Creepy Guy event
        self.seek(patch, int("5b6df", 16) + rom_offset)
        self.write(patch, INV_FULL)

        # Alter laborer text
        self.seek(patch, int("5bfdb", 16) + rom_offset)
        self.write(patch, b"\xde\xbf")

        # Have some fun with snitch item text
        self.seek(patch, int("5b8bc", 16) + rom_offset)
        self.write(patch, b"\x62")
        self.seek(patch, int("5b925", 16) + rom_offset)
        self.write(patch, b"\x88\xa4\x84\x8c\x2a\xcb\xac\x69\x84\xa3\x2b\xac\x48\x0e\x8c\xac\x80\xac\x81")
        self.write(patch, b"\x80\x83\xac\xa0\x84\xa2\xa3\x8e\x8d\xcb\xac\x63\x8d\x88\xa4\x82\x87\x84\xa3")
        self.write(patch, b"\xac\x86\x84\xa4\xac\xa3\xa4\x88\xa4\x82\x87\x84\xa3\x2b\xac\xa9\x8e\xca")

        ##########################################################################
        #                        Modify Diamond Mine events
        ##########################################################################
        # Trapped laborer gives you an item instead of sending Jewels to Jeweler
        self.seek(patch, int("5d739", 16) + rom_offset)
        self.write(patch, b"\x4c\x5d\xd8\x85")
        f_trappedlaborer = open(BIN_PATH + "05d7e2_trappedlaborer.bin", "rb")
        self.seek(patch, int("5d7e2", 16) + rom_offset)
        self.write(patch, f_trappedlaborer.read())
        f_trappedlaborer.close

        # Shorten laborer items
        self.seek(patch, int("aa753", 16) + rom_offset)
        self.write(patch, b"\xef\xa7")
        self.seek(patch, int("aa75a", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("aa773", 16) + rom_offset)
        self.write(patch, b"\x5c\xa8")
        self.seek(patch, int("aa77a", 16) + rom_offset)
        self.write(patch, b"\x6b")

        # Shorten morgue item get
        self.seek(patch, int("5d4d8", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\xeb\xd4\x02\xe0")

        # Cut out Sam's song
        self.seek(patch, int("5d24f", 16) + rom_offset)
        self.write(patch, b"\x6b")

        # Give appearing Dark Space the option of handling an ability
        self.seek(patch, int("5d62f", 16) + rom_offset)
        self.write(patch, b"\xAC\xD6\x88\x00\x2B\xA5\x0E\x85\x24\xA9\x00\x20\x85\x0E\x02\xE0")

        ##########################################################################
        #                       Modify Neil's Cottage events
        ##########################################################################
        # Allow travel by plane with the Memory Melody
        f_neilscottage = open(BIN_PATH + "05d89a_neilscottage.bin", "rb")
        self.seek(patch, int("5d89a", 16) + rom_offset)
        self.write(patch, f_neilscottage.read())
        f_neilscottage.close

        # Invention event serves as an overworld exit
        self.seek(patch, int("5e305", 16) + rom_offset)
        self.write(patch, b"\x00\x00\x30\x02\x45\x07\x0d\x0a\x0e\x11\xe3\x6b")
        self.write(patch, b"\x02\x40\x00\x04\x18\xe3\x6b\x02\x66\x70\x02\x70\x02\x07\x02\xC1\x6b")

        ##########################################################################
        #                            Modify Nazca events
        ##########################################################################
        # Speedup warp sequence to Sky Garden
        f_nazca = open(BIN_PATH + "05e647_nazca.bin", "rb")
        self.seek(patch, int("5e647", 16) + rom_offset)
        self.write(patch, f_nazca.read())
        f_nazca.close

        # Allow exit to world map
        self.seek(patch, int("5e80c", 16) + rom_offset)
        self.write(patch, b"\x02\x66\x10\x03\x90\x02\x07\x02\xC1\x6B")

        ##########################################################################
        #                          Modify Sky Garden events
        ##########################################################################
        # Allow travel from Sky Garden to other locations
        f_skygarden = open(BIN_PATH + "05f356_skygarden.bin", "rb")
        self.seek(patch, int("5f356", 16) + rom_offset)
        self.write(patch, f_skygarden.read())
        f_skygarden.close

        # Instant form change & warp to Seaside Palace if Viper is defeated
        self.seek(patch, int("ace9b", 16) + rom_offset)
        self.write(patch, b"\x4c\x90\xfd")
        self.seek(patch, int("acecb", 16) + rom_offset)
        self.write(patch, b"\x01\x02\x26\x5a\x90\x00\x70\x00\x83\x00\x14\x02\xc1\x6b")

        f_viperchange = open(BIN_PATH + "0afd90_viperchange.bin", "rb")
        self.seek(patch, int("afd90", 16) + rom_offset)
        self.write(patch, f_viperchange.read())
        f_viperchange.close

        ##########################################################################
        #                       Modify Seaside Palace events
        ##########################################################################
        # Add exit from Mu passage to Angel Village @191de
        self.seek(patch, int("191de", 16) + rom_offset)
        self.write(patch, b"\x04\x06\x02\x03\x69\xa0\x02\x38\x00\x00\x00\x13")  # Temporarily put exit one tile south
        # self.write(patch, b"\x04\x05\x02\x03\x69\xa0\x02\x38\x00\x00\x00\x13")  # Change to this if map is ever updated

        # Replace Mu Passage map with one that includes a door to Angel Village
        f_mupassage = open(BIN_PATH + "1e28a5_mupassage.bin", "rb")
        self.seek(patch, int("1e28a5", 16) + rom_offset)
        self.write(patch, f_mupassage.read())
        f_mupassage.close

        # Shorten NPC item get
        self.seek(patch, int("68b01", 16) + rom_offset)
        self.write(patch, b"\x6b")

        # Purification event won't softlock if you don't have Lilly
        self.seek(patch, int("69406", 16) + rom_offset)
        self.write(patch, b"\x10")
        self.seek(patch, int("6941a", 16) + rom_offset)
        self.write(patch, b"\x01\x02\xc1\x02\xc1")

        # Remove Lilly text when Mu door opens
        self.seek(patch, int("39174", 16) + rom_offset)
        self.write(patch, b"\x60")
        self.seek(patch, int("391d7", 16) + rom_offset)
        self.write(patch, b"\xc0")

        # Allow player to open Mu door from the back
        f_mudoor = open(BIN_PATH + "069739_mudoor.bin", "rb")
        self.seek(patch, int("69739", 16) + rom_offset)
        self.write(patch, f_mudoor.read())
        f_mudoor.close

        # Remove fanfare from coffin item get
        self.seek(patch, int("69232", 16) + rom_offset)
        self.write(patch, b"\x9e\x93\x4c\x61\x92")
        self.seek(patch, int("69267", 16) + rom_offset)
        self.write(patch, b"\x80\x04")

        # Make coffin spoiler re-readable
        self.seek(patch, int("68ff3", 16) + rom_offset)
        self.write(patch, b"\xf5\x8f")
        self.seek(patch, int("68ffb", 16) + rom_offset)
        self.write(patch, b"\x70\xe5")
        self.seek(patch, int("69092", 16) + rom_offset)
        self.write(patch, b"\x02\xce\x01\x02\x25\x2F\x0A\x4c\xfd\x8f")
        self.seek(patch, int("6e570", 16) + rom_offset)
        self.write(patch, b"\x02\xD1\x3A\x01\x01\x8A\xE5\x02\xD0\x6F\x01\x82\xE5\x02\xBF\xA7\x90\x6B")
        self.write(patch, b"\x02\xBF\xCF\x90\x02\xCC\x01\x6B\x02\xBF\x67\x91\x6B")

        ##########################################################################
        #                             Modify Mu events
        ##########################################################################
        # Add "inventory full" option to Statue of Hope items
        self.seek(patch, int("698cd", 16) + rom_offset)
        self.write(patch, INV_FULL)

        # Shorten Statue of Hope get
        self.seek(patch, int("698b8", 16) + rom_offset)
        self.write(patch, b"\x02\xBF\xD2\x98\x02\xD4\x28\xCD\x98\x02\xCC\x79\x6B")
        self.seek(patch, int("69960", 16) + rom_offset)
        self.write(patch, b"\x02\xBF\x75\x99\x02\xD4\x1E\xCD\x98\x02\xCC\x7F\x6B")

        # Shorten Rama statue event
        self.seek(patch, int("69e50", 16) + rom_offset)
        self.write(patch, b"\x10")
        self.seek(patch, int("69f26", 16) + rom_offset)
        self.write(patch, b"\x00")

        # Text in Hope Room
        self.seek(patch, int("69baa", 16) + rom_offset)
        self.write(patch, qt_encode("Hey.", True))

        # Spirits in Rama statue room can't lock you
        self.seek(patch, int("6a07a", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("6a082", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("6a08a", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("6a092", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("6a09a", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("6a0a2", 16) + rom_offset)
        self.write(patch, b"\x6b")

        # Move exits around to make Vampires required for Statue
        self.seek(patch, int("193ea", 16) + rom_offset)
        self.write(patch, b"\x5f\x80\x00\x50\x00\x03\x00\x44")
        self.seek(patch, int("193f8", 16) + rom_offset)
        self.write(patch, b"\x65\xb8\x00\x80\x02\x03\x00\x44")
        self.seek(patch, int("69c62", 16) + rom_offset)
        self.write(patch, b"\x67\x78\x01\xd0\x01\x80\x01\x22")
        self.seek(patch, int("6a4c9", 16) + rom_offset)
        self.write(patch, b"\x02\x26\x66\xf8\x00\xd8\x01\x00\x00\x22\x02\xc1\x6b")

        # Instant form change after Vamps are defeated
        self.seek(patch, int("6a43b", 16) + rom_offset)
        self.write(patch, b"\x4c\x00\xe5")

        f_vampchange = open(BIN_PATH + "06e500_vampchange.bin", "rb")
        self.seek(patch, int("6e500", 16) + rom_offset)
        self.write(patch, f_vampchange.read())
        f_vampchange.close

        ##########################################################################
        #                       Modify Angel Village events
        ##########################################################################
        # Add exit from Angel Village to Mu passage @1941a
        self.seek(patch, int("1941a", 16) + rom_offset)
        self.write(patch, b"\x2a\x05\x01\x01\x5e\x48\x00\x90\x00\x01\x00\x14")  # Temporarily put exit one tile south
        # self.write(patch, b"\x2a\x05\x01\x01\x5e\x48\x00\x80\x00\x01\x00\x14")  # Change to this if map is ever updated

        # Update sign to read "Passage to Mu"
        f_angelsign = open(BIN_PATH + "06ba36_angelsign.bin", "rb")
        self.seek(patch, int("6ba36", 16) + rom_offset)
        self.write(patch, f_angelsign.read())
        f_angelsign.close

        # Entering this area clears your enemy defeat count and forces change to Will
        self.seek(patch, int("6bff7", 16) + rom_offset)
        self.write(patch, b"\x00\x00\x30\x02\x40\x01\x0F\x01\xC0\x6b")
        self.write(patch, b"\xA0\x00\x00\xA9\x00\x00\x99\x80\x0A\xC8\xC8\xC0\x20\x00\xD0\xF6")
        self.write(patch, FORCE_CHANGE + b"\x02\xE0")

        # Insert new arrangement for map 109, takes out rock to prevent spin dash softlock
        f_angelmap = open(BIN_PATH + "1a5a37_angelmap.bin", "rb")
        self.seek(patch, int("1a5a37", 16) + rom_offset)
        self.write(patch, f_angelmap.read())
        f_angelmap.close

        # Ishtar's game never closes
        self.seek(patch, int("6d9fc", 16) + rom_offset)
        self.write(patch, b"\x10")
        self.seek(patch, int("6cede", 16) + rom_offset)
        self.write(patch, b"\x9c\xa6\x0a\x6b")
        self.seek(patch, int("6cef6", 16) + rom_offset)
        self.write(patch, b"\x40\x86\x80\x88\x8d\x4f\xc0")

        ##########################################################################
        #                           Modfy Watermia events
        ##########################################################################
        # Allow NPC to contact Seth
        self.seek(patch, int("78542", 16) + rom_offset)
        self.write(patch, b"\x50\xe9")
        self.seek(patch, int("7e950", 16) + rom_offset)
        self.write(patch, b"\x02\xD0\x11\x01\x5B\xE9\x02\xBF\xb8\xe9\x6B\x02\xD0\x12\x01\x68\xE9")
        self.write(patch, b"\x02\xcc\x12\x02\xBF\x6c\xE9\x5C\xBD\xB9\x84")
        self.write(patch, b"\xd3" + qt_encode("Oh, you know Bagu? Then I can help you cross.") + b"\xcb")
        self.write(patch, qt_encode("(And by Bagu I mean Morse Code.)") + b"\xc0")
        self.write(patch, b"\xd3" + qt_encode("Only town folk may cross this river!") + b"\xcb")
        self.write(patch, qt_encode("(Or, if you can talk to fish, I guess.)") + b"\xc0")

        # Allow for travel from  Watermia to Euro
        # Update address pointer
        self.seek(patch, int("78544", 16) + rom_offset)
        self.write(patch, b"\x69")

        # Update event address pointers
        f_watermia1 = open(BIN_PATH + "078569_watermia1.bin", "rb")
        self.seek(patch, int("78569", 16) + rom_offset)
        self.write(patch, f_watermia1.read())
        f_watermia1.close

        # Change textbox contents
        f_watermia2 = open(BIN_PATH + "0786c1_watermia2.bin", "rb")
        self.seek(patch, int("786c1", 16) + rom_offset)
        self.write(patch, f_watermia2.read())
        f_watermia2.close

        # Russian Glass NPC just gives you the item
        f_russianglass = open(BIN_PATH + "079237_russianglass.bin", "rb")
        self.seek(patch, int("79237", 16) + rom_offset)
        self.write(patch, f_russianglass.read())
        f_russianglass.close

        # Fix Lance item get text
        self.seek(patch, int("7ad28", 16) + rom_offset)
        self.write(patch, INV_FULL)

        ##########################################################################
        #                          Modify Great Wall events
        ##########################################################################
        # Rewrite Necklace Stone acquisition event
        # Fill block with new item acquisition code (2 items)
        f_necklace = open(BIN_PATH + "07b59e_necklace.bin", "rb")
        self.seek(patch, int("7b59e", 16) + rom_offset)
        self.write(patch, f_necklace.read())
        f_necklace.close

        # Update event table instance to point to new events
        # New pointers include leading zero byte to negate event parameters
        self.seek(patch, int("cb822", 16) + rom_offset)  # First stone, map 130
        self.write(patch, b"\x00\x9e\xb5\x87")
        self.seek(patch, int("cb94a", 16) + rom_offset)  # Second stone, map 131
        self.write(patch, b"\x00\xfe\xb5\x87")

        # Entering wrong door in 2nd map area doesn't softlock you
        self.seek(patch, int("19a4c", 16) + rom_offset)
        self.write(patch, b"\x84")

        # Give appearing Dark Space the option of handling an ability
        self.seek(patch, int("7be0b", 16) + rom_offset)
        self.write(patch, b"\xAC\xD6\x88\xC8\x01\x80\x02\x00\x2B\xA5\x0E\x85\x24\xA9\x00\x20\x85\x0E\x02\xE0")
        self.seek(patch, int("cbc60", 16) + rom_offset)
        self.write(patch, b"\x03")

        # Exit after Sand Fanger takes you back to start
        self.seek(patch, int("19c84", 16) + rom_offset)
        self.write(patch, b"\x82\x10\x00\x90\x00\x07\x00\x18")

        ##########################################################################
        #                            Modify Euro events
        ##########################################################################
        # Allow travel from Euro to Watermia
        # Update event address pointers
        f_euro1 = open(BIN_PATH + "07c432_euro1.bin", "rb")
        self.seek(patch, int("7c432", 16) + rom_offset)
        self.write(patch, f_euro1.read())
        f_euro1.close
        # Change textbox contents
        f_euro2 = open(BIN_PATH + "07c4d0_euro2.bin", "rb")
        self.seek(patch, int("7c4d0", 16) + rom_offset)
        self.write(patch, f_euro2.read())
        f_euro2.close
        self.seek(patch, int("7c482", 16) + rom_offset)
        self.write(patch, qt_encode("A moose once bit my sister.", True))

        # Neil in Euro
        f_euroneil = open(BIN_PATH + "07e398_euroneil.bin", "rb")
        self.seek(patch, int("7e398", 16) + rom_offset)
        self.write(patch, f_euroneil.read())
        f_euroneil.close
        self.seek(patch, int("7e37f", 16) + rom_offset)
        self.write(patch, b"\x14\x00")
        self.seek(patch, int("7e394", 16) + rom_offset)
        self.write(patch, b"\x10\x00")

        # Hidden house replaces STR upgrade with item acquisition
        f_euroitem = open(BIN_PATH + "07e517_euroitem.bin", "rb")
        self.seek(patch, int("7e517", 16) + rom_offset)
        self.write(patch, f_euroitem.read())
        f_euroitem.close

        # Speed up store line
        self.seek(patch, int("7d5e1", 16) + rom_offset)
        self.write(patch, b"\x00\x01")

        # Change vendor event, allows for only one item acquisition
        # Note: this cannibalizes the following event
        self.seek(patch, int("7c0a7", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\x9a\x01\xba\xc0\x02\xbf\xf3\xc0\x02\xd4\x28\xbf\xc0")
        self.write(patch, b"\x02\xcc\x9a\x6b\x02\xbf\xdd\xc0\x6b")
        self.write(patch, INV_FULL)
        # Change pointer for cannibalized event
        self.seek(patch, int("7c09b", 16) + rom_offset)
        self.write(patch, b"\xc4")

        # Store replaces status upgrades with item acquisition
        self.seek(patch, int("7cd03", 16) + rom_offset)  # HP upgrade
        self.write(patch, b"\x02\xd0\xf0\x01\x32\xcd\x02\xc0\x10\xcd\x02\xc1\x6b")
        self.write(patch, b"\x02\xd4\x29\x20\xcd\x02\xcc\xf0\x02\xbf\x39\xcd\x02\xe0")
        self.seek(patch, int("7cdf7", 16) + rom_offset)  # Dark Friar upgrade
        self.write(patch, b"\x02\xd4\x2d\x05\xce\x02\xcc\xf1\x02\xbf\x28\xce\x02\xe0")
        self.write(patch, b"\x02\xbf\x3e\xce\x6b")

        # Old men text no longer checks for Teapot
        self.seek(patch, int("7d60a", 16) + rom_offset)
        self.write(patch, b"\x14\xd6")
        self.seek(patch, int("7d7a5", 16) + rom_offset)
        self.write(patch, b"\xbd\xd7")

        # Various NPC dialogue
        self.seek(patch, int("7d6db", 16) + rom_offset)
        self.write(patch, b"\x2A\xD0\xC8\xC9\x1E\xC2\x0B\xC2\x03" + qt_encode("It could be carried by an African swallow!"))
        self.write(patch, b"\xCF\xC2\x03\xC2\x04" + qt_encode("Oh yeah, an African swallow maybe, but not a European swallow, that's my point!") + b"\xc0")
        self.seek(patch, int("7d622", 16) + rom_offset)
        self.write(patch, qt_encode("Rofsky: Wait a minute, supposing two swallows carried it together?...") + b"\xc0")
        self.seek(patch, int("7c860", 16) + rom_offset)
        self.write(patch, b"\xce" + qt_encode("Nobody expects the Spanish Inquisition!") + b"\xc0")
        self.seek(patch, int("7c142", 16) + rom_offset)
        self.write(patch, qt_encode("I am no longer infected.", True))
        self.seek(patch, int("7c160", 16) + rom_offset)
        self.write(patch, qt_encode("My hovercraft is full of eels.", True))
        self.seek(patch, int("7c182", 16) + rom_offset)
        self.write(patch, qt_encode("... w-i-i-i-i-ith... a herring!!", True))
        self.seek(patch, int("7c1b6", 16) + rom_offset)
        self.write(patch, qt_encode("It's only a wafer-thin mint, sir...", True))
        self.seek(patch, int("7c1dc", 16) + rom_offset)
        self.write(patch, b"\xd3" + qt_encode("The mill's closed. There's no more work. We're destitute.|"))
        self.write(patch, qt_encode("I've got no option but to sell you all for scientific experiments.") + b"\xc0")
        self.seek(patch, int("7c3d4", 16) + rom_offset)
        self.write(patch, qt_encode("You're a looney.", True))

        ##########################################################################
        #                        Modify Native Village events
        ##########################################################################
        # Native can guide you to Dao if you give him the roast
        f_natives = open(BIN_PATH + "088fc4_natives.bin", "rb")
        self.seek(patch, int("88fc4", 16) + rom_offset)
        self.write(patch, f_natives.read())
        f_natives.close

        # Change event pointers for cannibalized NPC code
        self.seek(patch, int("cca93", 16) + rom_offset)
        self.write(patch, b"\x88\x8f\x88")

        ##########################################################################
        #                         Modify Ankor Wat events
        ##########################################################################
        # Modify Gorgon Flower event, make it a simple item get
        f_ankorwat1 = open(BIN_PATH + "089abf_ankorwat.bin", "rb")
        self.seek(patch, int("89abf", 16) + rom_offset)
        self.write(patch, f_ankorwat1.read())
        f_ankorwat1.close

        # Shorten black glasses get
        self.seek(patch, int("89fa9", 16) + rom_offset)
        self.write(patch, b"\x02\xe0")

        # Bright room looks at switch 4f rather than equipment
        f_ankorwat2 = open(BIN_PATH + "089a31_ankorwat.bin", "rb")
        self.seek(patch, int("89a31", 16) + rom_offset)
        self.write(patch, f_ankorwat2.read())
        f_ankorwat2.close

        ##########################################################################
        #                            Modify Dao events
        ##########################################################################
        # Snake game grants an item instead of sending Jewels to the Jeweler
        f_snakegame = open(BIN_PATH + "08b010_snakegame.bin", "rb")
        self.seek(patch, int("8b010", 16) + rom_offset)
        self.write(patch, f_snakegame.read())
        f_snakegame.close

        # Neil in Dao
        f_daoneil = open(BIN_PATH + "08a5bd_daoneil.bin", "rb")
        self.seek(patch, int("8a5bd", 16) + rom_offset)
        self.write(patch, f_daoneil.read())
        f_daoneil.close
        self.seek(patch, int("8a5b3", 16) + rom_offset)
        self.write(patch, b"\x14\x00")

        # Allow travel back to Natives' Village
        self.seek(patch, int("8b16d", 16) + rom_offset)
        self.write(patch, b"\x4c\x50\xfe")
        self.seek(patch, int("8fe50", 16) + rom_offset)
        self.write(patch, b"\x02\xBF\x71\xFE\x02\xBE\x02\x01\x5A\xFE\x60\xFE\x60\xFE\x65\xFE")
        self.write(patch, b"\x02\xBF\x93\xFE\x6B\x02\x26\xAC\xC0\x01\xD0\x01\x06\x00\x22\x02\xC5")
        self.write(patch, b"\xd3" + qt_encode("Go to Natives' Village?") + b"\xcb\xac")
        self.write(patch, qt_encode("No") + b"\xcb\xac" + qt_encode("Yes") + b"\xca")
        self.write(patch, b"\xce" + qt_encode("Come back anytime!") + b"\xc0")

        # Modify two-item acquisition event
        self.seek(patch, int("8b1bb", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("8b189", 16) + rom_offset)
        self.write(patch, b"\xe0\xfd")
        self.seek(patch, int("8fde0", 16) + rom_offset)
        self.write(patch, b"\xD3\x4b\x8e\x8b\x80\x0e\xa3\xac\x4b\x84\xa4\xa4\x84\xa2\xCB")
        self.write(patch, b"\x49\x8e\xa5\xa2\x8d\x80\x8b\xac\xac\xac\xac\xac\xac\xCF\xCE")
        self.write(patch, qt_encode("If you want a guide to take you to the Natives' Village, I can get one for you.") + b"\xc0")

        # Spirit appears only after you defeat Mummy Queen or Solid Arm
        self.seek(patch, int("980cb", 16) + rom_offset)
        self.write(patch, b"\x4c\xb0\xf6")
        self.seek(patch, int("9f6b0", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\xf6\x01\xd1\x80\x02\xd1\x79\x01\x01\xd1\x80\x02\xe0")

        ##########################################################################
        #                           Modify Pyramid events
        ##########################################################################
        # Can give journal to the guide in hieroglyph room
        self.seek(patch, int("8c207", 16) + rom_offset)
        self.write(patch, b"\x0E\xC2\x02\x0B\x02\xC1\x6B\x02\xD0\xEF\x01\x1E\xC2\x02\xD6\x26\x22\xC2")
        self.write(patch, b"\x02\xBF\x2D\xC2\x6B\x5C\x08\xF2\x83\x02\xCC\xEF\x02\xD5\x26\x02\xBF\x7F\xC2\x6B")
        self.write(patch, qt_encode("If you have any information about the pyramid, I'd be happy to hold onto it for you.", True))
        self.write(patch, qt_encode("I'll hold onto that journal for you. Come back anytime if you want to read it.", True))
        self.seek(patch, int("3f208", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\x1a\x9e\x6b")

        # Shorten hieroglyph get
        self.seek(patch, int("8c7b8", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("8c87f", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("8c927", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("8c9cf", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("8ca77", 16) + rom_offset)
        self.write(patch, b"\x6b")
        self.seek(patch, int("8cb1f", 16) + rom_offset)
        self.write(patch, b"\x6b")

        ##########################################################################
        #                            Modify Babel events
        ##########################################################################
        # Move Dark Space in Babel Tower from map 224 to map 223
        # Allows player to exit Babel without crystal ring
        # Modify address pointer for Maps 224 in exit table
        self.seek(patch, int("183f4", 16) + rom_offset)
        self.write(patch, b"\xea")
        # Move Dark Space exit data to Map 223
        f_babel1 = open(BIN_PATH + "01a7c2_babel.bin", "rb")
        self.seek(patch, int("1a7c2", 16) + rom_offset)
        self.write(patch, f_babel1.read())
        f_babel1.close
        # Modify address pointer for Maps 224-227 in event table
        self.seek(patch, int("c81c0", 16) + rom_offset)
        self.write(patch, b"\xa2\xe0\xe3\xe0\x0f\xe1\x2d\xe1")
        # Assign new Dark Space correct overworld name
        self.seek(patch, int("bf8c4", 16) + rom_offset)
        self.write(patch, b"\x47\xfa")
        # Move Dark Space event data to Map 223
        # Also move spirits for entrance warp
        f_babel2 = open(BIN_PATH + "0ce099_babel.bin", "rb")
        self.seek(patch, int("ce099", 16) + rom_offset)
        self.write(patch, f_babel2.read())
        f_babel2.close

        # Spirits can warp you back to start
        self.seek(patch, int("99b69", 16) + rom_offset)
        self.write(patch, b"\x76\x9B\x76\x9B\x76\x9B\x76\x9B")
        self.seek(patch, int("99b7a", 16) + rom_offset)
        self.write(patch, b"\x02\xBE\x02\x01\x80\x9B\x86\x9B\x86\x9B\x16\x9D\x02\xBF\x95\x9C\x6B")
        self.seek(patch, int("99c1e", 16) + rom_offset)
        self.write(patch, b"\xd3" + qt_encode("What'd you like to do?") + b"\xcb\xac")
        self.write(patch, qt_encode("Git gud") + b"\xcb\xac" + qt_encode("Run away!") + b"\xca")
        self.seek(patch, int("99c95", 16) + rom_offset)
        self.write(patch, b"\xce" + qt_encode("Darn straight.") + b"\xc0")
        self.seek(patch, int("99d16", 16) + rom_offset)
        self.write(patch, b"\x02\x26\xDE\x78\x00\xC0\x00\x00\x00\x11\x02\xC5")

        # Change switch conditions for Crystal Ring item
        self.seek(patch, int("9999b", 16) + rom_offset)
        self.write(patch, b"\x4c\xd0\xf6")
        self.seek(patch, int("9f6d0", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\xdc\x00\xa0\x99\x02\xd0\x3e\x00\xa0\x99\x02\xd0\xb4\x01\x9a\x99\x4c\xa0\x99")
        self.seek(patch, int("999aa", 16) + rom_offset)
        self.write(patch, b"\x4c\xf0\xf6")
        self.seek(patch, int("9f6f0", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\xdc\x01\x9a\x99\x4c\xaf\x99")
        self.seek(patch, int("99a49", 16) + rom_offset)
        self.write(patch, b"\x02\xbf\xe4\x9a\x02\xd4\x27\x57\x9a\x02\xcc\xdc\x02\xe0" + INV_FULL)
        # Change text
        self.seek(patch, int("99a70", 16) + rom_offset)
        self.write(patch, qt_encode("Well, lookie there.", True))

        # Olman event no longer warps you out of the room
        self.seek(patch, int("98891", 16) + rom_offset)
        self.write(patch, b"\x02\x0b\x6b")

        # Shorten Olman text boxes
        self.seek(patch, int("9884c", 16) + rom_offset)
        self.write(patch, b"\x01\x00")
        self.seek(patch, int("98903", 16) + rom_offset)
        self.write(patch, qt_encode("heya.", True))
        self.seek(patch, int("989a2", 16) + rom_offset)
        self.write(patch, qt_encode("you've been busy, huh?", True))

        # Speed up roof sequence
        self.seek(patch, int("98fad", 16) + rom_offset)
        self.write(patch, b"\x02\xcc\x0e\x02\xcc\x0f\x6b")

        ##########################################################################
        #                      Modify Jeweler's Mansion events
        ##########################################################################
        # Set exit warp to Dao
        self.seek(patch, int("8fcb2", 16) + rom_offset)
        self.write(patch, b"\x02\x26\xc3\x40\x01\x88\x00\x00\x00\x23")

        # Set flag when Solid Arm is killed
        self.seek(patch, int("8fa25", 16) + rom_offset)
        self.write(patch, b"\x4c\x20\xfd")
        self.seek(patch, int("8fd20", 16) + rom_offset)
        self.write(patch, b"\x02\xcc\xf6\x02\x26\xe3\x80\x02\xa0\x01\x80\x10\x23\x02\xe0")

        # Solid Arm text
        self.seek(patch, int("8fa32", 16) + rom_offset)
        self.write(patch, qt_encode("Weave a circle round him") + b"\xcb" + qt_encode("  thrice,"))
        self.write(patch, b"\xcb" + qt_encode("And close your eyes with") + b"\xcb" + qt_encode("  holy dread,"))
        self.write(patch, b"\xcf" + qt_encode("For he on honey-dew hath") + b"\xcb" + qt_encode("  fed,"))
        self.write(patch, b"\xcb" + qt_encode("And drunk the milk of ") + b"\xcb" + qt_encode("  Paradise.") + b"\xc0")

        self.seek(patch, int("8fbc9", 16) + rom_offset)
        self.write(patch, b"\xd5\x02" + qt_encode("Ed, what an ugly thing to say... does this mean we're not friends anymore?|"))
        self.write(patch, qt_encode("You know, Ed, if I thought you weren't my friend, I just don't think I could bear it.") + b"\xc0")

        ##########################################################################
        #                           Modify Ending cutscene
        ##########################################################################
        # Custom credits
        str_endpause = b"\xC9\xB4\xC8\xCA"
        self.seek(patch, int("bd566", 16) + rom_offset)
        self.write(patch, b"\xCB" + qt_encode("    Thanks a million.") + str_endpause)
        self.seek(patch, int("bd5ac", 16) + rom_offset)
        self.write(patch, b"\xCB" + qt_encode(" Extra special thanks to") + b"\xCB" + qt_encode("       manafreak"))
        self.write(patch, b"\xC9\x78\xCE\xCB" + qt_encode(" This project would not") + b"\xCB" + qt_encode("  exist without his work."))
        self.write(patch, b"\xC9\x78\xCE\xCB" + qt_encode("     gaiathecreator") + b"\xCB" + qt_encode("      .blogspot.com") + str_endpause)
        self.seek(patch, int("bd71c", 16) + rom_offset)
        self.write(patch, qt_encode("    Created by") + b"\xCB" + qt_encode("       DontBaguMe") + str_endpause)
        self.seek(patch, int("bd74f", 16) + rom_offset)
        self.write(patch, qt_encode("Additional Development By") + b"\xCB" + qt_encode("    bryon w and Raeven0"))
        self.write(patch, b"\xCB" + qt_encode("  EmoTracker by Apokalysme"))
        self.write(patch, b"\xC9\x78\xCE\xCB" + qt_encode("   Thanks to all the") + b"\xCB" + qt_encode("  amazing playtesters!") + str_endpause)
        self.seek(patch, int("bdee2", 16) + rom_offset)
        # self.write(patch, b"\xCB" + qt_encode("  Thanks RPGLimitBreak!") + str_endpause)
        self.write(patch, b"\xCB" + qt_encode(" That's it, show's over.") + str_endpause)
        self.seek(patch, int("bda09", 16) + rom_offset)
        self.write(patch, b"\xCB" + qt_encode("   Thanks for playing!") + str_endpause)
        self.seek(patch, int("bdca5", 16) + rom_offset)
        self.write(patch, qt_encode("Wait a minute...") + b"\xCB" + qt_encode("what happened to Hamlet?") + str_endpause)
        self.seek(patch, int("bdd48", 16) + rom_offset)
        self.write(patch, qt_encode("Um...") + b"\xCB" + qt_encode("I wouldn't worry about") + b"\xCB" + qt_encode("that too much...") + str_endpause)
        self.seek(patch, int("bddf6", 16) + rom_offset)
        self.write(patch, qt_encode("Well, but...") + str_endpause)
        self.seek(patch, int("bde16", 16) + rom_offset)
        self.write(patch, qt_encode("Shh... here,") + b"\xCB" + qt_encode("have some bacon.") + str_endpause)

        # Thank the playtesters
        self.seek(patch, int("be056", 16) + rom_offset)
        self.write(patch, b"\x80\xfa")
        self.seek(patch, int("bfa80", 16) + rom_offset)
        self.write(patch, b"\xD3\xD2\x00\xD5\x00" + qt_encode("Contributors and Testers:") + b"\xCB")
        self.write(patch, qt_encode("-Alchemic   -Austin21300") + b"\xCB")
        self.write(patch, qt_encode("-Atlas      -BOWIEtheHERO") + b"\xCB")
        self.write(patch, qt_encode("-Bonzaibier -BubbaSWalter") + b"\xC9\xB4\xCE")

        self.write(patch, qt_encode("-Crazyhaze  -DerTolleIgel") + b"\xCB")
        self.write(patch, qt_encode("-DoodSF     -djtifaheart") + b"\xCB")
        self.write(patch, qt_encode("-Eppy37     -Keypaladin") + b"\xCB")
        self.write(patch, qt_encode("-Lassic") + b"\xC9\xB4\xCE")

        self.write(patch, qt_encode("-Le Hulk    -Plan") + b"\xCB")
        self.write(patch, qt_encode("-manafreak  -Pozzum Senpai") + b"\xCB")
        self.write(patch, qt_encode("-Mikan      -roeya") + b"\xCB")
        self.write(patch, qt_encode("-Mr Freet") + b"\xC9\xB4\xCE")

        self.write(patch, qt_encode("-Scheris    -SmashManiac") + b"\xCB")
        self.write(patch, qt_encode("-SDiezal    -solarcell007") + b"\xCB")
        self.write(patch, qt_encode("-Skarsnik   -steve hacks") + b"\xCB")
        self.write(patch, qt_encode("-Skipsy") + b"\xC9\xB4\xCE")

        self.write(patch, qt_encode("-Sye990     -Verallix") + b"\xCB")
        self.write(patch, qt_encode("-Tsurana    -Volor") + b"\xCB")
        self.write(patch, qt_encode("-Tymekeeper -Veetorp") + b"\xC9\xB4\xCE")

        self.write(patch, qt_encode("-Voranthe   -Xyrcord") + b"\xCB")
        self.write(patch, qt_encode("-Wilddin    -Z4t0x") + b"\xCB")
        self.write(patch, qt_encode("-wormsofcan -ZockerStu") + b"\xC9\xB4\xCE")

        self.write(patch, b"\xCB" + qt_encode("  Thank you all so much!"))
        self.write(patch, b"\xCB" + qt_encode("     This was so fun!"))

        self.write(patch, b"\xC9\xF0\xC8\xCA")

        ##########################################################################
        #                           Modify Jeweler event
        ##########################################################################
        # Replace status upgrades with item acquisitions
        f_jeweler = open(BIN_PATH + "08cec9_jeweler.bin", "rb")
        self.seek(patch, int("8cec9", 16) + rom_offset)
        self.write(patch, f_jeweler.read())
        f_jeweler.close

        # Allow jeweler to take 2- and 3-jewel items
        f_jeweler2 = open(BIN_PATH + "08fd90_jeweler2.bin", "rb")
        self.seek(patch, int("8fd90", 16) + rom_offset)
        self.write(patch, f_jeweler2.read())
        f_jeweler2.close

        # Jeweler doesn't disappear when defeated
        self.seek(patch, int("8cea5", 16) + rom_offset)
        self.write(patch, b"\x10\x00")

        # Jeweler warps you to credits for Red Jewel hunts
        if settings.goal.value == Goal.RED_JEWEL_HUNT.value:
            self.seek(patch, int("8d32a", 16) + rom_offset)
            self.write(patch, b"\xE5\x00\x00\x00\x00\x00\x00\x11")
            self.seek(patch, int("8d2d8", 16) + rom_offset)
            self.write(patch, qt_encode("Beat the game"))

        ##########################################################################
        #                          Update dark space code
        ##########################################################################
        # Allow player to return to South Cape at any time
        # Also, checks for end game state and warps to final boss
        f_darkspace = open(BIN_PATH + "08db07_darkspace.bin", "rb")
        self.seek(patch, int("8db07", 16) + rom_offset)
        self.write(patch, f_darkspace.read())
        f_darkspace.close

        # Shorten ability acquisition text
        self.seek(patch, int("8eb81", 16) + rom_offset)
        self.write(patch, b"\xc0")

        # Cut out ability explanation text
        self.seek(patch, int("8eb15", 16) + rom_offset)
        self.write(patch, b"\xa4\x26\xa9\x00\x00\x99\x24\x00\x02\x04\x16")
        self.write(patch, b"\x02\xda\x01\xa9\xf0\xff\x1c\x5a\x06\x02\xe0")

        # Remove abilities from all Dark Spaces
        self.seek(patch, int("c8b34", 16) + rom_offset)  # Itory Village (Psycho Dash)
        self.write(patch, b"\x01")
        self.seek(patch, int("c9b49", 16) + rom_offset)  # Diamond Mine (Dark Friar)
        self.write(patch, b"\x03")
        self.seek(patch, int("caa99", 16) + rom_offset)  # Mu (Psycho Slide)
        self.write(patch, b"\x03")
        self.seek(patch, int("cbb80", 16) + rom_offset)  # Great Wall (Spin Dash)
        self.write(patch, b"\x03")
        self.seek(patch, int("cc7b8", 16) + rom_offset)  # Mt. Temple (Aura Barrier)
        self.write(patch, b"\x03")
        self.seek(patch, int("cd0a2", 16) + rom_offset)  # Ankor Wat (Earthquaker)
        self.write(patch, b"\x03")

        # Insert subroutine that can force change back to Will
        f_forcechange = open(BIN_PATH + "08fd30_forcechange.bin", "rb")
        self.seek(patch, int("8fd30", 16) + rom_offset)
        self.write(patch, f_forcechange.read())
        f_forcechange.close

        ##########################################################################
        #                          Fix special attacks
        ##########################################################################
        # Earthquaker no longer charges; Aura Barrier can be used w/o Friar
        self.seek(patch, int("2b871", 16) + rom_offset)
        self.write(patch, b"\x30")

        # Insert new code to explicitly check for Psycho Dash and Friar
        self.seek(patch, int("2f090", 16) + rom_offset)
        self.write(patch, b"\xAD\xA2\x0A\x89\x01\x00\xF0\x06\xA9\xA0\xBE\x20\x26\xB9\x4C\x01\xB9")  # Psycho Dash @2f090
        self.write(patch, b"\xAD\xA2\x0A\x89\x10\x00\xF0\x06\xA9\x3B\xBB\x20\x26\xB9\x4C\x01\xB9")  # Dark Friar @2f0a1

        # Insert jumps to new code
        self.seek(patch, int("2b858", 16) + rom_offset)  # Psycho Dash
        self.write(patch, b"\x4c\x90\xf0")
        self.seek(patch, int("2b8df", 16) + rom_offset)  # Dark Friar
        self.write(patch, b"\x4c\xa1\xf0")

        ##########################################################################
        #                      Disable NPCs in various maps
        ##########################################################################
        # School
        self.seek(patch, int("48d25", 16) + rom_offset)  # Lance
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("48d72", 16) + rom_offset)  # Seth
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("48d99", 16) + rom_offset)  # Erik
        self.write(patch, b"\xe0\x6b")

        # Seaside cave
        self.seek(patch, int("4afb6", 16) + rom_offset)  # Playing cards
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("4b06c", 16) + rom_offset)  # Lance
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("4b459", 16) + rom_offset)  # Seth
        self.write(patch, b"\xe0\x6b")

        # Edward's Castle
        self.seek(patch, int("4cb5e", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("9bc37", 16) + rom_offset)  # Lilly's flower
        self.write(patch, b"\x02\xe0\x6b")

        # Itory Village
        self.seek(patch, int("4e06e", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("4f0a7", 16) + rom_offset)  # Lola
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("4ef78", 16) + rom_offset)  # Bill
        self.write(patch, b"\xe0\x6b")

        # Lilly's House
        self.seek(patch, int("4e1b7", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")

        # Moon Tribe
        # self.seek(patch, int("4f445",16)+rom_offset)   # Lilly
        # self.write(patch, b"\xe0\x6b")

        # Inca Ruins Entrance
        self.seek(patch, int("9ca03", 16) + rom_offset)  # Lilly
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("9cea7", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")

        # Diamond Coast
        # self.seek(patch, int("5aaa2",16)+rom_offset)   # Kara
        # self.write(patch, b"\xe0\x6b")

        # Freejia Hotel
        self.seek(patch, int("5c782", 16) + rom_offset)  # Lance
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5cb34", 16) + rom_offset)  # Erik
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5c5b7", 16) + rom_offset)  # Lilly??
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5c45a", 16) + rom_offset)  # Kara??
        self.write(patch, b"\xe0\x6b")

        # Nazca Plain
        self.seek(patch, int("5e845", 16) + rom_offset)
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5ec8f", 16) + rom_offset)
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5eea5", 16) + rom_offset)
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5efed", 16) + rom_offset)
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("5f1fd", 16) + rom_offset)
        self.write(patch, b"\xe0\x6b")

        # Seaside Palace
        self.seek(patch, int("68689", 16) + rom_offset)  # Lilly
        self.write(patch, b"\xe0\x6b")

        # Mu
        self.seek(patch, int("6a2cc", 16) + rom_offset)  # Erik
        self.write(patch, b"\xe0\x6b")

        # Watermia
        self.seek(patch, int("7a871", 16) + rom_offset)  # Lilly
        self.write(patch, b"\xe0\x6b")

        # Euro
        self.seek(patch, int("7d989", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("7daa1", 16) + rom_offset)  # Erik
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("7db29", 16) + rom_offset)  # Neil
        self.write(patch, b"\xe0\x6b")

        # Natives' Village
        # self.seek(patch, int("8805d",16)+rom_offset)   # Kara
        # self.write(patch, b"\xe0\x6b")
        # self.seek(patch, int("8865f",16)+rom_offset)   # Hamlet
        # self.write(patch, b"\xe0\x6b")
        # self.seek(patch, int("8854a",16)+rom_offset)   # Erik
        # self.write(patch, b"\xe0\x6b")

        # Dao
        self.seek(patch, int("8a4af", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("8a56b", 16) + rom_offset)  # Erik
        self.write(patch, b"\xe0\x6b")
        # self.seek(patch, int("980cc",16)+rom_offset)   # Spirit
        # self.write(patch, b"\xe0\x6b")

        # Pyramid
        self.seek(patch, int("8b7a1", 16) + rom_offset)  # Kara
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("8b822", 16) + rom_offset)  # Jackal
        self.write(patch, b"\xe0\x6b")

        # Babel
        self.seek(patch, int("99e90", 16) + rom_offset)  # Kara 1
        self.write(patch, b"\xe0\x6b")
        self.seek(patch, int("98519", 16) + rom_offset)  # Kara 2
        self.write(patch, b"\xe0\x6b")

        ##########################################################################
        #                Prepare Room/Boss Rewards for Randomization
        ##########################################################################
        # Remove existing rewards
        f_roomrewards = open(BIN_PATH + "01aade_roomrewards.bin", "rb")
        self.seek(patch, int("1aade", 16) + rom_offset)
        self.write(patch, f_roomrewards.read())
        f_roomrewards.close

        # Make room-clearing HP rewards grant +3 HP each
        self.seek(patch, int("e041", 16) + rom_offset)
        self.write(patch, b"\x03")

        # Make boss rewards also grant +3 HP per unclaimed reward
        self.seek(patch, int("c381", 16) + rom_offset)
        self.write(patch, b"\x20\x90\xf4")
        self.seek(patch, int("f490", 16) + rom_offset)
        self.write(patch, b"\xee\xca\x0a\xee\xca\x0a\xee\xca\x0a\x60")

        # Change boss room ranges
        self.seek(patch, int("c31a", 16) + rom_offset)
        self.write(patch, b"\x67\x5A\x73\x00\x8A\x82\xA8\x00\xDD\xCC\xDD\x00\xEA\xB0\xBF\x00")
        # self.write(patch, b"\xF6\xB0\xBF\x00")   # If Solid Arm ever grants Babel rewards

        # Add boss reward events to Babel and Jeweler Mansion
        # self.seek(patch, int("ce3cb",16)+rom_offset)  # Solid Arm
        # self.write(patch, b"\x00\x01\x01\xDF\xA5\x8B\x00\x00\x01\x01\xBB\xC2\x80\x00\xFF\xCA")
        self.seek(patch, int("ce536", 16) + rom_offset)  # Mummy Queen (Babel)
        self.write(patch, b"\x00\x01\x01\xBB\xC2\x80\x00\xFF\xCA")

        # Black Glasses allow you to "see" which upgrades are available
        f_startmenu = open(BIN_PATH + "03fdb0_startmenu.bin", "rb")
        self.seek(patch, int("3fdb0", 16) + rom_offset)
        self.write(patch, f_startmenu.read())
        f_startmenu.close
        self.seek(patch, int("381d6", 16) + rom_offset)
        self.write(patch, b"\x4C\xB0\xFD")

        # Change start menu "FORCE" text
        self.seek(patch, int("1ff70", 16) + rom_offset)
        self.write(patch, b"\x01\xC6\x01\x03\x14\x2D\x33\x48\x50\x00")  # "+3HP"
        self.seek(patch, int("1ff80", 16) + rom_offset)
        self.write(patch, b"\x01\xC6\x01\x03\x14\x2D\x31\x53\x54\x52\x00")  # "+1STR"
        self.seek(patch, int("1ff90", 16) + rom_offset)
        self.write(patch, b"\x01\xC6\x01\x03\x14\x2D\x31\x44\x45\x46\x00")  # "+1DEF"

        ##########################################################################
        #                        Balance Enemy Stats
        ##########################################################################
        # Determine enemy stats, by difficulty
        if mode == 0:
            f_enemies = open(BIN_PATH + "01abf0_enemieseasy.bin", "rb")
        elif mode == 1:
            f_enemies = open(BIN_PATH + "01abf0_enemiesnormal.bin", "rb")
        elif mode == 2:
            f_enemies = open(BIN_PATH + "01abf0_enemieshard.bin", "rb")
        elif mode == 3:
            f_enemies = open(BIN_PATH + "01abf0_enemiesextreme.bin", "rb")

        if mode < 4:
            self.seek(patch, int("1abf0", 16) + rom_offset)
            self.write(patch, f_enemies.read())
            f_enemies.close

        ##########################################################################
        #                            Randomize Inca tile
        ##########################################################################
        # Prepare file for uncompressed map data
        f_incamapblank = open(BIN_PATH + "incamapblank.bin", "rb")
        f_incamap = tempfile.TemporaryFile()
        f_incamap.write(f_incamapblank.read())
        f_incamapblank.close

        # Set random X/Y for new Inca tile
        inca_x = random.randint(0, 11)
        inca_y = random.randint(0, 5)

        # Modify coordinates in event data
        inca_str = format(2 * inca_x + 4, "02x") + format(15 + 2 * inca_y, "02x")
        inca_str = inca_str + format(7 + 2 * inca_x, "02x") + format(18 + 2 * inca_y, "02x")
        self.seek(patch, int("9c683", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(inca_str))

        # Remove Wind Melody when door opens
        self.seek(patch, int("9c660", 16) + rom_offset)
        self.write(patch, b"\x02\xcd\x12\x01\x02\xd5\x08\x02\xe0")
        self.seek(patch, int("9c676", 16) + rom_offset)
        self.write(patch, b"\x67")
        self.seek(patch, int("9c6a3", 16) + rom_offset)
        self.write(patch, b"\x02\xd0\x10\x01\x60\xc6")

        # Determine address location for new tile in uncompressed map data
        row = 32 + 2 * inca_y + 16 * int(inca_x / 6)
        column = 2 * ((inca_x + 2) % 8)
        addr = 16 * row + column

        # Write single tile at new location in uncompressed data
        f_incamap.seek(addr)
        f_incamap.write(b"\x40\x41\x00\x00\x00\x00\x00\x00\x00")
        f_incamap.write(b"\x00\x00\x00\x00\x00\x00\x00\x42\x43")
        f_incamap.seek(0)

        # Compress map data and write to file
        f_incamapcomp = tempfile.TemporaryFile()
        f_incamapcomp.write(qt_compress(f_incamap.read()))
        f_incamapcomp.seek(0)
        f_incamap.close

        # Insert new compressed map data
        # self.seek(patch, int("1f38db",16)+rom_offset)
        self.seek(patch, int("1f3ea0", 16) + rom_offset)
        self.write(patch, b"\x02\x02")
        self.write(patch, f_incamapcomp.read())
        f_incamapcomp.close

        # Direct map arrangement pointer to new data - NO LONGER NECESSARY
        # self.seek(patch, int("d8703",16)+rom_offset)
        # self.write(patch, b"\xa0\x3e")

        ##########################################################################
        #                       Randomize heiroglyph order
        ##########################################################################
        # Determine random order
        hieroglyph_order = [1, 2, 3, 4, 5, 6]
        random.shuffle(hieroglyph_order)

        # Update Father's Journal with correct order
        self.seek(patch, int("39e9a", 16) + rom_offset)
        for x in hieroglyph_order:
            if x == 1:
                self.write(patch, b"\xc0\xc1")
            elif x == 2:
                self.write(patch, b"\xc2\xc3")
            elif x == 3:
                self.write(patch, b"\xc4\xc5")
            elif x == 4:
                self.write(patch, b"\xc6\xc7")
            elif x == 5:
                self.write(patch, b"\xc8\xc9")
            elif x == 6:
                self.write(patch, b"\xca\xcb")

        # Update sprite pointers for hieroglyph items, Item 1e is @10803c
        self.seek(patch, int("10803c", 16) + rom_offset)
        for x in hieroglyph_order:
            if x == 1:
                self.write(patch, b"\xde\x81")
            if x == 2:
                self.write(patch, b"\xe4\x81")
            if x == 3:
                self.write(patch, b"\xea\x81")
            if x == 4:
                self.write(patch, b"\xf0\x81")
            if x == 5:
                self.write(patch, b"\xf6\x81")
            if x == 6:
                self.write(patch, b"\xfc\x81")

        # Update which tiles are called when hieroglyph is placed
        i = 0
        for x in hieroglyph_order:
            self.seek(patch, int("39b89", 16) + 5 * i + rom_offset)
            if x == 1:
                self.write(patch, b"\x84")
            elif x == 2:
                self.write(patch, b"\x85")
            elif x == 3:
                self.write(patch, b"\x86")
            elif x == 4:
                self.write(patch, b"\x8c")
            elif x == 5:
                self.write(patch, b"\x8d")
            elif x == 6:
                self.write(patch, b"\x8e")
            i += 1

        # Update which tiles are called from placement flags
        self.seek(patch, int("8cb94", 16) + rom_offset)
        for x in hieroglyph_order:
            if x == 1:
                self.write(patch, b"\x84")
            elif x == 2:
                self.write(patch, b"\x85")
            elif x == 3:
                self.write(patch, b"\x86")
            elif x == 4:
                self.write(patch, b"\x8c")
            elif x == 5:
                self.write(patch, b"\x8d")
            elif x == 6:
                self.write(patch, b"\x8e")

        ##########################################################################
        #                    Randomize Jeweler Reward amounts
        ##########################################################################
        # Randomize jeweler reward values
        gem = []
        gem.append(random.randint(1, 3))
        gem.append(random.randint(4, 6))
        gem.append(random.randint(7, 9))
        gem.append(random.randint(10, 14))
        gem.append(random.randint(16, 24))
        gem.append(random.randint(26, 34))
        gem.append(random.randint(36, 50))

        if settings.goal.value == Goal.RED_JEWEL_HUNT.value:
            if mode == 0:
                gem[6] = GEMS_EASY
            elif mode == 1:
                gem[6] = GEMS_NORMAL
            else:
                gem[6] = GEMS_HARD

        gem_str = []

        # Write new values into reward check code (BCD format)
        gem_str.append(format(int(gem[0] / 10), "x") + format(gem[0] % 10, "x"))
        self.seek(patch, int("8cee0", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[0]))

        gem_str.append(format(int(gem[1] / 10), "x") + format(gem[1] % 10, "x"))
        self.seek(patch, int("8cef1", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[1]))

        gem_str.append(format(int(gem[2] / 10), "x") + format(gem[2] % 10, "x"))
        self.seek(patch, int("8cf02", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[2]))

        gem_str.append(format(int(gem[3] / 10), "x") + format(gem[3] % 10, "x"))
        self.seek(patch, int("8cf13", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[3]))

        gem_str.append(format(int(gem[4] / 10), "x") + format(gem[4] % 10, "x"))
        self.seek(patch, int("8cf24", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[4]))

        gem_str.append(format(int(gem[5] / 10), "x") + format(gem[5] % 10, "x"))
        self.seek(patch, int("8cf35", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[5]))

        gem_str.append(format(int(gem[6] / 10), "x") + format(gem[6] % 10, "x"))
        self.seek(patch, int("8cf40", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[6]))

        # Write new values into inventory table (Quintet text table format)
        # NOTE: Hard-coded for 1st, 2nd and 3rd rewards each < 10
        gem_str[0] = format(2, "x") + format(gem[0] % 10, "x")
        self.seek(patch, int("8d26f", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[0]))

        gem_str[1] = format(2, "x") + format(gem[1] % 10, "x")
        self.seek(patch, int("8d283", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[1]))

        gem_str[2] = format(2, "x") + format(gem[2] % 10, "x")
        self.seek(patch, int("8d297", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[2]))

        gem_str[3] = format(2, "x") + format(int(gem[3] / 10), "x")
        gem_str[3] = gem_str[3] + format(2, "x") + format(gem[3] % 10, "x")
        self.seek(patch, int("8d2aa", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[3]))

        gem_str[4] = format(2, "x") + format(int(gem[4] / 10), "x")
        gem_str[4] = gem_str[4] + format(2, "x") + format(gem[4] % 10, "x")
        self.seek(patch, int("8d2be", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[4]))

        gem_str[5] = format(2, "x") + format(int(gem[5] / 10), "x")
        gem_str[5] = gem_str[5] + format(2, "x") + format(gem[5] % 10, "x")
        self.seek(patch, int("8d2d2", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[5]))

        gem_str[6] = format(2, "x") + format(int(gem[6] / 10), "x")
        gem_str[6] = gem_str[6] + format(2, "x") + format(gem[6] % 10, "x")
        self.seek(patch, int("8d2e6", 16) + rom_offset)
        self.write(patch, binascii.unhexlify(gem_str[6]))

        ##########################################################################
        #                    Randomize Mystic Statue requirement
        ##########################################################################
        statueOrder = [1, 2, 3, 4, 5, 6]
        random.shuffle(statueOrder)

        statues = []
        statues_hex = []

        i = 0
        while i < statues_required:
            if statueOrder[i] == 1:
                statues.append(1)
                statues_hex.append(b"\x21")

                # Check for Mystic Statue possession at end game state
                self.seek(patch, int("8dd19", 16) + rom_offset)
                self.write(patch, b"\xf8")

            if statueOrder[i] == 2:
                statues.append(2)
                statues_hex.append(b"\x22")

                # Check for Mystic Statue possession at end game state
                self.seek(patch, int("8dd1f", 16) + rom_offset)
                self.write(patch, b"\xf9")

            if statueOrder[i] == 3:
                statues.append(3)
                statues_hex.append(b"\x23")

                # Check for Mystic Statue possession at end game state
                self.seek(patch, int("8dd25", 16) + rom_offset)
                self.write(patch, b"\xfa")

                # Restrict removal of Rama Statues from inventory
                self.seek(patch, int("1e12c", 16) + rom_offset)
                self.write(patch, b"\x9f")

            if statueOrder[i] == 4:
                statues.append(4)
                statues_hex.append(b"\x24")

                # Check for Mystic Statue possession at end game state
                self.seek(patch, int("8dd2b", 16) + rom_offset)
                self.write(patch, b"\xfb")

            if statueOrder[i] == 5:
                statues.append(5)
                statues_hex.append(b"\x25")

                # Check for Mystic Statue possession at end game state
                self.seek(patch, int("8dd31", 16) + rom_offset)
                self.write(patch, b"\xfc")

                # Restrict removal of Hieroglyphs from inventory
                self.seek(patch, int("1e12d", 16) + rom_offset)
                self.write(patch, b"\xf7\xff")

            if statueOrder[i] == 6:
                statues.append(6)
                statues_hex.append(b"\x26")

                # Check for Mystic Statue possession at end game state
                self.seek(patch, int("8dd37", 16) + rom_offset)
                self.write(patch, b"\xfd")

            i += 1

        # Can't face Dark Gaia in Red Jewel hunts
        if settings.goal.value != Goal.DARK_GAIA.value:
            self.seek(patch, int("8dd0d", 16) + rom_offset)
            self.write(patch, b"\x10\x01")

        statues.sort()
        statues_hex.sort()

        # Teacher at start spoils required Mystic Statues
        statue_str = ""
        if len(statues_hex) == 0:
            statue_str = b"\xd3\x4d\x8e\xac\xd6\xd2\x80\xa2\x84\xac"
            statue_str += b"\xa2\x84\xa1\xa5\x88\xa2\x84\x83\x4f\xc0"

        else:
            statue_str = b"\xd3\x69\x8e\xa5\xac\x8d\x84\x84\x83\xac"
            statue_str += b"\x4c\xa9\xa3\xa4\x88\x82\xac\x63\xa4\x80\xa4\xa5\x84"
            if len(statues_hex) == 1:
                statue_str += b"\xac"
                statue_str += statues_hex[0]
                statue_str += b"\x4f\xc0"

            else:
                statue_str += b"\xa3\xcb"
                while statues_hex:
                    if len(statues_hex) > 1:
                        statue_str += statues_hex[0]
                        statue_str += b"\x2b\xac"

                    else:
                        statue_str += b"\x80\x8d\x83\xac"
                        statue_str += statues_hex[0]
                        statue_str += b"\x4f\xc0"

                    statues_hex.pop(0)

        self.seek(patch, int("48aab", 16) + rom_offset)
        self.write(patch, statue_str)

        ##########################################################################
        #                   Randomize Location of Kara Portrait
        #       Sets spoiler in Lance's Letter and places portrait sprite
        ##########################################################################
        # Determine random location ID
        kara_location = random.randint(1, 5)
        # ANGEL_TILESET = b"\x03\x00\x10\x10\x36\x18\xca\x01"
        # ANGEL_PALETTE = b"\x04\x00\x60\xa0\x80\x01\xdf"
        # ANGEL_SPRTESET = b"\x10\x43\x0a\x00\x00\x00\xda"

        # Modify Kara Portrait event
        self.seek(patch, int("6d153", 16) + rom_offset)
        self.write(patch, b"\x8a")
        self.seek(patch, int("6d169", 16) + rom_offset)
        self.write(patch, b"\x02\xd2\x8a\x01\x02\xe0")
        self.seek(patch, int("6d25c", 16) + rom_offset)
        self.write(patch, b"\x8a")
        self.seek(patch, int("6d27e", 16) + rom_offset)
        self.write(patch, qt_encode("Hurry boy, she's waiting there for you!") + b"\xc0")
        self.seek(patch, int("6d305", 16) + rom_offset)
        self.write(patch, qt_encode("Kara's portrait. If only you had Magic Dust...") + b"\xc0")

        if kara_location == KARA_ANGEL:
            # Set spoiler for Kara's location in Lance's Letter
            self.seek(patch, int("39521", 16) + rom_offset)
            self.write(patch, b"\x40\x8d\x86\x84\x8b\xac\x66\x88\x8b\x8b\x80\x86\x84")

        else:
            # Remove Kara's painting from Ishtar's Studio
            self.seek(patch, int("cb397", 16) + rom_offset)
            self.write(patch, b"\x18")

            if kara_location == KARA_EDWARDS:  # Underground tunnel exit, map 19 (0x13)
                # Set spoiler for Kara's location in Lance's Letter
                self.seek(patch, int("39521", 16) + rom_offset)
                self.write(patch, b"\x44\x83\xa7\x80\xa2\x83\x0e\xa3\xac\x60\xa2\x88\xa3\x8e\x8d")

                # Set map check ID for Magic Dust item event
                self.seek(patch, int("393a9", 16) + rom_offset)
                self.write(patch, b"\x13\x00\xD0\x08\x02\x45\x0b\x0b\x0d\x0d")

                # Set Kara painting event in appropriate map
                self.seek(patch, int("c8ac5", 16) + rom_offset)
                self.write(patch, b"\x0b\x0b\x00\x4e\xd1\x86\xff\xca")  # this is correct

                # Adjust sprite palette
                self.seek(patch, int("6d15b", 16) + rom_offset)
                self.write(patch, b"\x02\xb6\x30")

            elif kara_location == KARA_MINE:
                # Set spoiler for Kara's location in Lance's Letter
                self.seek(patch, int("39521", 16) + rom_offset)
                self.write(patch, b"\x43\x88\x80\x8c\x8e\x8d\x83\xac\x4c\x88\x8d\x84")

                # Set map check ID for Magic Dust item event
                self.seek(patch, int("393a9", 16) + rom_offset)
                self.write(patch, b"\x47\x00\xD0\x08\x02\x45\x0b\x24\x0d\x26")

                # Change "Sam" to "Samlet"
                self.seek(patch, int("5fee0", 16) + rom_offset)
                self.write(patch, b"\x1a\x00\x10\x02\xc0\x9e\xd2\x02\x0b\x02\xc1\x6b")
                self.seek(patch, int("5d2bd", 16) + rom_offset)
                self.write(patch, b"\xf0\xd2")
                self.seek(patch, int("5d2f0", 16) + rom_offset)
                self.write(patch, b"\xd3\xc2\x05" + qt_encode("Samlet: I'll never forget you!") + b"\xc0")
                self.seek(patch, int("c9c78", 16) + rom_offset)
                self.write(patch, b"\x03\x2a\x00\xe0\xfe\x85")

                # Disable Remus
                self.seek(patch, int("5d15e", 16) + rom_offset)
                self.write(patch, b"\xe0")

                # Assign Kara painting spriteset to appropriate Map
                self.seek(patch, 0)
                addr = self.find(patch, b"\x15\x0C\x00\x49\x00\x02", int("d8000", 16) + rom_offset)
                if addr < 0:
                    self.logger.error("ERROR: Could not change spriteset for Diamond Mine")
                else:
                    self.seek(patch, addr)
                    self.write(patch, b"\x15\x25")

                # Set Kara painting event in appropriate map
                self.seek(patch, int("c9c6a", 16) + rom_offset)
                self.write(patch, b"\x0b\x24\x00\x4e\xd1\x86")

                # Adjust sprite
                # self.seek(patch, int("6d14e",16)+rom_offset)
                # self.write(patch, b"\x2a")
                self.seek(patch, int("6d15b", 16) + rom_offset)
                self.write(patch, b"\x02\xb6\x30")

            elif kara_location == KARA_KRESS:

                # Set spoiler for Kara's location in Lance's Letter
                self.seek(patch, int("39521", 16) + rom_offset)
                self.write(patch, b"\x4c\xa4\x2a\xac\x4a\xa2\x84\xa3\xa3")

                # Set map check ID for Magic Dust item event
                self.seek(patch, int("393a9", 16) + rom_offset)
                self.write(patch, b"\xa9\x00\xD0\x08\x02\x45\x12\x06\x14\x08")

                # Set Kara painting event in appropriate map
                # Map #169, written into unused Map #104 (Seaside Tunnel)
                self.seek(patch, int("c8152", 16) + rom_offset)
                self.write(patch, b"\x42\xad")
                self.seek(patch, int("cad42", 16) + rom_offset)
                self.write(patch, b"\x05\x0a\x00\x8c\xc3\x82\x00\x00\x00\x00\xed\xea\x80\x00\xdf")
                self.write(patch, b"\xdf\x00\x4d\xe9\x80\x00\x12\x06\x00\x4e\xd1\x86\x00\xff\xca")

                # Adjust sprite
                self.seek(patch, int("6d15b", 16) + rom_offset)
                self.write(patch, b"\x02\xb6\x30")

            elif kara_location == KARA_ANKORWAT:
                # Set spoiler for Kara's location in Lance's Letter
                self.seek(patch, int("39521", 16) + rom_offset)
                self.write(patch, b"\x40\x8d\x8a\x8e\xa2\xac\x67\x80\xa4")

                # Set map check ID for Magic Dust item event
                self.seek(patch, int("393a9", 16) + rom_offset)
                self.write(patch, b"\xbf\x00\xD0\x08\x02\x45\x1a\x10\x1c\x12")

                # Set Kara painting event in appropriate map (Map #191)
                # Map #191, written into unused Map #104 (Seaside Tunnel)
                self.seek(patch, int("c817e", 16) + rom_offset)
                self.write(patch, b"\x42\xad")
                self.seek(patch, int("cad42", 16) + rom_offset)
                self.write(patch, b"\x05\x0a\x02\x8c\xc3\x82\x00\x00\x00\x00\xed\xea\x80\x00\x0f")
                self.write(patch, b"\x0b\x00\xa3\x9a\x88\x00\x1a\x10\x00\x4e\xd1\x86\x00\xff\xca")

                # Adjust sprite
                self.seek(patch, int("6d15b", 16) + rom_offset)
                self.write(patch, b"\x02\xb6\x30")

        ##########################################################################
        #                          Have fun with death text
        ##########################################################################
        death_list = []
        death_list.append(
            b"\x2d\x48\xa4\xac\xd6\xa3\xa3\x8e\xac\x87\x80\xa0\xa0\x84\x8d\xa3\xac\xd6\xd7\xcb\xd6\xfe\x85\xa2\x88\x84\x8d\x83\xac\xd7\x73\x88\xa3\xac\xd7\x89\xcb\x4c\x4e\x63\x64\x4b\x69\xac\x83\x84\x80\x83\x2a\x2e\xcb\xac\xac\x6d\x4c\x88\xa2\x80\x82\x8b\x84\xac\x4c\x80\xa8\xc0")
        death_list.append(
            b"\x2d\x69\x8e\xa5\xac\xd7\x9e\x80\xac\x83\x84\x82\x84\x8d\xa4\xac\x85\x84\x8b\x8b\x8e\xa7\x2a\xcb\x48\xac\x87\x80\xa4\x84\xac\xa4\x8e\xac\x8a\x88\x8b\x8b\xac\xa9\x8e\xa5\x2a\x2e\xcb\xac\xac\x6d\x48\x8d\x88\x86\x8e\xac\x4c\x8e\x8d\xa4\x8e\xa9\x80\xc0")
        death_list.append(
            b"\x2d\x64\x8e\xac\x83\x88\x84\xac\xd6\xef\x81\x84\xac\x80\xac\xd6\x95\xcb\x80\x83\xa6\x84\x8d\xa4\xa5\xa2\x84\x2a\x2e\xcb\xac\xac\x6d\x60\x84\xa4\x84\xa2\xac\x41\x80\x8d\x8d\x88\x8d\x86\xc0")
        death_list.append(
            b"\x2d\x4b\x88\x8a\x84\xac\xd6\x94\xa3\x8b\x84\x84\xa0\xac\x82\x8e\x8c\x84\xa3\xcb\x80\x85\xa4\x84\xa2\xac\x87\x80\xa2\x83\xac\xa7\x8e\xa2\x8a\xab\xac\xd6\x94\xa2\x84\xa3\xa4\xcb\x82\x8e\x8c\x84\xa3\xac\x80\x85\xa4\x84\xa2\xac\x80\x8d\xac\x87\x8e\x8d\x84\xa3\xa4\xcb\x8b\x88\x85\x84\x2a\x2e\xac\xac\xac\xac\x6d\x64\xa5\xa2\x81\x8e\xc0")
        death_list.append(
            b"\x2d\x45\x8e\x8b\x8b\x8e\xa7\xac\xd6\xfe\x83\xa2\x84\x80\x8c\xa3\x2a\x2a\x2a\xcb\x83\x84\x80\xa4\x87\xac\x88\xa3\xac\x8d\x8e\xa4\x87\x88\x8d\x86\xab\xac\xd6\xb0\x88\xa3\xcb\x84\xa6\x84\xa2\xa9\xa4\x87\x88\x8d\x86\x2a\x2e\xcb\xac\xac\x6d\x63\xa4\x84\x85\x80\x8d\xac\x4a\x80\xa2\x8b\xac\x63\xa4\x84\x85\x80\x8d\xa3\xa3\x8e\x8d\xc0")
        death_list.append(
            b"\x2d\x40\x8b\x8b\xac\x83\x84\x80\xa4\x87\xa3\xac\x80\xa2\x84\xac\xa3\xa5\x83\x83\x84\x8d\xab\xac\x8d\x8e\xcb\xd6\xb8\x87\x8e\xa7\xac\x86\xa2\x80\x83\xa5\x80\x8b\xac\xa4\x87\x84\xcb\x83\xa9\x88\x8d\x86\xac\x8c\x80\xa9\xac\x81\x84\x2a\x2e\xcb\xac\xac\x6d\x4c\x88\x82\x87\x80\x84\x8b\xac\x4c\x82\x43\x8e\xa7\x84\x8b\x8b\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\xa0\x84\xa2\x87\x80\xa0\xa3\xac\x80\x8d\xcb\x8e\xa2\x83\x84\x80\x8b\xab\xac\x81\xa5\xa4\xac\x88\xa4\xac\x88\xa3\xac\x8d\x8e\xa4\xac\x80\x8d\xcb\x84\xa8\xa0\x88\x80\xa4\x88\x8e\x8d\x2a\x2e\xcb\xac\xac\x6d\x40\x8b\x84\xa8\x80\x8d\x83\xa2\x84\xac\x43\xa5\x8c\x80\xa3\xc0")
        death_list.append(
            b"\x2d\xd6\x62\xd7\x95\x8c\x80\xa4\xa4\x84\xa2\x84\x83\xac\x88\x8d\xcb\x8b\x88\x85\x84\xab\xac\xd6\xf7\x86\x80\xa6\x84\xac\x88\xa4\xcb\xa7\x84\x88\x86\x87\xa4\xab\xac\xa7\x80\xa3\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x49\x84\x85\x85\xa2\x84\xa9\xac\x44\xa5\x86\x84\x8d\x88\x83\x84\xa3\xc0")
        death_list.append(
            b"\x2d\x4d\x8e\xac\x8e\x8d\x84\xac\xd7\x6d\x8e\xa5\xa4\xac\x8e\x85\xac\xd6\xd6\xcb\xd6\xf5\x80\x8b\x88\xa6\x84\x2a\x2a\x2a\xac\x84\xa8\x82\x84\xa0\xa4\xcb\x80\xa3\xa4\xa2\x8e\x8d\x80\xa5\xa4\xa3\x2a\x2e\xcb\xac\xac\x6d\x63\xa4\x84\xa7\x80\xa2\xa4\xac\x63\xa4\x80\x85\x85\x8e\xa2\x83\xc0")
        death_list.append(b"\x2d\x44\xa4\xac\xa4\xa5\xac\x41\xa2\xa5\xa4\x84\x0d\x2e\xcb\xac\xac\x6d\x49\xa5\x8b\x88\xa5\xa3\xac\x42\x80\x84\xa3\x80\xa2\xc0")
        death_list.append(
            b"\x2d\x64\x8e\xac\xa4\x87\x84\xac\xa7\x88\xaa\x80\xa2\x83\xac\x83\x84\x80\xa4\x87\xac\x88\xa3\xcb\x8c\x84\xa2\x84\x8b\xa9\xac\x80\xac\x81\x84\x8b\x88\x84\x85\x2a\x2e\xcb\xac\xac\x6d\x43\x84\x84\xa0\x80\x8a\xac\x42\x87\x8e\xa0\xa2\x80\xc0")
        death_list.append(
            b"\x2d\x44\xa6\x84\xa2\xa9\xac\xd6\xdf\xa9\x8e\xa5\xac\x83\x88\x84\xab\xac\x88\xa4\xcb\x87\xa5\xa2\xa4\xa3\x2a\x2e\xcb\xac\xac\x6d\x49\x8e\xa3\x87\xac\x47\x84\x8d\x83\x84\xa2\xa3\x8e\x8d\xc0")
        death_list.append(
            b"\x2d\x48\x85\xac\x48\xac\xd6\x98\xa4\x8e\xac\x83\x88\x84\xab\xac\x8b\x84\xa4\xac\x8c\x84\xcb\x83\x88\x84\xac\x85\x88\x86\x87\xa4\x88\x8d\x86\x2a\x2e\xcb\xac\xac\x6d\x46\x80\x81\xa2\x88\x84\x8b\xac\x46\x80\xa2\x82\x88\x80\xac\x4c\x80\xa2\xa1\xa5\x84\xaa\xc0")
        death_list.append(
            b"\x2d\x44\x80\x82\x87\xac\x83\x84\x80\xa4\x87\xac\x88\xa3\xac\x80\xa3\xac\xa5\x8d\x88\xa1\xa5\x84\xcb\x80\xa3\xac\x84\x80\x82\x87\xac\x8b\x88\x85\x84\x2a\x2e\xcb\xac\xac\x6d\x4d\x88\x82\x87\x8e\x8b\x80\xa3\xac\x67\x8e\x8b\xa4\x84\xa2\xa3\xa4\x8e\xa2\x85\x85\xc0")
        death_list.append(
            b"\x2d\x48\x8d\xac\xd6\xb0\xa9\x8e\xa5\xac\xd6\x78\xd6\xb5\xcb\x85\x8e\xa2\xa7\x80\xa2\x83\xac\xd6\xab\x81\x80\x82\x8a\x2a\x2e\xcb\xac\xac\x6d\x4c\x80\xa2\x8a\xac\x4c\x80\xa2\xa3\x8b\x80\x8d\x83\xc0")
        death_list.append(
            b"\x2d\x48\xac\x82\x80\x8d\xac\xd6\x91\xa4\x87\x84\xac\x83\x80\x88\xa3\x88\x84\xa3\xcb\x86\xa2\x8e\xa7\x88\x8d\x86\xac\xd6\xbe\x8c\x84\x2a\x2e\xcb\xac\xac\x6d\x49\x8e\x87\x8d\xac\x4a\x84\x80\xa4\xa3\xc0")
        death_list.append(
            b"\x2d\x40\xac\xa0\x84\xa2\xa3\x8e\x8d\x0e\xa3\xac\x83\x84\xa3\xa4\x88\x8d\xa9\xac\x8e\x85\xa4\x84\x8d\xcb\x84\x8d\x83\xa3\xac\xd6\x74\x87\x88\xa3\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x4c\x88\x8b\x80\x8d\xac\x4a\xa5\x8d\x83\x84\xa2\x80\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\xa4\x87\x84\xac\x83\x84\xa3\xa4\xa2\x8e\xa9\x84\xa2\xcb\x80\x8d\x83\xac\x86\x88\xa6\x84\xa2\xac\x8e\x85\xac\xa3\x84\x8d\xa3\x84\x2a\x2e\xcb\xac\xac\x6d\x40\x8d\x83\xa9\xac\x47\x80\xa2\x86\x8b\x84\xa3\x88\xa3\xc0")
        death_list.append(
            b"\x2d\x41\x84\xac\x82\x80\x8b\x8c\x2a\xac\x46\x8e\x83\xac\x80\xa7\x80\x88\xa4\xa3\xac\xa9\x8e\xa5\xcb\x80\xa4\xac\xa4\x87\x84\xac\x83\x8e\x8e\xa2\x2a\x2e\xcb\xac\xac\x6d\x46\x80\x81\xa2\x88\x84\x8b\xac\x46\x80\xa2\x82\x88\x80\xac\x4c\x80\xa2\xa1\xa5\x84\xaa\xc0")
        death_list.append(
            b"\x2d\x67\x84\xac\xd6\x91\xd7\x88\x80\x8b\x88\xa6\x84\xac\xd6\xf6\xcb\xa7\x84\xac\x80\xa2\x84\xac\x82\x8b\x8e\xa3\x84\xa3\xa4\xac\xa4\x8e\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x4d\x84\x8d\x88\x80\xac\x42\x80\x8c\xa0\x81\x84\x8b\x8b\xc0")
        death_list.append(
            b"\x43\x84\x80\xa4\x87\xac\xa4\xa7\x88\xa4\x82\x87\x84\xa3\xac\x8c\xa9\xac\x84\x80\xa2\x2f\xcb\x2d\x4b\x88\xa6\x84\xab\x2e\xac\x87\x84\xac\xa3\x80\xa9\xa3\x2a\x2a\x2a\xac\x2d\x48\x0e\x8c\xcb\x82\x8e\x8c\x88\x8d\x86\x2a\x2e\xcb\xac\xac\x6d\x66\x88\xa2\x86\x88\x8b\xc0")
        death_list.append(
            b"\x2d\x47\x84\x80\xa6\x84\x8d\xac\x88\xa3\xac\x80\xac\xd7\x90\xd6\xf4\xcb\x80\x8b\x8b\xac\xa4\x87\x84\xac\x83\x8e\x86\xa3\xac\xa9\x8e\xa5\x0e\xa6\x84\xac\xd7\x5d\xcb\x8b\x8e\xa6\x84\x83\xac\xd6\x79\xa4\x8e\xac\x86\xa2\x84\x84\xa4\xac\xa9\x8e\xa5\x2a\x2e\xcb\xac\xac\x6d\x4e\x8b\x88\xa6\x84\xa2\xac\x46\x80\xa3\xa0\x88\xa2\xa4\xaa\xc0")
        death_list.append(
            b"\x2d\x44\xa6\x84\xa2\xa9\xac\x8c\x80\x8d\xac\x83\x88\x84\xa3\x2a\xac\x4d\x8e\xa4\xcb\x84\xa6\x84\xa2\xa9\xac\x8c\x80\x8d\xac\xd7\x95\x8b\x88\xa6\x84\xa3\x2a\x2e\xcb\xac\xac\x6d\x67\x88\x8b\x8b\x88\x80\x8c\xac\x67\x80\x8b\x8b\x80\x82\x84\xc0")
        death_list.append(
            b"\x2d\x40\x8d\x83\xac\x48\xac\xa7\x88\x8b\x8b\xac\xa3\x87\x8e\xa7\xac\xa4\x87\x80\xa4\xcb\x8d\x8e\xa4\x87\x88\x8d\x86\xac\x82\x80\x8d\xac\x87\x80\xa0\xa0\x84\x8d\xac\x8c\x8e\xa2\x84\xcb\x81\x84\x80\xa5\xa4\x88\x85\xa5\x8b\xac\xa4\x87\x80\x8d\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x67\x80\x8b\xa4\xac\x67\x87\x88\xa4\x8c\x80\x8d\xc0")
        death_list.append(
            b"\x2d\x46\x84\xa4\xac\x81\xa5\xa3\xa9\xac\x8b\x88\xa6\x88\x8d\x0e\x2b\xac\x8e\xa2\xac\x86\x84\xa4\xcb\x81\xa5\xa3\xa9\xac\x83\xa9\x88\x8d\x0e\x2a\x2e\xcb\xac\xac\x6d\x40\x8d\x83\xa9\xac\x43\xa5\x85\xa2\x84\xa3\x8d\x84\xc0")
        death_list.append(
            b"\x2d\x69\x8e\xa5\x0e\xa2\x84\xac\x8a\x88\x8b\x8b\x88\x8d\x0e\xac\x8c\x84\x2b\xcb\x63\x8c\x80\x8b\x8b\xa3\x4f\x2e\xcb\xac\xac\x6d\x47\x80\x8c\x88\x8b\xa4\x8e\x8d\xac\x60\x8e\xa2\xa4\x84\xa2\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\x89\xa5\xa3\xa4\xac\x80\x8d\x8e\xa4\x87\x84\xa2\xcb\xa0\x80\xa4\x87\x2a\xac\x4E\x8d\x84\xac\xa4\x87\x80\xa4\xac\xa7\x84\xac\x80\x8b\x8b\xac\x8c\xa5\xa3\xa4\xcb\xa4\x80\x8a\x84\x2a\x2e\xcb\xac\xac\x6d\x46\x80\x8d\x83\x80\x8b\x85\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\x8d\x8e\xa4\x87\x88\x8d\x86\x2b\xac\x81\xa5\xa4\xac\xa4\x8e\xcb\x8b\x88\xa6\x84\xac\x83\x84\x85\x84\x80\xa4\x84\x83\xac\x80\x8d\x83\xac\x88\x8d\x86\x8b\x8e\xa2\x6d\xcb\x88\x8e\xa5\xa3\xac\x88\xa3\xac\xa4\x8e\xac\x83\x88\x84\xac\x83\x80\x88\x8b\xa9\x2a\x2e\xcb\xac\xac\x6d\x4D\x80\xa0\x8e\x8b\x84\x8e\x8d\xac\x41\x8e\x8d\x80\xa0\x80\xa2\xa4\x84\xc0")
        death_list.append(
            b"\x2d\x44\xa6\x84\xa2\xa9\xac\xa0\x80\xa2\xa4\x88\x8d\x86\xac\x86\x88\xa6\x84\xa3\xac\x80\xcb\x85\x8e\xa2\x84\xa4\x80\xa3\xa4\x84\xac\x8e\x85\xac\x83\x84\x80\xa4\x87\x2b\xac\x84\xa6\x84\xa2\xa9\xcb\xa2\x84\xa5\x8d\x88\x8e\x8d\xac\x80\xac\x87\x88\x8d\xa4\xac\x8e\x85\xac\xa4\x87\x84\xac\xa2\x84\x6d\xcb\xa3\xa5\xa2\xa2\x84\x82\xa4\x88\x8e\x8d\x2a\x2e\xac\x6d\x63\x82\x87\x8e\xa0\x84\x8d\x87\x80\xa5\x84\xa2\xc0")
        death_list.append(
            b"\x2d\x45\x8e\xa2\xac\x8b\x88\x85\x84\xac\x80\x8d\x83\xac\x83\x84\x80\xa4\x87\xac\x80\xa2\x84\xcb\x8e\x8d\x84\x2b\xac\x84\xa6\x84\x8d\xac\x80\xa3\xac\xa4\x87\x84\xac\xa2\x88\xa6\x84\xa2\xac\x80\x8d\x83\xcb\xa4\x87\x84\xac\xa3\x84\x80\xac\x80\xa2\x84\xac\x8e\x8d\x84\x2a\x2e\xcb\xac\x6d\x4A\x87\x80\x8b\x88\x8b\xac\x46\x88\x81\xa2\x80\x8d\xc0")
        death_list.append(
            b"\x2d\x4B\x88\xa6\x84\xac\xa9\x8e\xa5\xa2\xac\x8b\x88\x85\x84\xac\xa4\x87\x80\xa4\xac\xa4\x87\x84\xcb\x85\x84\x80\xa2\xac\x8e\x85\xac\x83\x84\x80\xa4\x87\xac\x82\x80\x8d\xac\x8d\x84\xa6\x84\xa2\xcb\x84\x8d\xa4\x84\xa2\xac\xa9\x8e\xa5\xa2\xac\x87\x84\x80\xa2\xa4\x2a\x2e\xcb\xac\xac\x6d\x64\x84\x82\xa5\x8c\xa3\x84\x87\xc0")
        death_list.append(
            b"\x2d\x40\x82\x87\x88\x84\xa6\x88\x8d\x86\xac\x8b\x88\x85\x84\xac\x88\xa3\xac\x8d\x8e\xa4\xac\xa4\x87\x84\xcb\x84\xa1\xa5\x88\xa6\x80\x8b\x84\x8d\xa4\xac\x8e\x85\xac\x80\xa6\x8e\x88\x83\x88\x8d\x86\xcb\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x40\xa9\x8d\xac\x62\x80\x8d\x83\xc0")
        death_list.append(
            b"\x2d\x48\x85\xac\xa7\x84\xac\x8c\xa5\xa3\xa4\xac\x83\x88\x84\x2b\xac\xa7\x84\xac\x83\x88\x84\xcb\x83\x84\x85\x84\x8d\x83\x88\x8d\x86\xac\x8e\xa5\xa2\xac\xa2\x88\x86\x87\xa4\xa3\x2a\x2e\xcb\xac\xac\x6d\x63\x88\xa4\xa4\x88\x8d\x86\xac\x41\xa5\x8b\x8b\xc0")
        death_list.append(
            b"\x2d\x64\x87\x84\xac\x82\x8b\x8e\xa3\x84\xa2\xac\xa7\x84\xac\x82\x8e\x8c\x84\xac\xa4\x8e\xac\xa4\x87\x84\xcb\x8d\x84\x86\x80\xa4\x88\xa6\x84\x2b\xac\xa4\x8e\xac\x83\x84\x80\xa4\x87\x2b\xac\xa4\x87\x84\xcb\x8c\x8e\xa2\x84\xac\xa7\x84\xac\x81\x8b\x8e\xa3\xa3\x8e\x8c\x2a\x2e\xcb\xac\xac\x6d\x4C\x8e\x8d\xa4\x86\x8e\x8c\x84\xa2\xa9\xac\x42\x8b\x88\x85\xa4\xc0")
        death_list.append(
            b"\x2d\x48\x85\xac\xa7\x84\xac\x83\x8e\x8d\x0e\xa4\xac\x8a\x8d\x8e\xa7\xac\x8b\x88\x85\x84\x2b\xcb\x87\x8e\xa7\xac\x82\x80\x8d\xac\xa7\x84\xac\x8a\x8d\x8e\xa7\xac\x83\x84\x80\xa4\x87\x0d\x2e\xcb\xac\xac\x6d\x42\x8e\x8d\x85\xa5\x82\x88\xa5\xa3\xc0")
        death_list.append(
            b"\x2d\x48\xac\x83\x8e\x8d\x0e\xa4\xac\x87\x80\xa6\x84\xac\x8d\x8e\xac\x85\x84\x80\xa2\xac\x8e\x85\xcb\x83\x84\x80\xa4\x87\x2a\xac\x4C\xa9\xac\x8e\x8d\x8b\xa9\xac\x85\x84\x80\xa2\xac\x88\xa3\xcb\x82\x8e\x8c\x88\x8d\x86\xac\x81\x80\x82\x8a\xac\xa2\x84\x88\x8d\x82\x80\xa2\x8d\x80\xa4\x84\x83\x2a\x2e\xcb\xac\xac\x6d\x64\xa5\xa0\x80\x82\xac\x63\x87\x80\x8a\xa5\xa2\xc0")
        death_list.append(
            b"\x2d\x4B\x88\x85\x84\xac\x88\xa4\xa3\x84\x8b\x85\xac\x88\xa3\xac\x81\xa5\xa4\xac\xa4\x87\x84\xcb\xa3\x87\x80\x83\x8e\xa7\xac\x8e\x85\xac\x83\x84\x80\xa4\x87\x2b\xac\x80\x8d\x83\xac\xa3\x8e\xa5\x8b\xa3\xcb\x83\x84\xa0\x80\xa2\xa4\x84\x83\xac\x81\xa5\xa4\xac\xa4\x87\x84\xac\xa3\x87\x80\x83\x8e\xa7\xa3\xcb\x8e\x85\xac\xa4\x87\x84\xac\x8b\x88\xa6\x88\x8d\x86\x2a\x2e\xac\x6d\x64\x2a\xac\x41\xa2\x8e\xa7\x8d\x84\xc0")
        death_list.append(
            b"\x2d\x63\x8e\x8c\x84\x8e\x8d\x84\xac\x87\x80\xa3\xac\xa4\x8e\xac\x83\x88\x84\xac\x88\x8d\xcb\x8e\xa2\x83\x84\xa2\xac\xa4\x87\x80\xa4\xac\xa4\x87\x84\xac\xa2\x84\xa3\xa4\xac\x8e\x85\xac\xa5\xa3\xcb\xa3\x87\x8e\xa5\x8b\x83\xac\xa6\x80\x8b\xa5\x84\xac\x8b\x88\x85\x84\xac\x8c\x8e\xa2\x84\x2a\x2e\xcb\xac\xac\x6d\x66\x88\xa2\x86\x88\x8d\x88\x80\xac\x67\x8e\x8e\x8b\x85\xc0")
        death_list.append(
            b"\x2d\x4E\xa5\xa2\xac\x8b\x88\x85\x84\xac\x83\xa2\x84\x80\x8c\xa3\xac\xa4\x87\x84\xcb\x65\xa4\x8e\xa0\x88\x80\x2a\xac\x4E\xa5\xa2\xac\x83\x84\x80\xa4\x87\xac\x80\x82\x87\x88\x84\xa6\x84\xa3\xcb\xa4\x87\x84\xac\x48\x83\x84\x80\x8b\x2a\x2e\xcb\xac\xac\x6d\x66\x88\x82\xa4\x8e\xa2\xac\x47\xa5\x86\x8e\xc0")
        death_list.append(
            b"\x2d\x48\x85\xac\xa9\x8e\xa5\xac\x83\x88\x84\xac\x88\x8d\xac\x80\x8d\xcb\x84\x8b\x84\xa6\x80\xa4\x8e\xa2\x2b\xac\x81\x84\xac\xa3\xa5\xa2\x84\xac\xa4\x8e\xac\xa0\xa5\xa3\x87\xcb\xa4\x87\x84\xac\x65\xa0\xac\x81\xa5\xa4\xa4\x8e\x8d\x2a\x2e\xcb\xac\xac\x6d\x63\x80\x8c\xac\x4B\x84\xa6\x84\x8d\xa3\x8e\x8d\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\xa6\x84\xa2\xa9\xac\x8e\x85\xa4\x84\x8d\xcb\xa2\x84\x85\x84\xa2\xa2\x84\x83\xac\xa4\x8e\xac\x80\xa3\xac\x80\xac\x86\x8e\x8e\x83\xcb\x82\x80\xa2\x84\x84\xa2\xac\x8c\x8e\xa6\x84\x2a\x2e\xcb\xac\xac\x6d\x41\xa5\x83\x83\xa9\xac\x47\x8e\x8b\x8b\xa9\xc0")
        death_list.append(
            b"\x2d\x42\x8e\xa5\xa2\x80\x86\x84\xac\x88\xa3\xac\x81\x84\x88\x8d\x86\xac\xa3\x82\x80\xa2\x84\x83\xcb\xa4\x8e\xac\x83\x84\x80\xa4\x87\x2a\x2a\x2a\xac\x80\x8d\x83\xac\xa3\x80\x83\x83\x8b\x88\x8d\x86\xcb\xa5\xa0\xac\x80\x8d\xa9\xa7\x80\xa9\x2a\x2e\xcb\xac\xac\x6d\x49\x8e\x87\x8d\xac\x67\x80\xa9\x8d\x84\xc0")
        death_list.append(
            b"\x2d\x48\x8d\x80\x82\xa4\x88\xa6\x88\xa4\xa9\xac\x88\xa3\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x41\x84\x8d\x88\xa4\x8e\xac\x4C\xa5\xa3\xa3\x8e\x8b\x88\x8d\x88\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\xa4\x87\x84\xac\x86\x8e\x8b\x83\x84\x8d\xac\x8a\x84\xa9\xcb\xa4\x87\x80\xa4\xac\x8e\xa0\x84\x8d\xa3\xac\xa4\x87\x84\xac\xa0\x80\x8b\x80\x82\x84\xac\x8e\x85\xcb\x84\xa4\x84\xa2\x8d\x88\xa4\xa9\x2a\x2e\xcb\xac\xac\x6d\x49\x8e\x87\x8d\xac\x4C\x88\x8b\xa4\x8e\x8d\xc0")
        death_list.append(
            b"\x2d\x48\xac\x80\x8b\xa7\x80\xa9\xa3\xac\xa3\x80\xa9\x2b\xac\x82\x8e\x8c\xa0\x8b\x80\x82\x84\x8d\x82\xa9\xcb\x88\xa3\xac\xa4\x87\x84\xac\x8a\x88\xa3\xa3\xac\x8e\x85\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x63\x87\x80\xa2\x88\xac\x62\x84\x83\xa3\xa4\x8e\x8d\x84\xc0")
        death_list.append(
            b"\x2d\x48\x8d\xac\xa4\x87\x84\xac\x8b\x8e\x8d\x86\xac\xa2\xa5\x8d\xac\xa7\x84\xac\x80\xa2\x84\xcb\x80\x8b\x8b\xac\x83\x84\x80\x83\x2a\x2e\xcb\xac\xac\x6d\x49\x8e\x87\x8d\xac\x4C\x80\xa9\x8d\x80\xa2\x83\xac\x4A\x84\xa9\x8d\x84\xa3\xc0")
        death_list.append(
            b"\x2d\x48\x0e\x8c\xac\x8d\x8e\xa4\xac\x80\x85\xa2\x80\x88\x83\xac\x8e\x85\xac\x83\x84\x80\xa4\x87\x2b\xcb\x81\xa5\xa4\xac\x48\x0e\x8c\xac\x88\x8d\xac\x8d\x8e\xac\x87\xa5\xa2\xa2\xa9\xac\xa4\x8e\xcb\x83\x88\x84\x2a\xac\x48\xac\x87\x80\xa6\x84\xac\xa3\x8e\xac\x8c\xa5\x82\x87\xac\x48\xac\xa7\x80\x8d\xa4\xcb\xa4\x8e\xac\x83\x8e\xac\x85\x88\xa2\xa3\xa4\x2a\x2e\xac\x6d\x63\x2a\xac\x47\x80\xa7\x8a\x88\x8d\x86\xc0")
        death_list.append(
            b"\x2d\x45\x8e\xa2\xac\xa4\x88\xa3\xac\x8d\x8e\xa4\xac\x88\x8d\xac\x8c\x84\xa2\x84\xac\x83\x84\x80\xa4\x87\xcb\xa4\x87\x80\xa4\xac\x8c\x84\x8d\xac\x83\x88\x84\xac\x8c\x8e\xa3\xa4\x2a\x2e\xcb\xac\xac\x6d\x44\x8b\x88\xaa\x80\x81\x84\xa4\x87\xac\x41\x80\xa2\xa2\x84\xa4\xa4\xcb\xac\xac\xac\xac\xac\x41\xa2\x8e\xa7\x8d\x88\x8d\x86\xc0")
        death_list.append(
            b"\x2d\x43\x8e\xac\x8d\x8e\xa4\xac\x85\x84\x80\xa2\xac\x83\x84\x80\xa4\x87\xac\xa3\x8e\xac\x8c\xa5\x82\x87\xcb\x81\xa5\xa4\xac\xa2\x80\xa4\x87\x84\xa2\xac\xa4\x87\x84\xac\x88\x8d\x80\x83\x84\xa1\xa5\x80\xa4\x84\xcb\x8b\x88\x85\x84\x2a\x2e\xcb\xac\xac\x6d\x41\x84\xa2\xa4\x8e\x8b\xa4\xac\x41\xa2\x84\x82\x87\xa4\xc0")
        death_list.append(
            b"\x2d\x4D\x8e\xa4\x87\x88\x8d\x86\xac\x88\x8d\xac\x8b\x88\x85\x84\xac\x88\xa3\xcb\xa0\xa2\x8e\x8c\x88\xa3\x84\x83\xac\x84\xa8\x82\x84\xa0\xa4\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x4A\x80\x8d\xa9\x84\xac\x67\x84\xa3\xa4\xc0")
        death_list.append(
            b"\x2d\x4C\xa9\xac\x85\x84\x80\xa2\xac\xa7\x80\xa3\xac\x8d\x8e\xa4\xac\x8e\x85\xac\x83\x84\x80\xa4\x87\xcb\x88\xa4\xa3\x84\x8b\x85\x2b\xac\x81\xa5\xa4\xac\x80\xac\x83\x84\x80\xa4\x87\xac\xa7\x88\xa4\x87\x6d\xcb\x8e\xa5\xa4\xac\x8c\x84\x80\x8d\x88\x8d\x86\x2a\x2e\xcb\xac\xac\x6d\x47\xa5\x84\xa9\xac\x4D\x84\xa7\xa4\x8e\x8d\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\x89\xa5\xa3\xa4\xac\x8b\x88\x85\x84\x0e\xa3\xac\x8d\x84\xa8\xa4\xcb\x81\x88\x86\xac\x80\x83\xa6\x84\x8d\xa4\xa5\xa2\x84\x2a\x2e\xcb\xac\xac\x6d\x49\x2a\xac\x4A\x2a\xac\x62\x8e\xa7\x8b\x88\x8d\x86\xc0")
        death_list.append(
            b"\x2d\x41\x84\x82\x80\xa5\xa3\x84\xac\x8e\x85\xac\x88\x8d\x83\x88\x85\x85\x84\xa2\x84\x8d\x82\x84\x2b\xcb\x8e\x8d\x84\xac\x83\x88\x84\xa3\xac\x81\x84\x85\x8e\xa2\x84\xac\x8e\x8d\x84\xcb\x80\x82\xa4\xa5\x80\x8b\x8b\xa9\xac\x83\x88\x84\xa3\x2a\x2e\xcb\xac\xac\x6d\x44\x8b\x88\x84\xac\x67\x88\x84\xa3\x84\x8b\xc0")
        death_list.append(
            b"\x2d\x4C\xa5\xa3\xa4\xac\x8d\x8e\xa4\xac\x80\x8b\x8b\xac\xa4\x87\x88\x8d\x86\xa3\xac\x80\xa4\xcb\xa4\x87\x84\xac\x8b\x80\xa3\xa4\xac\x81\x84\xac\xa3\xa7\x80\x8b\x8b\x8e\xa7\x84\x83\xac\xa5\xa0\xcb\x88\x8d\xac\x83\x84\x80\xa4\x87\x0d\x2e\xcb\xac\xac\x6d\x60\x8b\x80\xa4\x8e\xc0")
        death_list.append(
            b"\x2d\x64\x87\x84\xa2\x84\xac\x88\xa3\xac\x8d\x8e\xac\x83\x84\x80\xa4\x87\x2b\xac\x8e\x8d\x8b\xa9\xcb\x80\xac\x82\x87\x80\x8d\x86\x84\xac\x8e\x85\xac\xa7\x8e\xa2\x8b\x83\xa3\x2a\x2e\xcb\xac\xac\x6d\x42\x87\x88\x84\x85\xac\x63\x84\x80\xa4\xa4\x8b\x84\xc0")
        death_list.append(
            b"\x2d\x48\xac\x87\x80\x83\xac\xa3\x84\x84\x8d\xac\x81\x88\xa2\xa4\x87\xac\x80\x8d\x83\xcb\x83\x84\x80\xa4\x87\xac\x81\xa5\xa4\xac\x87\x80\x83\xac\xa4\x87\x8e\xa5\x86\x87\xa4\xac\xa4\x87\x84\xa9\xcb\xa7\x84\xa2\x84\xac\x83\x88\x85\x85\x84\xa2\x84\x8d\xa4\x2a\x2e\xcb\xac\xac\x6d\x64\x2a\xac\x63\x2a\xac\x44\x8b\x88\x8e\xa4\xc0")
        death_list.append(
            b"\x2d\x42\xa5\xa2\x88\x8e\xa3\x88\xa4\xa9\xac\x88\xa3\xac\x8b\x88\x85\x84\x2a\xcb\x40\xa3\xa3\xa5\x8c\xa0\xa4\x88\x8e\x8d\xac\x88\xa3\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\xac\x6d\x4C\x80\xa2\x8a\xac\x60\x80\xa2\x8a\x84\xa2\xc0")
        death_list.append(
            b"\x2d\x48\xac\x85\x84\x84\x8b\xac\x8c\x8e\x8d\x8e\xa4\x8e\x8d\xa9\xac\x80\x8d\x83\xac\x83\x84\x80\xa4\x87\xcb\xa4\x8e\xac\x81\x84\xac\x80\x8b\x8c\x8e\xa3\xa4\xac\xa4\x87\x84\xac\xa3\x80\x8c\x84\x2a\x2e\xcb\xac\xac\x6d\x42\x87\x80\xa2\x8b\x8e\xa4\xa4\x84\xac\x41\xa2\x8e\x8d\xa4\x84\xc0")
        death_list.append(
            b"\x2d\x63\x8e\x8c\x84\xac\xa0\x84\x8e\xa0\x8b\x84\xac\x80\xa2\x84\xac\xa3\x8e\xac\x80\x85\xa2\x80\x88\x83\xcb\xa4\x8e\xac\x83\x88\x84\xac\xa4\x87\x80\xa4\xac\xa4\x87\x84\xa9\xac\x8d\x84\xa6\x84\xa2\xcb\x81\x84\x86\x88\x8d\xac\xa4\x8e\xac\x8b\x88\xa6\x84\x2a\x2e\xcb\xac\xac\x6d\x47\x84\x8d\xa2\xa9\xac\x66\x80\x8d\xac\x43\xa9\x8a\x84\xc0")
        death_list.append(
            b"\x2d\x64\x87\x84\xac\x81\x8e\x83\xa9\xac\x83\x88\x84\xa3\x2b\xac\x81\xa5\xa4\xac\xa4\x87\x84\xcb\xa3\xa0\x88\xa2\x88\xa4\xac\xa4\x87\x80\xa4\xac\xa4\xa2\x80\x8d\xa3\x82\x84\x8d\x83\xa3\xac\x88\xa4\xcb\x82\x80\x8d\x8d\x8e\xa4\xac\x81\x84\xac\xa4\x8e\xa5\x82\x87\x84\x83\xac\x81\xa9\xcb\x83\x84\x80\xa4\x87\x2a\x2e\xac\xac\x6d\x62\x80\x8c\x80\x8d\x80\xac\x4C\x80\x87\x80\xa2\xa3\x87\x88\xc0")
        death_list.append(
            b"\x2d\x67\x87\x84\xa4\x87\x84\xa2\xac\x85\x8e\xa2\xac\x8b\x88\x85\x84\xac\x8e\xa2\xcb\x83\x84\x80\xa4\x87\x2b\xac\x83\x8e\xac\xa9\x8e\xa5\xa2\xac\x8e\xa7\x8d\xac\xa7\x8e\xa2\x8a\xcb\xa7\x84\x8b\x8b\x2a\x2e\xcb\xac\xac\x6d\x49\x8e\x87\x8d\xac\x62\xa5\xa3\x8a\x88\x8d\xc0")
        death_list.append(
            b"\x2d\x64\x87\x84\xac\xa2\x84\xa0\x8e\xa2\xa4\xa3\xac\x8e\x85\xac\x8c\xa9\xac\x83\x84\x80\xa4\x87\xcb\x87\x80\xa6\x84\xac\x81\x84\x84\x8d\xac\x86\xa2\x84\x80\xa4\x8b\xa9\xcb\x84\xa8\x80\x86\x86\x84\xa2\x80\xa4\x84\x83\x2a\x2e\xcb\xac\xac\x6d\x4C\x80\xa2\x8a\xac\x64\xa7\x80\x88\x8d\xc0")
        death_list.append(
            b"\x2d\x64\x87\x84\xac\xa6\x80\x8b\x88\x80\x8d\xa4\xac\x8d\x84\xa6\x84\xa2\xac\xa4\x80\xa3\xa4\x84\xcb\x8e\x85\xac\x83\x84\x80\xa4\x87\xac\x81\xa5\xa4\xac\x8e\x8d\x82\x84\x2a\x2e\xcb\xac\xac\x6d\x67\x88\x8b\x8b\x88\x80\x8c\xac\x63\x87\x80\x8a\x84\xa3\xa0\x84\x80\xa2\x84\xc0")
        death_list.append(
            b"\x2d\x67\x84\xac\x8a\x8d\x8e\xa7\xac\xa4\x87\x84\xac\xa2\x8e\x80\x83\xac\xa4\x8e\xcb\x85\xa2\x84\x84\x83\x8e\x8c\xac\x87\x80\xa3\xac\x80\x8b\xa7\x80\xa9\xa3\xac\x81\x84\x84\x8d\xcb\xa3\xa4\x80\x8b\x8a\x84\x83\xac\x81\xa9\xac\x83\x84\x80\xa4\x87\x2a\x2e\xcb\xac\x6d\x40\x8d\x86\x84\x8b\x80\xac\x43\x80\xa6\x88\xa3\xc0")
        death_list.append(
            b"\x2d\x43\x84\xa3\xa0\x88\xa3\x84\xac\x8d\x8e\xa4\xac\x83\x84\x80\xa4\x87\x2b\xac\x81\xa5\xa4\xcb\xa7\x84\x8b\x82\x8e\x8c\x84\xac\x88\xa4\x2b\xac\x85\x8e\xa2\xac\x8d\x80\xa4\xa5\xa2\x84\xcb\xa7\x88\x8b\x8b\xa3\xac\x88\xa4\xac\x8b\x88\x8a\x84\xac\x80\x8b\x8b\xac\x84\x8b\xa3\x84\x2a\x2e\xcb\xac\xac\x6d\x4C\x80\xa2\x82\xa5\xa3\xac\x40\xa5\xa2\x84\x8b\x88\xa5\xa3\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\x8d\x8e\xa4\xac\xa4\x87\x84\xac\xa7\x8e\xa2\xa3\xa4\xcb\xa4\x87\x80\xa4\xac\x82\x80\x8d\xac\x87\x80\xa0\xa0\x84\x8d\xac\xa4\x8e\xac\x8c\x84\x8d\x2a\x2e\xcb\xac\xac\x6d\x60\x8b\x80\xa4\x8e\xc0")
        death_list.append(
            b"\x2d\x4B\x88\x85\x84\xac\x8b\x84\xa6\x84\x8b\xa3\xac\x80\x8b\x8b\xac\x8c\x84\x8d\x2a\xcb\x43\x84\x80\xa4\x87\xac\xa2\x84\xa6\x84\x80\x8b\xa3\xac\xa4\x87\x84\xcb\x84\x8c\x88\x8d\x84\x8d\xa4\x2a\x2e\xcb\xac\xac\x6d\x46\x84\x8e\xa2\x86\x84\xac\x41\x84\xa2\x8d\x80\xa2\x83\xac\x63\x87\x80\xa7\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\x88\xa3\xac\xa4\x87\x84\xac\xa7\x88\xa3\x87\xac\x8e\x85\xcb\xa3\x8e\x8c\x84\x2b\xac\xa4\x87\x84\xac\xa2\x84\x8b\x88\x84\x85\xac\x8e\x85\xac\x8c\x80\x8d\xa9\x2b\xcb\x80\x8d\x83\xac\xa4\x87\x84\xac\x84\x8d\x83\xac\x8e\x85\xac\x80\x8b\x8b\x2a\x2e\xcb\xac\xac\x6d\x4B\xa5\x82\x88\xa5\xa3\xac\x40\x8d\x8d\x80\x84\xa5\xa3\xac\x63\x84\x8d\x84\x82\x80\xc0")
        death_list.append(
            b"\x2d\x43\x84\x80\xa4\x87\xac\xa7\x88\x8b\x8b\xac\x81\x84\xac\x80\xac\x86\xa2\x84\x80\xa4\xcb\xa2\x84\x8b\x88\x84\x85\x2a\xac\x4D\x8e\xac\x8c\x8e\xa2\x84\xcb\x88\x8d\xa4\x84\xa2\xa6\x88\x84\xa7\xa3\x2a\x2e\xcb\xac\xac\x6d\x4A\x80\xa4\x87\x80\xa2\x88\x8d\x84\xac\x47\x84\xa0\x81\xa5\xa2\x8d\xc0\xc0")
        if mode == 3:
            death_list.append(b"\x2d\x46\x88\xa4\xac\x86\xa5\x83\xac\xa3\x82\xa2\xa5\x81\x2a\x2e\xcb\xac\xac\x6d\x41\x80\x86\xa5\xc0")

        # Will death text
        self.seek(patch, int("d7c3", 16) + rom_offset)
        self.write(patch, death_list[random.randint(0, len(death_list) - 1)])
        # self.write(patch, death_list[0])

        # Change Fredan and Shadow death pointers
        self.seek(patch, int("d7b2", 16) + rom_offset)
        self.write(patch, b"\xc2\xd7")
        self.seek(patch, int("d7b8", 16) + rom_offset)
        self.write(patch, b"\xc2\xd7")

        ##########################################################################
        #                          Have fun with final text
        ##########################################################################
        superhero_list = []
        superhero_list.append(qt_encode("I must go, my people need me!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("     Up, up, and away!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("       Up and atom!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("  It's clobberin' time!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("       For Asgard!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("    Back in a flash!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("      I am GROOT!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("Wonder Twin powers activate!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("    Titans together!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("       HULK SMASH!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("        Flame on!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("    I have the power!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("        Shazam!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("     Bite me, fanboy.") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("  Hi-yo Silver... away!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("Here I come to save the day!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("    Teen Titans, Go!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("       Cowabunga!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("       SPOOOOON!!") + b"\xc3\x00\xc0")
        superhero_list.append(qt_encode("There better be bacon when I get there...") + b"\xc3\x00\xc0")

        # Assign final text box
        self.seek(patch, int("98ebe", 16) + rom_offset)
        self.write(patch, superhero_list[random.randint(0, len(superhero_list) - 1)])

        ##########################################################################
        #                   Randomize item and ability placement
        ##########################################################################
        done = False
        seed_adj = 0
        self.w = World(settings, statues, kara_location, gem, [inca_x + 1, inca_y + 1], hieroglyph_order)
        while not done:
            if seed_adj > 10:
                self.logger.error("ERROR: Max number of seed adjustments exceeded")
                raise RecursionError
            self.w = World(settings, statues, kara_location, gem, [inca_x + 1, inca_y + 1], hieroglyph_order)
            done = self.w.randomize(seed_adj)
            seed_adj += 1

        self.w.generate_spoiler(VERSION)
        self.w.write_to_rom(patch, rom_offset)

        ##########################################################################
        #                        Randomize Ishtar puzzle
        ##########################################################################
        # Add checks for Will's hair in each room
        self.seek(patch, int("6dc53", 16) + rom_offset)
        self.write(patch, b"\x4c\x00\xdd\x86")
        self.seek(patch, int("6dd00", 16) + rom_offset)
        self.write(patch, b"\x02\x45\x10\x00\x20\x10\x66\xdc\x02\x45\x30\x00\x40\x10\x66\xDC")
        self.write(patch, b"\x02\x45\x50\x00\x60\x10\x66\xdc\x02\x45\x70\x00\x80\x10\x66\xDC")
        self.write(patch, b"\x4c\x66\xdc\x86")

        # Generalize success text boxes
        # Make Rooms 1 and 3 equal to Room 2 text (which is already general)
        self.seek(patch, int("6d978", 16) + rom_offset)  # Room 1
        self.write(patch, b"\x2c\xdb")
        self.seek(patch, int("6d9ce", 16) + rom_offset)  # Room 3
        self.write(patch, b"\x2c\xdb")
        # Generalize Room 4 text
        self.seek(patch, int("6d9f8", 16) + rom_offset)
        self.write(patch, b"\xc6\xdb")
        self.seek(patch, int("6dbc6", 16) + rom_offset)
        self.write(patch, b"\xc2\x0a")

        # Create temporary map file
        f_ishtarmapblank = open(BIN_PATH + "ishtarmapblank.bin", "rb")
        f_ishtarmap = tempfile.TemporaryFile()
        f_ishtarmap.write(f_ishtarmapblank.read())
        f_ishtarmapblank.close()

        room_offsets = ["6d95e", "6d98a", "6d9b4", "6d9de"]  # ROM addrs for cursor capture, by room
        coord_offsets = [3, 8, 15, 20]  # Offsets for xmin, xmax, ymin, ymax
        changes = [random.randint(1, 8), random.randint(1, 7), random.randint(1, 5), random.randint(1, 7)]

        # Set change for Room 1
        if changes[0] == 1:  # Change right vase to light (vanilla)
            f_ishtarmap.seek(int("17b", 16))
            f_ishtarmap.write(b"\x7b")
            f_ishtarmap.seek(int("18b", 16))
            f_ishtarmap.write(b"\x84")
            coords = [b"\xB0\x01", b"\xC0\x01", b"\x70\x00", b"\x90\x00"]

        elif changes[0] == 2:  # Change middle vase to light
            f_ishtarmap.seek(int("175", 16))
            f_ishtarmap.write(b"\x7b")
            f_ishtarmap.seek(int("185", 16))
            f_ishtarmap.write(b"\x84")
            coords = [b"\x50\x01", b"\x60\x01", b"\x70\x00", b"\x90\x00"]

        elif changes[0] == 3:  # Change left vase to dark
            f_ishtarmap.seek(int("174", 16))
            f_ishtarmap.write(b"\x83")
            f_ishtarmap.seek(int("184", 16))
            f_ishtarmap.write(b"\x87")
            coords = [b"\x40\x01", b"\x50\x01", b"\x70\x00", b"\x90\x00"]

        elif changes[0] == 4:  # Change left shelf to empty
            f_ishtarmap.seek(int("165", 16))
            f_ishtarmap.write(b"\x74")
            coords = [b"\x50\x01", b"\x60\x01", b"\x58\x00", b"\x70\x00"]

        elif changes[0] == 5:  # Change left shelf to books
            f_ishtarmap.seek(int("165", 16))
            f_ishtarmap.write(b"\x76")
            coords = [b"\x50\x01", b"\x60\x01", b"\x58\x00", b"\x70\x00"]

        elif changes[0] == 6:  # Change right shelf to jar
            f_ishtarmap.seek(int("166", 16))
            f_ishtarmap.write(b"\x75")
            coords = [b"\x60\x01", b"\x70\x01", b"\x58\x00", b"\x70\x00"]

        elif changes[0] == 7:  # Change right shelf to empty
            f_ishtarmap.seek(int("166", 16))
            f_ishtarmap.write(b"\x74")
            coords = [b"\x60\x01", b"\x70\x01", b"\x58\x00", b"\x70\x00"]

        elif changes[0] == 8:  # Will's hair
            self.seek(patch, int("6dd06", 16) + rom_offset)
            self.write(patch, b"\x5d")
            coords = [b"\xa0\x01", b"\xc0\x01", b"\xb0\x00", b"\xd0\x00"]

        # Update cursor check ranges for Room 1
        for i in range(4):
            self.seek(patch, int(room_offsets[0], 16) + coord_offsets[i] + rom_offset)
            self.write(patch, coords[i])

        # Set change for Room 2
        if changes[1] == 1:  # Change both pots to dark (vanilla)
            f_ishtarmap.seek(int("3a3", 16))
            f_ishtarmap.write(b"\x7c\x7c")
            f_ishtarmap.seek(int("3b3", 16))
            f_ishtarmap.write(b"\x84\x84")
            coords = [b"\x30\x03", b"\x50\x03", b"\xa0\x00", b"\xc0\x00"]

        elif changes[1] == 2:  # Remove rock
            f_ishtarmap.seek(int("3bd", 16))
            f_ishtarmap.write(b"\x73")
            coords = [b"\xd0\x03", b"\xe0\x03", b"\xb0\x00", b"\xc0\x00"]

        elif changes[1] == 3:  # Add round table
            f_ishtarmap.seek(int("395", 16))
            f_ishtarmap.write(b"\x7d\x7e")
            f_ishtarmap.seek(int("3a5", 16))
            f_ishtarmap.write(b"\x85\x86")
            f_ishtarmap.seek(int("3b5", 16))
            f_ishtarmap.write(b"\x8d\x8e")
            coords = [b"\x50\x03", b"\x70\x03", b"\x90\x00", b"\xb0\x00"]

        elif changes[1] == 4:  # Add sconce
            f_ishtarmap.seek(int("357", 16))
            f_ishtarmap.write(b"\x88\x89")
            f_ishtarmap.seek(int("367", 16))
            f_ishtarmap.write(b"\x90\x91")
            coords = [b"\x70\x03", b"\x90\x03", b"\x50\x00", b"\x70\x00"]

        elif changes[1] == 5:  # Add rock
            f_ishtarmap.seek(int("3b2", 16))
            f_ishtarmap.write(b"\x77")
            coords = [b"\x20\x03", b"\x30\x03", b"\xb0\x00", b"\xc0\x00"]

        elif changes[1] == 6:  # Will's hair
            self.seek(patch, int("6dd0e", 16) + rom_offset)
            self.write(patch, b"\x5d")
            coords = [b"\x90\x03", b"\xb0\x03", b"\xa0\x00", b"\xc0\x00"]

        elif changes[1] == 7:  # Put moss on rock
            f_ishtarmap.seek(int("3bd", 16))
            f_ishtarmap.write(b"\x8f")
            coords = [b"\xd0\x03", b"\xe0\x03", b"\xb0\x00", b"\xc0\x00"]

        # Update cursor check ranges for Room 2
        for i in range(4):
            self.seek(patch, int(room_offsets[1], 16) + coord_offsets[i] + rom_offset)
            self.write(patch, coords[i])

        # Set change for Room 3
        # Check for chest contents, only change map if contents are the same
        if self.w.item_locations[80][3] == self.w.item_locations[81][3]:
            if changes[2] == 1:  # Remove rock
                f_ishtarmap.seek(int("5bd", 16))
                f_ishtarmap.write(b"\x73")
                coords = [b"\xd0\x05", b"\xe0\x05", b"\xb0\x00", b"\xc0\x00"]

            elif changes[2] == 2:  # Add rock
                f_ishtarmap.seek(int("5b2", 16))
                f_ishtarmap.write(b"\x77")
                coords = [b"\x20\x05", b"\x30\x05", b"\xb0\x00", b"\xc0\x00"]

            elif changes[2] == 3:  # Add sconce
                f_ishtarmap.seek(int("557", 16))
                f_ishtarmap.write(b"\x88\x89")
                f_ishtarmap.seek(int("567", 16))
                f_ishtarmap.write(b"\x90\x91")
                coords = [b"\x70\x05", b"\x90\x05", b"\x50\x00", b"\x70\x00"]

            elif changes[2] == 4:  # Will's hair
                self.seek(patch, int("6dd16", 16) + rom_offset)
                self.write(patch, b"\x5d")
                coords = [b"\x90\x05", b"\xb0\x05", b"\xa0\x00", b"\xc0\x00"]

            if changes[2] == 5:  # Moss rock
                f_ishtarmap.seek(int("5bd", 16))
                f_ishtarmap.write(b"\x8f")
                coords = [b"\xd0\x05", b"\xe0\x05", b"\xb0\x00", b"\xc0\x00"]

            # Update cursor check ranges for Room 3 (only if chest contents different)
            for i in range(4):
                self.seek(patch, int(room_offsets[2], 16) + coord_offsets[i] + rom_offset)
                self.write(patch, coords[i])

        # Set change for Room 4
        if changes[3] == 1:  # Will's hair (vanilla)
            self.seek(patch, int("6dd1e", 16) + rom_offset)
            self.write(patch, b"\x5d")

        else:
            if changes[3] == 2:  # Remove rock
                f_ishtarmap.seek(int("7bd", 16))
                f_ishtarmap.write(b"\x73")
                coords = [b"\xd0\x07", b"\xe0\x07", b"\xb0\x00", b"\xc0\x00"]

            elif changes[3] == 3:  # Add rock
                f_ishtarmap.seek(int("7b2", 16))
                f_ishtarmap.write(b"\x77")
                coords = [b"\x20\x07", b"\x30\x07", b"\xb0\x00", b"\xc0\x00"]

            elif changes[3] == 4:  # Add vase L
                f_ishtarmap.seek(int("7a3", 16))
                f_ishtarmap.write(b"\x7c")
                f_ishtarmap.seek(int("7b3", 16))
                f_ishtarmap.write(b"\x84")
                coords = [b"\x30\x07", b"\x40\x07", b"\xa0\x00", b"\xc0\x00"]

            elif changes[3] == 5:  # Add vase R
                f_ishtarmap.seek(int("7ac", 16))
                f_ishtarmap.write(b"\x7c")
                f_ishtarmap.seek(int("7bc", 16))
                f_ishtarmap.write(b"\x84")
                coords = [b"\xc0\x07", b"\xd0\x07", b"\xa0\x00", b"\xc0\x00"]

            elif changes[3] == 6:  # Crease in floor
                f_ishtarmap.seek(int("7b4", 16))
                f_ishtarmap.write(b"\x69\x6a")
                coords = [b"\x40\x07", b"\x60\x07", b"\xb0\x00", b"\xc8\x00"]

            if changes[3] == 7:  # Moss rock
                f_ishtarmap.seek(int("7bd", 16))
                f_ishtarmap.write(b"\x8f")
                coords = [b"\xd0\x07", b"\xe0\x07", b"\xb0\x00", b"\xc0\x00"]

            # Update cursor check ranges for Room 3 (only if not hair)
            for i in range(4):
                self.seek(patch, int(room_offsets[3], 16) + coord_offsets[i] + rom_offset)
                self.write(patch, coords[i])

        # Compress map data and write to file
        f_ishtarmapcomp = tempfile.TemporaryFile()
        f_ishtarmap.seek(0)
        f_ishtarmapcomp.write(qt_compress(f_ishtarmap.read()))
        f_ishtarmapcomp.seek(0)
        f_ishtarmap.close()

        # Insert new compressed map data
        # self.seek(patch, int("193d25",16)+rom_offset)
        self.seek(patch, int("1f4100", 16) + rom_offset)
        self.write(patch, b"\x08\x02")
        self.write(patch, f_ishtarmapcomp.read())
        f_ishtarmapcomp.close()

        # Direct map arrangement pointer to new data - NO LONGER NECESSARY
        # self.seek(patch, int("d977e",16)+rom_offset)
        # self.write(patch, b"\x00\x41")

        return json.dumps(patch.data)

    def generate_spoiler(self) -> str:
        return json.dumps(self.w.spoiler)

    def seek(self, patch, s: int) -> None:
        patch.seek(s)

    def write(self, patch, s):
        patch.write(s)

    def find(self, patch, d, start=None, end=None):
        return patch.find(d, start, end)

    def __get_required_statues__(self, settings: RandomizerData) -> int:
        if settings.goal.value == Goal.RED_JEWEL_HUNT.value:
            return 0

        if settings.statues.lower() == "random":
            return random.randrange(0, 6)

        return int(settings.statues)

    def __generate_patch__(self):
        data = copy.deepcopy(self.original_rom_data)

        return Patch(data, self.logger)

    def __get_offset__(self, patch):
        header = b"\x49\x4C\x4C\x55\x53\x49\x4F\x4E\x20\x4F\x46\x20\x47\x41\x49\x41\x20\x55\x53\x41"

        self.seek(patch,  0)
        h_addr = self.find(patch, header)
        if h_addr < 0:
            raise OffsetError

        return h_addr - int("ffc0", 16)

