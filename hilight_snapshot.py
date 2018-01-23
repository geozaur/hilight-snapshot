import os
import json

from pynput.keyboard import Key, Listener, Controller

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog

from threading import Thread
from time import time

state = {
    'started': False,
    'start_time': time(),
    'save_dir': os.path.dirname(os.path.realpath(__file__)),
    'save_name': 'snapshot',
    'trigger': {Key.ctrl_l},
    'recording': False
}


def set_listener_thread(listener):
    state['listener'] = listener


def on_window_close():
    print('closing the program')
    try:
        state['listener'].stop()
    except Exception as err:
        pass
    root.destroy()


def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)


def format_trigger(trigger):
    str = ''
    for key in trigger:
        try:
            str += key.char + ' '
        except:
            for special_key in [a for a in dir(Key) if not a.startswith('__')]:
                if key is Key[special_key]:
                    str += special_key + ' '
                    break
    return str[:-1]


def capture_keys():
    current = set()

    def on_press(key):
        if key in state['trigger']:
            current.add(key)

        if all(k in current for k in state['trigger']):
            try:
                elapsed = time() - state['start_time']
                message['text'] = 'Last snapshot at {0}'.format(
                    format_time(elapsed))
                state['current_file'].write('{0}\n'.format(
                    format_time(elapsed)))
            except:
                pass

    def on_release(key):
        try:
            current.remove(key)
        except KeyError:
            pass

    with Listener(on_press=on_press, on_release=on_release) as listener:
        state['listener'] = listener
        listener.join()


def on_start():
    if not state['started']:
        print('App state started')

        save_dir_btn['state'] = DISABLED
        save_name_btn['state'] = DISABLED
        trigger_btn['state'] = DISABLED

        state['start_time'] = time()
        state['started'] = True
        start_btn['text'] = 'Stop'

        state['current_file'] = open(
            state['save_dir'] + '/' + state['save_name'] + '.txt', 'w')

        thread1 = Thread(target=capture_keys)
        thread1.start()
    else:
        print('App state finished')

        save_dir_btn['state'] = NORMAL
        save_name_btn['state'] = NORMAL
        trigger_btn['state'] = NORMAL

        state['started'] = False
        start_btn['text'] = 'Start'
        state['listener'].stop()

        state['current_file'].close()


def record_keys():
    current = set()
    state['trigger'] = set()

    def on_press(key):
        try:
            current.add(key)
            state['trigger'].add(key)
        except:
            pass

    def on_release(key):
        try:
            current.remove(key)
            if not current:
                state['recorder'].stop()
                print('trigger now is {0}'.format(state['trigger']))
                state['recording'] = False
                trigger_btn['text'] = 'Record'
                trigger_label['text'] = format_trigger(state['trigger'])
        except KeyError:
            pass

    with Listener(on_press=on_press, on_release=on_release) as listener:
        state['recorder'] = listener
        listener.join()


def on_record():
    if not state['recording']:
        state['recording'] = True
        trigger_btn['text'] = 'Recording'
        thread1 = Thread(target=record_keys)
        thread1.start()


def change_save_dir():
    dir = filedialog.askdirectory()
    if dir:
        try:
            print(dir)
            state['save_dir'] = dir
            save_dir_label['text'] = dir
        except:
            pass


def change_save_name():
    answer = simpledialog.askstring("Change save name", "Please input the new save name",
                                    parent=root)
    state['save_name'] = answer
    save_name_label['text'] = answer


# GUI
root = Tk()
root.title('Hilight Snapshot')
# root.geometry('300x300')

# message area
message = Label(root, text='Welcome to Hilight Snapshot!')
message.grid(row=0, column=0, columnspan=3)

# save location
Label(root, text='Save directory').grid(row=1, column=0, sticky='W')
save_dir_label = Label(root, text=state['save_dir'])
save_dir_label.grid(row=1, column=1, sticky='W')
save_dir_btn = Button(root, text='Browse', command=change_save_dir)
save_dir_btn.grid(row=1, column=2, sticky='W')

# save name
Label(root, text='Save name').grid(row=2, column=0, sticky='W')
save_name_label = Label(root, text=state['save_name'])
save_name_label.grid(row=2, column=1, sticky='W')
save_name_btn = Button(root, text='Change', command=change_save_name)
save_name_btn.grid(row=2, column=2, sticky='W')

# record trigger
Label(root, text='Trigger').grid(row=3, column=0, sticky='W')
trigger_label = Label(root, text=format_trigger(state['trigger']))
trigger_label.grid(row=3, column=1, sticky='W')
trigger_btn = Button(root, text='Record', command=on_record)
trigger_btn.grid(row=3, column=2, sticky='W')

# start snapshot
start_btn = Button(root, text='Start', command=on_start)
start_btn.grid(row=4, column=0, columnspan=3)

# window close
root.protocol('WM_DELETE_WINDOW', on_window_close)


mainloop()
