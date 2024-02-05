import datetime
import os
from typing import List, TypeVar

T = TypeVar("T")


def listify(o: T) -> List[T]:
    if isinstance(o, list):
        return o
    else:
        return [o]


def now_ts() -> float:
    return datetime.datetime.now().timestamp()


def now_str(frmt="%Y%m%d-%H:%M:%S.%f") -> str:
    return datetime.datetime.now().strftime(frmt)


def now_str_iso() -> str:
    return now_str(frmt="%Y-%m-%dT%H:%M:%S.%f")


def get_proc_name() -> str:
    import psutil
    process = psutil.Process(os.getpid())
    process_name = process.name()
    return process_name


def parse_db_url(db_url: str) -> (str, str, str, str, int, str):
    dialect, tail = db_url.split("://", maxsplit=1)
    usr_pwd, host_port_db = tail.split("@", maxsplit=1)
    host_port, db = host_port_db.split("/", maxsplit=1)

    user, pwd = usr_pwd.split(":", maxsplit=1)
    host, port = host_port.split(":", maxsplit=1)
    port = int(port)

    return dialect, host, port, user, pwd, db


def get_project_root(marker: str = "src", current_dir: str = None) -> str:
    """
    Recursively inspects from current_dir heading up to FS root.
    :param marker: file/folder to search for in root dir. (src by deafult)
    :param current_dir: start_search from. will os.getcwd() if not defined
    :return: path to root dir (str)
    """
    if current_dir is None:
        current_dir = os.getcwd()

    if os.name == 'nt':
        delim = "\\"
    else:
        delim = "/"

    if os.path.exists(f"{current_dir}{delim}{marker}"):
        return current_dir

    splitted = current_dir.split(delim)

    new_current_dir = delim.join(splitted[:-1])

    return get_project_root(marker, current_dir=new_current_dir)
