
# AudioPrioritizer

This script allows you to prioritize programs and mute non-priority programs. 

For instance, if you are listening to music in your browser and receive a voice message in Telegram, you would need to manually turn off the music, turn on the voice message, and then turn the music back on. However, with this script's convenient interface, everything can be done for you automatically.

## Install

Install Python 3.10+:

```bash
https://www.python.org/downloads/
```

Download .pyw from repository and run it (just double click).

`libraries will be installed only at first launch`
## How to use

1) Turn on music in the programs for which you want to set priorities.

2) In the script interface, set the priorities according to the screenshot below.
<p align="center">
  <img src="https://github.com/mat-shur/audio-prioritizer/blob/main/Screenshots/introduction.png?raw=true" alt="howto"/>
</p>

3) Adjust the program muting level with the slider (to what level to mute non-priority programs).

4) Close the script interface by clicking on the X (it will minimize to the system tray).

- to restore the interface, left-click on the icon in the system tray
- to close the script, right-click on the icon in the system tray and select "quit"
- processes that are not present in the system process list for more than 5 minutes and do not have assigned priorities are automatically removed from the list
- if multiple priority programs are selected, the more prioritized one will always mute the less prioritized ones

## Screenshot
<p align="center">
  <img src="https://github.com/mat-shur/audio-prioritizer/blob/main/Screenshots/example.jpg?raw=true" alt="example"/>
</p>

## Technologies

- Python 3x
- PyQt5
- Singletons
- pycaw (Python Core Audio Windows Library)

## To Do
- Saving priorities on restart
- Restore sound levels when programs are closed, if certain processes were muted
- ~~Removing unnecessary individual programs from the list~~ 
- ~~Updating slider styles in the list~~ 
- ~~Fixing the program logic halt during sleep mode~~ 
