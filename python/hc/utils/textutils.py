from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict


def format_spaces(msg: str,
                  only_check_end: bool = False) -> str:
    if not only_check_end:
        for k, v in [(' ,', ', '), (' /', '/'), (' .', '.')]:
            msg = msg.replace(k, v)
            while '  ' in msg:
                msg = msg.replace('  ', ' ')
    if msg.endswith(' '):
        msg = msg[:-1]
    if msg.startswith(' '):
        msg = msg[1:]
    return msg


def format_commandline(msg: str,
                       key: str = '-') -> Dict[str, str]:
    keys = [key + i.split(' ')[0] for i in msg.split(key)[1:] if i[0] != ' ']
    result = {}
    for i, k in enumerate(keys):
        if i == len(keys) - 1:
            val = msg.split(k)[1]
        else:
            val = msg.split(k)[1].split(keys[i + 1])[0]
        result[k.strip(key)] = format_spaces(val.replace(k, ' '), True)
    return result
