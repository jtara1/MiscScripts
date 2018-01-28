import sys
import mouse


def run():
    start_stop_record = 'F2'
    print('Press {} to start or stop mouse recording'
          .format(start_stop_record))

    events = mouse.record(button=start_stop_record,)
    print('Recorded:\n{}'.format(events))
    question = 'Press [enter] to continue playing the recorded macro '
    try:
        response = input(question)
    except NameError:  # py 2 support
        response = raw_input(question)
    response = response.strip()
    if response == '':
        for i in range(2):
            mouse.play(events, speed_factor=1.0)


if __name__ == '__main__':
    run()
