import time


class KleenTimer:
    start_time = 0
    end_time = 0

    @staticmethod
    def start_timer():
        KleenTimer.start_time = time.time()

    @staticmethod
    def end_timer():
        KleenTimer.end_time = time.time()

    @staticmethod
    def elapsed_time(output):
        total_s = int(KleenTimer.end_time - KleenTimer.start_time)
        secondes = total_s % 60
        minutes = (total_s / 60) % 60
        minutes = int(minutes)
        hours = (total_s / (60 * 60)) % 24
        hours = int(hours)
        return output.format(hours=hours, minutes=minutes, secondes=secondes)
