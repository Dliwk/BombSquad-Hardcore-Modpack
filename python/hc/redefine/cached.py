from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List

from ._redefine import import_module
from _ba import pushcall, screenmessage
from ba import Lstr

from threading import Thread
import time
import os


def redefine_cached_methods(
      target: Optional[str],
      new_contents: List[str],
      pass_errors: bool = False,
      send_restart_message: bool = True) -> None:
    if not new_contents:
        if pass_errors:
            return
        raise ValueError()
    module = import_module(target)
    for attr in ['__file__', '__cached__']:
        if not getattr(module, attr, None):
            if pass_errors:
                return
            raise ValueError(f'Cann\'t find attribute "{attr}" in module "{target}"')

    def run() -> None:
        path = module.__file__
        if os.path.exists(path):
            with open(path) as f:
                contents = f.read()
                f.close()
            can_rewrite = False
            for nc in new_contents:
                if nc not in contents:
                    contents += f'\n\n{nc}\n\n'
                    can_rewrite = True
            if can_rewrite:
                with open(path, 'w') as f:
                    f.write(contents)
                    f.close()
                del contents
                path = module.__cached__
                if os.path.exists(path):
                    time.sleep(3.0)
                    os.remove(path)
                    time.sleep(0.5)
                    if send_restart_message:
                        pushcall(lambda: screenmessage(
                            Lstr(
                                resource='settingsWindowAdvanced.mustRestartText'),
                            color=(1.0, 0.5, 0.0)),
                                 from_other_thread=True)
    Thread(target=run).start()
