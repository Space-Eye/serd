from datetime import date

Interval = tuple[date, date]

def overlaps(a: Interval, b: Interval)->bool:
    if a[0] > a[1]:
        raise ValueError("[{0}, {1}] is not a valid interval".format(a[0], a[1]))
    if b[0] > b[1]:
        raise ValueError("[{0}, {1}] is not a valid interval".format(b[0], b[1]))
    if a[0] <= b[0] and a[1] <= b[0]:
        return False
    if a[0] >= b[1] and a[1] >= b[1]:
        return False
    if a[0] <= b[0] and a[1] > b[0]:
        return True
    if b[0] <= a[0] and b[1] > a[0]:
        return True
    if a[0] <= b[0] and a[1] >= b[1]:
        return True
    if  b[0] <= a[0] and b[1] >= a[1]:
        return True
    assert(False)
