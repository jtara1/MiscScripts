import keyboard
import time

def main():
    time.sleep(1.5)
    while not keyboard.is_pressed('ctrl+c'):
        time.sleep(1)
        # keyboard.press_and_release('w')
        
        keyboard.press('w')
        time.sleep(0.1)
        keyboard.release('w')
        
        time.sleep(1)
        
        keyboard.press('s')
        time.sleep(0.1)
        keyboard.release('s')
        
        time.sleep(1)
        # keyboard.press_and_release('s')
    
main()