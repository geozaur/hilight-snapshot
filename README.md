# hilight-snapshot
Utility tool for live streamers.

It lets you place markers with the current recording time, so it would be easier later if you want to make a stream highlights video

## Requirements
It requires pynput, if you don't have it, type in:
```
  pip install pynput
```

## How it works
When you open the program you have to
- set the directory where the log will be saved
- set the filename of the log
- set the trigger command which logs the current time (it can be either a single key press or multiple keys pressed together)

After that, press start and whenever you will press the trigger combination, it will log the current time.
