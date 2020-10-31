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
    from typing import Any


from ba._plugin import Plugin
import _ba


def i_was_imported() -> bool:
    result = getattr(_ba.app, '_is_pro_version', False)
    setattr(_ba.app, '_is_pro_version', True)
    return result


def redefine() -> None:
    a = _ba.get_account_misc_read_val_2
    b = _ba.get_purchased

    def _a(misc_name: str, default_value: Any = None) -> Any:
        if misc_name == 'proOptionsUnlocked':
            return True
        return a(misc_name, default_value)

    def _b(purchase_name: str) -> bool:
        if purchase_name in [
              'upgrades.pro', 
              'static.pro', 
              'static.pro_sale']:
            return True
        return b(purchase_name)
    _ba.get_account_misc_read_val_2 = _a
    _ba.get_purchased = _b


def main() -> None:
    if i_was_imported():
        return
    redefine()


# ba_meta export plugin
class ProVersion(Plugin):
    def on_app_launch(self) -> None:
        main()