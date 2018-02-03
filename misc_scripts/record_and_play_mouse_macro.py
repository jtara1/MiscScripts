import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))

from pprint import pformat
import mouse
import keyboard
from misc_scripts.image_template_matching import get_matches_from_screen
from time import sleep

# globals
stop = False
STOP_BUTTON = 'F2'  # constant


def toggle_stop():
    global stop
    stop = not stop
    print('stop = {}'.format(stop))


# stop hotkey
keyboard.hook_key('F2', keydown_callback=toggle_stop)


def record_mouse_events():
    sleep(1.5)
    stop_record = 'right'
    print('Mouse recording has begun')
    print('Press {} mouse button to stop mouse recording'
          .format(stop_record))

    events = mouse.record(button=stop_record)
    print('Recorded:\n{}'.format(pformat(events)))
    return events


def get_number_of_iterations():
    question = 'Enter number of times to loop playback of recorded events: '
    try:
        response = input(question)
    except NameError:  # py 2 support
        response = raw_input(question)
    response = response.strip()
    return 0 if '' == response else int(response)


def play_mouse_events(events):
    iterations = get_number_of_iterations()
    for i in range(iterations):
        if stop:
            break
        mouse.play(events, speed_factor=1.0)
    return events


def click_template_image(template_image):
    try:
        region = get_matches_from_screen(template_image)[0]
    except IndexError:
        return False

    x = (region[0] + region[2]) / 2
    y = (region[1] + region[3]) / 2
    mouse.move(x, y, absolute=True, duration=0.5)
    sleep(0.5)
    mouse.click(button='left')
    return True


def click_template_image_then_playback_events(
        template_image='btn.png', iterations=1):

    click_template_image(template_image)
    events = record_mouse_events()
    iterations = get_number_of_iterations()

    for i in range(iterations):
        if stop:
            print('stop signal received, ending program')
            break

        print('{} Playing back: template click then events'.format(i))
        click_template_image(template_image)
        mouse.play(events, speed_factor=4.0)
        sleep(0.5)


if __name__ == '__main__':
    # record then play mouse events
    play_mouse_events(record_mouse_events())
    # click_template_image_then_playback_events(
    #     template_image=
    #     'C:\\Users\\James\\Documents\\_Github-Projects\\misc_scripts\\misc_scripts\\btn.png')
