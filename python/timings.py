import time
import math

''' Example: 4/4 - 1 chords per bar'''

def get_frequency(bpm: int) -> float:
    return (1 / (bpm / 60))


def main():
    bpm: int = int(input('BPM: '))
    note_length: int = int(input('Duration: '))

    frequency = get_frequency(bpm)

    if note_length == 0 or math.pow(2,note_length) % note_length != 0:
        raise ValueError("Note length must be a valid note duration")

    wait_time = frequency * note_length

    print(f'{frequency}: {wait_time}')

    fb = True
    # while 1:
    #     if fb is True:
    #         print("True")
    #         fb = False
    #     else:
    #         print("False")
    #         fb = True
    #     time.sleep(freq)


def sleepTime():
    pass


if __name__ == "__main__":
    main()
