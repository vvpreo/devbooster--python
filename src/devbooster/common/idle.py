import time

_start_proc_at = time.time()
_start_proc_cpu_at = time.process_time()


def get_proc_busy() -> float:
    """
    :return: proc_time/time from last func call or program start (module import)
    """
    global _start_proc_at, _start_proc_cpu_at
    _start_proc_at_2 = time.time()
    _start_proc_cpu_at_2 = time.process_time()

    overall = _start_proc_at_2 - _start_proc_at
    overall_cpu = _start_proc_cpu_at_2 - _start_proc_cpu_at


    _start_proc_at = _start_proc_at_2
    _start_proc_cpu_at = _start_proc_cpu_at_2

    return overall_cpu / overall

