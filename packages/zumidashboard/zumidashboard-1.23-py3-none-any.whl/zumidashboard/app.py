from flask import Flask
from flask_socketio import SocketIO
import time, subprocess
from zumi.zumi import Zumi
from zumi.util.screen import Screen
import zumidashboard.scripts as scripts
import zumidashboard.sounds as sound
import zumidashboard.updater as updater
import os

app = Flask(__name__, static_url_path="", static_folder='dashboard')
app.zumi = Zumi()
app.screen = Screen(clear=False)
app.ssid = ''
socketio = SocketIO(app)


def _awake():
    app.screen.hello()
    sound.wake_up_sound(app.zumi)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# first page render (select wifi page)
@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')


@app.route('/select-network')
def select_network():
    return app.send_static_file('index.html')


@socketio.on('ssid_list')
def ssid_list(sid):
    print('getting ssid list')
    _list = scripts.get_ssid_list()
    socketio.emit('ssid_list',str(_list))


# connect wifi functions
@socketio.on('connect_wifi')
def connect_wifi(ssid, passwd):
    print('app.py : connecting wifi start')
    print(ssid)
    scripts.add_wifi(ssid, passwd)
    print("personality start")
    app.screen.draw_image_by_name("tryingtoconnect")
    sound.try_calibrate_sound(app.zumi)
    sound.try_calibrate_sound(app.zumi)
    print("personality done")
    print('app.py : connecting wifi end')


@socketio.on('check_internet')
def check_internet():

    connected, ssid = scripts.check_wifi()
    app.ssid = ssid
    connected_to_internet = scripts.check_internet()
    if connected and "zumidashboard" in connected_to_internet:
        socketio.emit('check_internet', connected_to_internet)
    else:
        app.screen.draw_text_center("Failed to connect.\n Try again.")
        socketio.emit('check_internet', '')


@socketio.on('zumi_success')
def zumi_success():
    app.screen.draw_text_center("I'm connected to \"" + app.ssid + "\"")
    sound.calibrated_sound(app.zumi)
    time.sleep(2)
    _awake()


@socketio.on('zumi_fail')
def zumi_success():
    app.screen.draw_text_center("Failed to connect.\n Try again.")


# zumi run demo and lesson event link is in frontend already
@socketio.on('activate_offline_mode')
def activate_offline_mode():
    app.screen.draw_text_center("Starting offline mode")
    time.sleep(3)
    _awake()


@socketio.on('run_demos')
def run_demos():
    print('Run demos event from dashboard')


@socketio.on('goto_lessons')
def goto_lessons():
    print('Go to lessons event from dashboard')


# updater function and page
@app.route('/update')
def update():
    return app.send_static_file('index.html')


@socketio.on('update_firmware')
def update_firmware():
    print('update firmware from dashboard')
    print('server down soon')
    time.sleep(1)
    subprocess.run(["sudo killall -9 python3 && sudo python3 -c 'import zumidashboard.updater as update; update.run()'"], shell=True)


@socketio.on('update_content')
def update_content():
    print('update content from dashboard')
    if updater.update_content(app.screen):  # return True or False
        time.sleep(2)
        app.screen.happy()

    else:
        app.screen.draw_text_center("Fail to update")
        time.sleep(1)
        app.screen.sad()
    socketio.emit('update_content')


# shutdown function and page
@app.route('/shutting-down')
def shutting_down():
    return app.send_static_file('index.html')


@socketio.on('shutdown')
def shutdown():
    app.screen.draw_text_center("Please switch off after 15 seconds.")
    scripts.shutdown()


# this is for refresh page
@app.route('/step2')
def step2():
    return app.send_static_file('index.html')

@app.route('/lesson')
def lesson():
    return app.send_static_file('index.html')   


def run(_debug=False):
    if not os.path.isfile('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json'):
        subprocess.run(["sudo ln -s /etc/hostname /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json"], shell=True)

    socketio.run(app, debug=_debug, host='0.0.0.0', port=80)


if __name__ == '__main__':
    run()
