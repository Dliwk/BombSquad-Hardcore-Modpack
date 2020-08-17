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
#

# ba_meta require api 6
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, List, Any

import _ba, ba

def _get_new_items() -> Dict[str, List[Dict[str, Any]]]:
    return {
        'characters': [{
            'title': 'store.holidaySpecialText',
            'items': ['characters.bunny', 'characters.taobaomascot']}],
        'minigames': [{
            'title': 'store.holidaySpecialText',
            'items': ['games.easter_egg_hunt']}]
    }

def get_store_layout() -> Dict[str, List[Dict[str, Any]]]:
    store_layout = _get_store_layout()
    if store_layout:
        items = store_layout['characters'][0]['items']
        if 'characters.santa' not in items:
            i = items.index('characters.wizard')
            if i > -1:
                items = items[0: i - 1] + ['characters.santa'] + items[i:]
                store_layout['characters'][0]['items'] = items
        for key, values in _get_new_items().items():
            if key not in store_layout:
                continue
            for val in values:
                if val not in store_layout[key]:
                    store_layout[key].append(val)
    return store_layout

def i_was_imported() -> bool:
    result = bool(getattr(ba.app, '_ui_crack_enabled', False))
    setattr(ba.app, '_ui_crack_enabled', True)
    return result

def main() -> None:
    if i_was_imported():
        return
    for attr in [
        'get_store_layout']:
        globals()['_' + attr] = getattr(ba._store, attr)
        for module in [ba._store, ba.internal]:
            setattr(module, attr, globals()[attr])
        
# ba_meta export plugin
class HolidaySpecial(ba.Plugin):
    def on_app_launch(self) -> None:
        main()