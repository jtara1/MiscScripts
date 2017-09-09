import keyboard
import time
import mouse
import threading


class Action:
    def __init__(self, hotkey):
        """
        Interface for an action
        """
        self.hotkey = hotkey
        self.enabled = False
        self.terminate = False
        self.delay_between_picksups = 0.5

        self.thread = threading.Thread(target=self.start)
        self.thread.start()
        self.create_hotkey()
		
    def create_hotkey(self):
        keyboard.add_hotkey(
            hotkey=self.hotkey,
            callback=self.toggle_enabled)
                            
    def start(self):
        self._run_repeatedly()

    def _run(self):
        """Does the action once"""
        do_action()

    def _run_repeatedly(self):
        """Does the action over and over again
        until it's disabled
        """
        while not self.terminate:
            while self.enabled:
                # need to implement this in child class
                self.do_action()  
                time.sleep(self.delay_between_picksups)
            time.sleep(1)

    def do_action(self):
        raise Exception("Not implemented yet")
    
    def toggle_enabled(self):
        self.enabled = not self.enabled
        print(__class__.__name__ + str(self.enabled))
        

class Pickup(Action):
    def __init__(self, hotkey='F2'):
        """
        Presses f repeatedly which picks up loot
        in a certain online game
        """
        super().__init__(hotkey=hotkey)
        
    def do_action(self):
        keyboard.press_and_release('f')


class Digger(Action):
    def __init__(self, hotkey='F3'):
        """
        Digs dirt in a certain online game
        """
        super().__init__(hotkey=hotkey)

    def do_action(self):
        mouse.press(button='right')
        time.sleep(0.1)
        mouse.move(-700, 0, absolute=False, duration=0.1)
        mouse.release(button='right')
        time.sleep(3)  # approx time to dig in game


class Walker(Action):
    def __init__(self, hotkey='F4'):
        """
        Walks forward until disabled
        """
        super().__init__(hotkey=hotkey)

    def do_action(self):
        print('do_action')
        if self.enabled:
            keyboard.press('w')
        else:
            keyboard.release('w')

    def _run_repeatedly(self):
        """Don't need to do this for this macro"""
        pass

    def toggle_enabled(self):
        super().toggle_enabled()
        self.do_action()
    

if __name__ == "__main__":
    # start the program
    Pickup()
    Digger()
    Walker()
    # block until program exit (KeyBoardInterrupt) ctrl+c
    while True:
        time.sleep(10)
