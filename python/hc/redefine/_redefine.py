from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Dict, \
        Optional, Sequence, Any


class RedefineError(Exception):
    pass


def get_target_info(
        target: Optional[str],
        count: int = 2) -> Optional[Sequence[str, str]]:
    if count < 1:
        return [target]
    elif (count > 15 or count < 2) or \
            (not isinstance(target, str) and
             not isinstance(target, list)):
        raise ValueError()
    elif isinstance(target, str):
        target = target.split('.')
    result = []
    for i in range(count - 1):
        ind = (-count + i + 1)
        if not i:
            result.append('.'.join(target[:ind]))
        t = (target[ind: ind + 1] if
             ind < -1 else target[ind:])
        result.append(t[0] if len(t) else '')
    return tuple(result)


def import_module(module_name: str) -> Any:
    try:
        module = __import__(module_name, fromlist=['object'])
    except Exception as exc:
        raise RedefineError(exc, '\n',
                            'module:', module_name)
    return module


def redefine(
        target: Optional[str],
        methods: Dict[str, Callable],
        set_past: bool = False,
        pass_warnings: bool = False,
        pass_errors: bool = False) -> None:
    if not methods:
        if pass_errors:
            return
        raise ValueError()

    module_name, class_name = get_target_info(target, 2)
    module = import_module(module_name)
    cls = getattr(module, class_name, None)
    if not cls:
        if pass_errors:
            return
        raise RedefineError(class_name, 'not found')

    for method_name, obj in methods.items():
        m = getattr(cls, method_name, None)
        if m == obj:
            continue
        elif m is None:
            if not pass_warnings:
                print('Redefine warning:', 'can not find method',
                      method_name, 'in', class_name)
        else:
            if set_past:
                setattr(cls, method_name + '_hcmp', m)
        setattr(cls, method_name, obj)
    setattr(module, class_name, cls)
