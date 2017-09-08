import keyboard
import time
import mouse
import threading


class Action:
    def __init__(self):
        """
        Interface for can action
        """
        self.enabled = False
        self.terminate = False
        self.delay_between_picksups = 0.5

        self.thread = threading.Thread(target=self.start)
        self.thread.start()

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
        print('toggle enabled')
        self.enabled = not self.enabled
        

class Pickup(Action):
    def __init__(self):
        """
        Presses f repeatedly which picks up loot
        in a certain online game
        """
        super().__init__()
        
    def do_action(self):
        keyboard.press_and_release('f')


class Digger(Action):
    def __init__(self):
        """
        Digs dirt in a certain online game
        """
        super().__init__()

    def do_action(self):
        mouse.press(button='right')
        time.sleep(0.1)
        mouse.move(-700, 0, absolute=False, duration=0.1)
        mouse.release(button='right')
        time.sleep(3)  # approx time to dig in game


class Runner:
    def __init__(self):
        self.pickup = Pickup()
        self.digger = Digger()
        self.start()
        
    def start(self):
        keyboard.add_hotkey(hotkey='F2',
                            callback=self.pickup.toggle_enabled)
        keyboard.add_hotkey(hotkey='F3',
                            callback=self.digger.toggle_enabled)
    

if __name__ == "__main__":
    # start the program
    Runner()
