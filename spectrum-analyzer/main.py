""" Project to create an audio visualizer using Python and the STFT
    Author: Zander Blasingame """

import locale
import sys
import threading
import time

import audio
import Visualizer

# default setting for utf-8
locale.setlocale(locale.LC_ALL, '')

# Get command line arguments
use_log_scale = False

if len(sys.argv) > 1:
    if sys.argv[1] == 'log':
        use_log_scale = True


###############################################################################
#
# Functions
#
###############################################################################
# Handles input
def input_handler(vis, audio_proc):
    char = vis.get_ch()
    if char == -1:
        return

    char = chr(char)

    switcher = {
        'q': {'func': exit,
              'params': {'vis': vis, 'audio_proc': audio_proc}},
        'i': {'func': lambda au: au.set_mode('linear'),
              'params': {'au': audio_proc}},
        'l': {'func': lambda au: au.set_mode('log'),
              'params': {'au': audio_proc}},
        'o': {'func': lambda au: au.set_mode('octave'),
              'params': {'au': audio_proc}},

    }

    if char in list(switcher.keys()):
        entry = switcher[char]
        entry['func'](**entry['params'])


# exit function
def exit(vis, audio_proc):
    audio_proc.halt()
    vis.shut_down()
    sys.exit()


###############################################################################
#
# Main Method
#
###############################################################################
def main():
    # Audio processing class
    audio_proc = audio.Audio()

    # Visualizer
    vis = Visualizer.Visualizer()

    # Create and start audio thread
    audio_thread = threading.Thread(target=audio_proc.record_monitor)

    audio_thread.start()

    while True:
        # listen for input keys
        input_handler(vis, audio_proc)

        # render
        vis.render(audio_proc.get_stft)

        time.sleep(0.025)

if __name__ == '__main__':
    main()
