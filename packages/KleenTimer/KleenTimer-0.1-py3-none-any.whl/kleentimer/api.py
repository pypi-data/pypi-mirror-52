from . import timer


def start_timer():
    timer.KleenTimer.start_timer()


def end_timer():
    timer.KleenTimer.end_timer()


def print_elapsed_time(output):
    print(timer.KleenTimer.elapsed_time(output))
