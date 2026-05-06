import random
import math

#It simulates real temperature over time
def true_temperature(step):
    return round(25 + 2.2 * math.sin(step / 8) + random.uniform(-0.2, 0.2), 2)