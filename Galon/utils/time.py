import time

StartTime = time.time()


def get_readable_time(seconds: int) -> str:
    count = 0
    waktu = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        waktu += time_list.pop() + ", "
    time_list.reverse()
    waktu += ":".join(time_list)

    return waktu
