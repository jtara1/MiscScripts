import keyboard
import time
import mouse
import threading
import click


class Action(threading.Thread):
    def __init__(self, hotkey):
        """
        Interface for an action
        """
        self.hotkey = hotkey
        self.enabled = False
        self.terminate = False
        self.action_delay = 0.5  # delay after action has been done

        self.thread = threading.Thread(target=self._run_repeatedly)
        self.start()
        self._stop_event = threading.Event()
        
        self.create_hotkey()

    def create_hotkey(self):
        keyboard.add_hotkey(
            hotkey=self.hotkey,
            callback=self.toggle_enabled)

    def start(self):
        """Start the thread which should start the loop which
        should be ready to repeatedly do some action
        """
        self.thread.start()

    def _run_repeatedly(self):
        """Does the action over and over again
        until it's disabled
        """
        while not self.terminate:
            while self.enabled:
                # need to implement this in child class
                self.do_action()  
                time.sleep(self.action_delay)
            time.sleep(1)

    def do_action(self):
        raise Exception("Not implemented yet")
    
    def toggle_enabled(self):
        self.enabled = not self.enabled
        print("{} {}".format(self.__class__.__name__, str(self.enabled)))

    def stop(self):
        """Stop the thread. We're no longer doing any action
        with any hotkeys created
        """
        self._stop_event.set()
        

class Pickup(Action):
    def __init__(self, hotkey='F2'):
        """
        Presses f repeatedly which picks up loot
        in a certain online game
        """
        super(Pickup, self).__init__(hotkey=hotkey)
        
    def do_action(self):
        keyboard.press_and_release('f')


class Digger(Action):
    def __init__(self, hotkey='F3'):
        """
        Digs dirt in a certain online game
        """
        super(Digger, self).__init__(hotkey=hotkey)

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
        super(Walker, self).__init__(hotkey=hotkey)

    def do_action(self):
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
    

@click.command()
@click.option('-p', '--pickup', is_flag=True, default=True,
              help='Disables pickup macro')
@click.option('-d', '--digger', is_flag=True, default=True,
              help='Disables digger macro')
@click.option('-w', '--walker', is_flag=True, default=True,
              help='Disables walker macro')
def main(pickup, digger, walker):

    def stop_all():
        for macro in macros:
            macro.stop()
    
    macros = []
    if pickup:
        macros.append(Pickup())
    if digger:
        # if digger enabled, it's best if pickup is also enabled
        macros.append(Digger())
    if walker:
        macros.append(Walker())

    # block until program exit (KeyBoardInterrupt) ctrl+c
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop_all()
            exit(0)


if __name__ == "__main__":
    # start the program
    main()

