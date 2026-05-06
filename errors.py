import random

def inject_error(value):
    error = random.choices(
        ["normal", "noise", "missing", "spike"],
        weights=[0.55, 0.25, 0.10, 0.10]
    )[0]

    if error == "normal":
        return value, error
    elif error == "noise":
        return round(value + random.uniform(-1.5, 1.5), 2), error
    elif error == "missing":
        return None, error
    elif error == "spike":
        return round(value + random.choice([-1, 1]) * random.uniform(3, 5), 2), error