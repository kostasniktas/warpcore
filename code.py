import json
import time

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import digitalio
import neopixel
import socketpool
import wifi

import effects

NUM_PIXELS = 24
ENGINE_CORE = 12

COLOR_OFF = (0,0,0)

pixels = neopixel.NeoPixel(board.GP16, NUM_PIXELS)
pixels.brightness = 0.5

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Effect Button
button_0 = digitalio.DigitalInOut(board.GP17)
button_0.switch_to_input(pull=digitalio.Pull.DOWN)
BUTTON_0 = 0

# Speed Button
button_1 = digitalio.DigitalInOut(board.GP20)
button_1.switch_to_input(pull=digitalio.Pull.DOWN)
BUTTON_1 = 1

EFFECTS, EFFECTS_ITERATIONS = effects.get_all_effect_entries(pixels, ENGINE_CORE)
EFFECTS_SIZE = len(EFFECTS_ITERATIONS)

print("All the supported effects: " + str([item for sublist in EFFECTS_ITERATIONS for item in sublist]))

STATE_ON="ON"
STATE_OFF="OFF"
class StateClass(object):
    state_on: bool = False
    entry: effects.EffectEntry = effects.NOT_FOUND_EFFECT
    effect = None # fix typing
    effect_index: int = 0
    speed_index: int = 0


    def as_mqtt_state(self):
        state = {}
        state["state"] = STATE_ON if self.state_on else STATE_OFF
        if self.entry and self.entry != effects.NOT_FOUND_EFFECT:
            state["effect"] = self.entry.full_name()
        else:
            state["effect"] = None
        return state
    def set_entry(self, entry: effects.EffectEntry):
        if entry == effects.NOT_FOUND_EFFECT or entry.full_name() == "nothing":
            self.state_on = False
        else:
            self.state_on = True
        self.entry = entry
        self.effect_index = self.entry.index_effect
        self.speed_index = self.entry.index_speed
        self.effect = self.entry.effect()

the_state = StateClass()

topic_set = "testing/warpcore/set"
topic_state = "testing/warpcore"

def connect(mqtt_client, userdata, flags, rc):
    print("Connected to MQTT")
    print("Subscribing to %s" % topic_set)
    mqtt_client.subscribe(topic_set)
    send_state(mqtt_client)

def disconnect(mqtt_client, userdata, rc):
    print("Disconnected from MQTT")

def subscribe(mqtt_client, userdata, topic, granted_qos):
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

def unsubscribe(mqtt_client, userdata, topic, pid):
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))

def publish(mqtt_client, userdata, topic, pid):
    print("Published to {0}".format(topic))

def get_by_name(effect_name: str) -> effects.EffectEntry:
    if "_" not in effect_name:
        name = effect_name
        speed = ""
    else:
        name, speed = effect_name.rsplit("_", 1)
    try:
        effect_entry = EFFECTS[name][speed]
        return effect_entry
    except:
        print("Didn't find effect %s" % name)
        return effects.NOT_FOUND_EFFECT

def get_by_index(effect: int, speed: int) -> effects.EffectEntry:
    try:
        effect_entry = EFFECTS_ITERATIONS[effect][speed]
        return effect_entry
    except:
        return effects.NOT_FOUND_EFFECT

def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic,message))
    payload = {}
    try:
        payload = json.loads(message)
    except ValueError:
        print("Not JSON, ignore")
        return
    process_json(payload)
    send_state(client)

def process_json(payload):
    global the_state
    if "state" in payload:
        if payload["state"] == STATE_ON:
            if "effect" in payload:
                the_state.set_entry(get_by_name(payload["effect"]))
            else:
                the_state.set_entry(get_by_index(1,0))
        else:
            the_state.set_entry(get_by_name("nothing"))
    pass # TODO: gc.collect() do we need this on RP2040?
    return True

def send_state(client):
    state = the_state.as_mqtt_state()
    print("Sending state %s" % state)
    client.publish(topic_state, json.dumps(state))

from secrets import secrets

if "name" in secrets:
    wifi.radio.hostname = secrets["name"]
print("Connecting to %s" % secrets["wifi"])
wifi.radio.connect(secrets["wifi"], secrets["wifi_pw"])
print("Connected to %s with address %s" % (secrets["wifi"], wifi.radio.ipv4_address))
# TODO: Add logic to show errors with connections.


pixels.fill((100,100,0))
pixels.show()
time.sleep(1)
pixels.fill((0,0,0))
pixels.show()

# hard coding initial
the_state.set_entry(get_by_name("nothing"))

print("HI")

pool = socketpool.SocketPool(wifi.radio)
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt"],
    port=1883,
    username=secrets["mqtt_user"],
    password=secrets["mqtt_pw"],
    socket_pool=pool
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

changed = False
next_speed = 0
next_effect = 0
print("before loop")
while True:
    the_state.effect.animate()
    if button_0.value:
        next_effect = (the_state.effect_index + 1) % EFFECTS_SIZE
        next_speed = 0
        print("Changing effect")
        changed = True
    if button_1.value:
        next_speed = (the_state.speed_index + 1) % len(EFFECTS_ITERATIONS[the_state.effect_index])
        next_effect = the_state.effect_index
        print("Changing speed to " + str(next_speed))
        changed = True
    if changed:
        effect_entry = get_by_index(next_effect, next_speed)
        pixels.fill(COLOR_OFF)
        pixels.show()
        changed = False
        print("Changing to {0} {1} {2}".format(next_effect, next_speed, effect_entry.full_name()))
        the_state.set_entry(effect_entry)
        send_state(mqtt_client)
    time.sleep(0.05)
