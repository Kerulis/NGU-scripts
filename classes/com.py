import struct

class Com:
    """Com communicates with pipe server"""
    """eg. dll injected into the game process"""

    pipe = None

    @staticmethod
    def init() -> None:
        """Same as reconnect"""
        return Com.reconnect()

    @staticmethod
    def reconnect() -> None:
        """Recoonects with the communication pipe"""
        if Com.pipe is not None:
            Com.pipe.close()
            Com.pipe = None

        try:
            Com.pipe = open('\\\\.\\pipe\\ngu_cmd', 'wb', buffering=0)
        except FileNotFoundError as err:
            print('Are you sure you ran injector?')
            raise err

    @staticmethod
    def sync() -> None:
        """Wait for pipe server to complete last command"""
        Com.pipe.write(struct.pack('<b', 0xc))
    
    @staticmethod
    def set_cur_pos(x: int, y: int) -> None:
        """Fake position returned by user32.GetCursorPos"""
        """hook_get_cur_pos needed"""
        Com.pipe.write(struct.pack('<bhh', 0x0, x, y))
        Com.sync()
    
    @staticmethod
    def restore_cur() -> None:
        """Restore user32.GetCursorPos to its original state"""
        Com.pipe.write(struct.pack('<b', 0x1))
        Com.sync()
    
    @staticmethod
    def shortcut(keycode: int) -> None:
        """Fake keycode returned by Unity.GetKeyDownInt"""
        """hook_get_key_down needed"""
        Com.pipe.write(struct.pack('<bi', 0x2, keycode))
        Com.sync()
    
    @staticmethod
    def restore_shortcut() -> None:
        """Restore Unity.GetKeyDownInt to its original state"""
        Com.pipe.write(struct.pack('<b', 0x3))
        Com.sync()

    @staticmethod
    def special(keycode: int) -> None:
        """Fake keycode returned by Unity.GetKeyString"""
        """hook_get_key needed"""
        Com.pipe.write(struct.pack('<bb', 0x4, keycode))
        Com.sync()
    
    @staticmethod
    def restore_special() -> None:
        """Restore Unity.GetKeyString to its original state"""
        Com.pipe.write(struct.pack('<b', 0x5))
        Com.sync()

    @staticmethod
    def unhook() -> None:
        """Disable all hooks"""
        Com.pipe.write(struct.pack('<b', 0x6))
        Com.sync()

    @staticmethod
    def eject() -> None:
        """Close pipe server"""
        """Make sure that each hook is disabled"""
        Com.pipe.write(struct.pack('<b', 0x7))
        
    @staticmethod
    def hook_focus() -> None:
        """Hooks Unity.EventSystems.EventSystem.OnApplicationFocus."""
        """To take effect window must be focused and ufocused after"""
        """hook is created. This hook is necessary for script when game"""
        """is out of focus"""
        Com.pipe.write(struct.pack('<b', 0x8))
        Com.sync()

    @staticmethod
    def hook_get_cur_pos() -> None:
        """Hook user32.GetCursorPos"""
        Com.pipe.write(struct.pack('<b', 0x9))
        Com.sync()

    @staticmethod
    def hook_get_key_down() -> None:
        """Hook Unity.Input.GetKeyDownInt"""
        Com.pipe.write(struct.pack('<b', 0xa))
        Com.sync()

    @staticmethod
    def hook_get_key() -> None:
        """Hook Unity.Input.GetKeyString"""
        Com.pipe.write(struct.pack('<b', 0xb))
        Com.sync()

    @staticmethod
    def hook() -> None:
        """Enable all hooks"""
        Com.hook_focus()
        Com.hook_get_cur_pos()
        Com.hook_get_key_down()
        Com.hook_get_key()
