from time import sleep


def lamp_aan(component_id, intensity):
    print("Lamp %s aan (%s)" % (component_id, intensity))


def check_lamp(component_id, expected_state):
    sleep(0.3)
