def moving_average_filter(values, window=3):
    filtered = []
    for i in range(len(values)):
        recent = values[max(0, i-window+1):i+1]
        recent = [v for v in recent if v is not None]
        filtered.append(round(sum(recent) / len(recent), 2) if recent else None)
    return filtered