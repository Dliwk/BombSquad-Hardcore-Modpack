# Copyright (c) 2020 Daniil Rakhov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ba_meta require api 6

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Callable, Dict

from enum import Enum
from bastd.ui import watch
from bastd.ui.fileselector import FileSelectorWindow
from copy import copy
from _ba import get_replays_dir

import ba

import os
import shutil
import threading


class LanguageEnglish(Enum):
    UPLOAD = 'Upload replay'
    SAVE = 'Save replay'
    SUCCESS = 'Success'
    UNSUCCESS = 'Unsuccess'


class LanguageRussian(Enum):
    UPLOAD = 'Загрузить реплей'
    SAVE = 'Сохранить реплей'
    SUCCESS = 'Успешно'
    UNSUCCESS = 'Возникла ошибка'


Language = copy(globals().get('Language' + ba.app.language,
                              LanguageEnglish))


def screenmessage(message: Language) -> None:
    if message not in Language:
        raise ValueError()
    if message == Language.SUCCESS:
        color = (0, 1.0, 0)
    elif message == Language.UNSUCCESS:
        color = (1.0, 0, 0)
    else:
        color = (1.0, 1.0, 1.0)
    with ba.Context('ui'):
        ba.screenmessage(
            message=message.value,
            color=color)


def open_fileselector(
        path: str,
        callback: Callable = None) -> None:
    with ba.Context('ui'):
        FileSelectorWindow(path,
                           callback, True, ['brp'], False)


def get_save_path() -> str:
    path = os.path.join(ba.app.python_directory_user, 'replays')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_upload_path() -> str:
    return get_replays_dir()


def thread(
        call: Callable,
        callback: Optional[Callable] = None) -> None:
    def _call() -> None:
        result = call()
        if callback:
            ba.pushcall(ba.Call(callback, result),
                        from_other_thread=True)

    threading.Thread(target=_call).start()


def copy_replay(src: str, dst: str) -> int:
    if (src and dst and os.path.exists(src) and
            os.path.exists(dst)):
        if not os.path.exists(dst + os.path.sep + os.path.basename(src)):
            try:
                shutil.copy(src, dst)
            except Exception as exc:
                print('coping exc:', exc)
                return 1
            else:
                return 0
    return 2


def upload_replays(watch_window: watch.WatchWindow) -> None:
    def on_copy(result: bool) -> None:
        if not result:
            screenmessage(Language.SUCCESS)
            with ba.Context('ui'):
                watch_window._my_replay_selected = None
                watch_window._refresh_my_replays()
        elif result == 1:
            screenmessage(Language.UNSUCCESS)

    def on_select(path: Optional[str]) -> None:
        thread(ba.Call(copy_replay, path, get_upload_path()),
               on_copy)
    open_fileselector(get_save_path(), on_select)


def save_replays() -> None:
    def on_copy(result: bool) -> None:
        if not result:
            screenmessage(Language.SUCCESS)
        elif result == 1:
            screenmessage(Language.UNSUCCESS)

    def on_select(path: Optional[str]) -> None:
        thread(ba.Call(copy_replay, path, get_save_path()),
               on_copy)

    open_fileselector(get_upload_path(), on_select)


def _set_tab(self, tab: str) -> None:
    if tab != 'my_replays':
        self._set_tab_replays(tab)
        return
    elif self._current_tab == tab:
        return

    uiscale = ba.app.ui.uiscale
    c_height = self._scroll_height - 20

    b_width = 140 if uiscale is ba.UIScale.SMALL else 178
    b_height = (82 if uiscale is ba.UIScale.SMALL else
                80 if uiscale is ba.UIScale.MEDIUM else 106)
    b_space_extra = (0 if uiscale is ba.UIScale.SMALL else
                     2 if uiscale is ba.UIScale.MEDIUM else 3)
    btnv = (c_height - (48 if uiscale is ba.UIScale.SMALL else
                        55 if uiscale is ba.UIScale.MEDIUM else 50) -
            b_height)
    btnh = 40

    tscl = 1.0 if uiscale is ba.UIScale.SMALL else 1.2

    b_color = (0.6, 0.53, 0.63)
    b_textcolor = (0.75, 0.7, 0.8)

    self._set_tab_replays(tab)
    for child in self._tab_container.get_children():
        if child and child.get_widget_type() == 'button':
            ba.buttonwidget(edit=child,
                            position=(btnh, btnv),
                            size=(b_width, b_height))
            btnv -= b_height + b_space_extra
    self._upload_replays_button = ba.buttonwidget(parent=self._tab_container,
                                                  size=(b_width, b_height),
                                                  position=(btnh, btnv),
                                                  button_type='square',
                                                  color=b_color,
                                                  textcolor=b_textcolor,
                                                  on_activate_call=ba.Call(upload_replays, self),
                                                  text_scale=tscl,
                                                  label=ba.Lstr(value=Language.UPLOAD.value),
                                                  autoselect=True)
    btnv -= b_height + b_space_extra
    self._save_replays_button = ba.buttonwidget(parent=self._tab_container,
                                                size=(b_width, b_height),
                                                position=(btnh, btnv),
                                                button_type='square',
                                                color=b_color,
                                                textcolor=b_textcolor,
                                                on_activate_call=ba.Call(save_replays),
                                                text_scale=tscl,
                                                label=ba.Lstr(value=Language.SAVE.value),
                                                autoselect=True)


def redefine(methods: Dict[str, Callable]) -> None:
    for n, func in methods.items():
        if hasattr(watch.WatchWindow, n):
            setattr(watch.WatchWindow, n + '_replays',
                    getattr(watch.WatchWindow, n))
        setattr(watch.WatchWindow, n, func)


def i_was_imported() -> bool:
    result = bool(getattr(ba.app, '_replays_enabled', False))
    setattr(ba.app, '_replays_enabled', True)
    return result


def main() -> None:
    if i_was_imported():
        return
    redefine({
        '_set_tab': _set_tab
    })


# ba_meta export plugin
class SaveAneShareReplays(ba.Plugin):
    def on_app_launch(self) -> None:
        main()
