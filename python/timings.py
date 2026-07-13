import time

''' Example: 4/4 - 1 chords per bar'''


def main():
    bpm: int = int(input('BPM: '))
    beats: int = int(input('Beats'))
    note_length: int = int(input('Duration'))
    # chords_per_bar
    # music_time = f'{beats}/{duration}'
    freq = (1 / (bpm / 60)) * beats

    fb = True
    while 1:
        if fb is True:
            print("True")
            fb = False
        else:
            print("False")
            fb = True
        time.sleep(freq)


def sleepTime():
    pass


if __name__ == "__main__":
    main()
