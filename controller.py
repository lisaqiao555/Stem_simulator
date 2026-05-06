from config import FAN_ON, FAN_OFF

def fan_control(temp, previous_state):
    if temp is None:
        return previous_state
    if temp > FAN_ON:
        return "ON"
    elif temp < FAN_OFF:
        return "OFF"
    return previous_state