# yasuhati

starlight.py for main game

device.py for audio

pitch.py for audio pitch

v0 - v0.2.1

omitted

v0.3

added button event, press p for generating object

added hidden object (obstacle) for next update

v1.0

added 2 scoring system: distance and food

added object collision

added sensehat related gameplay

    when you shout softly, main character will become red(i.e., moving)

    when you shout loudly, main character will become yellow(i.e., jumping)

    when no sound, main character will become white(i.e., resting)

press P to release hadouken (only when resting)

Installation guide option 1 (anaconda3):

1. create environment

conda create -n yasuhati python=3.11

2. install aubio for python

conda config --add channels conda-forge

conda install -c conda-forge aubio

3. install required packages

pip install pyaudio

pip install pygame

Installation option 2 (anaconda3):

1. conda env create -f environment.yml