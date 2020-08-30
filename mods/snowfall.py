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
    from typing import Dict, Callable

from ba import _activity, Plugin
import _ba

import random


def i_was_imported() -> bool:
    result = getattr(_ba.app, '_snowfall_enabled', False)
    setattr(_ba.app, '_snowfall_enabled', True)
    return result


def redefine(methods: Dict[str, Callable]) -> None:
    for n, func in methods.items():
        if hasattr(_activity.Activity, n):
            setattr(_activity.Activity, n + '_snowfall',
                    getattr(_activity.Activity, n))
        setattr(_activity.Activity, n, func)


def snowfall(self) -> None:
    if hasattr(self, '_snowfall'):
        delattr(self, '_snowfall')
    if getattr(self, 'map', None):
        bounds = self.map.get_def_bound_box('map_bounds')

        def emits() -> None:
            for i in range(int(bounds[3] * bounds[5])):
                def _emit() -> None:
                    _ba.emitfx(
                        position=(
                            random.uniform(bounds[0], bounds[3]),
                            random.uniform(bounds[4] * 1.15, bounds[4] * 1.45),
                            random.uniform(bounds[2], bounds[5])
                        ),
                        velocity=(0, 0, 0),
                        scale=random.uniform(0.5, 0.8),
                        count=random.randint(7, 18),
                        spread=random.uniform(0.05, 0.1),
                        chunk_type='spark'
                    )
                _ba.timer(random.uniform(0.02, 0.05) * (i + 1),
                          _emit)

        setattr(self, '_snowfall',
                _ba.timer(0.5, emits, repeat=True))


def on_begin(self) -> None:
    """Called once the previous ba.Activity has finished transitioning out.

    At this point the activity's initial players and teams are filled in
    and it should begin its actual game logic.
    """
    self.snowfall()
    return self.on_begin_snowfall()


def main() -> None:
    if i_was_imported():
        return
    redefine({
        'snowfall': snowfall,
        'on_begin': on_begin
    })


# ba_meta export plugin
class SnowFall(Plugin):
    def on_app_launch(self) -> None:
        main()
