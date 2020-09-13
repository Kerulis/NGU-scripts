"""Helper functions."""
from classes.window import Window
from classes.inputs import Inputs
from classes.features import Inventory, MoneyPit, Adventure, Yggdrasil, GoldDiggers, Questing
from classes.com import Com

import coordinates as coords


class Helper:
    @staticmethod
    def init() -> None:
        Window.init()
        Com.init()
        Com.hook()

    @staticmethod
    def requirements() -> None:
        """Set everything to the proper requirements to run the script.
        It's strongly recommended to run this straight after init()."""
        Inputs.click(*coords.GAME_SETTINGS)
        Inputs.click(*coords.TO_SCIENTIFIC)
        Inputs.click(*coords.CHECK_FOR_UPDATE_OFF)
        Inputs.click(*coords.FANCY_TITAN_HP_BAR_OFF)
        Inputs.click(*coords.DISABLE_HIGHSCORE)
        Inputs.click(*coords.SETTINGS_PAGE_2)
        Inputs.click(*coords.SIMPLE_INVENTORY_SHORTCUT_ON)

    @staticmethod
    def loop(idle_majors: bool = False) -> None:
        """Run infinite loop to prevent idling after task is complete.
        
        Keyword arguments
        idle_majors -- Set to True if you wish to idle major and minor quests.
                       Set to False if you wish to idle minor quests only.
                       Currently active quest will be idled regardless.
        """
        Questing.set_use_majors(idle_majors)
        print("Engaging idle loop")
        while True:  # main loop
            Questing.questing(subcontract=True)  # Questing first, as we are already there
            MoneyPit.pit()
            MoneyPit.spin()
            Inventory.boost_cube()
            GoldDiggers.gold_diggers()
            Yggdrasil.ygg()
            Adventure.itopod_snipe(300)

    @staticmethod
    def human_format(num: float) -> str:
        """Convert large numbers into something readable."""
        suffixes = ['', 'K', 'M', 'B', 'T', 'Q', 'Qi', 'Sx', 'Sp']
        num = float('{:.3g}'.format(num))
        if num > 1e24:
            return '{:.3g}'.format(num)
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), suffixes[magnitude])
