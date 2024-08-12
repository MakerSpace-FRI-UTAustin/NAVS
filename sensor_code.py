from gpiozero import DistanceSensor, OutputDevice, Button
from time import sleep
from decimal import Decimal, ROUND_HALF_UP
sensors_pins = {
    'middle': {'trigger': 23, 'echo': 24, 'haptics': [17, 27, 22]},
    'left': {'trigger': 5, 'echo': 6, 'haptics': [10, 9, 11]},
    'right': {'trigger': 13, 'echo': 19, 'haptics': [25, 8, 7]},
    'back': {'trigger': 20, 'echo': 21, 'haptics': [18, 15, 14]}
}


sensors = {}
for position, pins in sensors_pins.items():
    sensors[position] = {
        'sensor': DistanceSensor(echo=pins['echo'], trigger=pins['trigger']),
        'haptics': [OutputDevice(pin) for pin in pins['haptics']]
    }


switch = Button(4)

def vibrate_haptics(distance, haptics, is_urban):
    if is_urban:
        if distance <= 0.2:
            haptics[0].on()
            haptics[1].on()
            haptics[2].on()
        elif distance <= 0.5:
            haptics[0].on()
            haptics[1].on()
            haptics[2].off()
        elif distance <= 0.8:
            haptics[0].on()
            haptics[1].off()
            haptics[2].off()
        else:
            haptics[0].off()
            haptics[1].off()
            haptics[2].off()
    else:
        if distance <= 0.7:
            haptics[0].on()
            haptics[1].on()
            haptics[2].on()
        elif distance <= 1.15:
            haptics[0].on()
            haptics[1].on()
            haptics[2].off()
        elif distance <= 3.0:
            haptics[0].on()
            haptics[1].off()
            haptics[2].off()
        else:
            haptics[0].off()
            haptics[1].off()
            haptics[2].off()

try:
    while True:
        is_urban = switch.is_pressed
        environment = "Urban" if is_urban else "Rural"
        print(f"Environment: {environment}")

        for position, components in sensors.items():
            distance = components['sensor'].distance * 100  # convert to cm
            print(f"{position.capitalize()} Distance: {distance:.2f} cm")
            vibrate_haptics(distance, components['haptics'], is_urban)
        
        sleep(0.5 if is_urban else 1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
