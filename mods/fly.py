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
    from typing import Sequence, Optional, Any

from bastd.actor import playerspaz

import time
import ba

def __init__(self,
             player: ba.Player,
             color: Sequence[float] = (1.0, 1.0, 1.0),
             highlight: Sequence[float] = (0.5, 0.5, 0.5),
             character: str = 'Spaz',
             powerups_expire: bool = True):
    self.can_fly = False
    self.holding_node = None
    self._combine = None
    self._offset = [0, 0, 0]
    self.fly_timer = None
    self.fly_speed = self.fly_speed_normal = 2.0
    self.last_jump_press_time = 0.0
    self.__init___fly(player, color, 
        highlight, character, powerups_expire)

def delete_holding_node(self) -> None:
    if self.holding_node:
        self.holding_node.delete()
        self.holding_node = None
    if self._combine:
        self._combine.delete()
        self._combine = None
    self.fly_timer = None

def spawn_holding_node(self) -> Optional[ba.Node]:
    if not self.node:
        return None
    self.delete_holding_node()
    t = self.node.position
    t = (t[0], t[1] + 1, t[2])
    self.holding_node = ba.newnode('prop', 
        owner = self.node,
        delegate = self, 
        attrs={
            'position': t,
            'body': 'box',
            'body_scale': 0.000001,
            'model': None,
            'model_scale': 0.000001,
            'color_texture': None,
            'max_speed': 0,
            'owner': self.node,
            'materials': []
        })
    self._combine = ba.newnode('combine', 
        owner = self.holding_node, 
        attrs={
            'size': 3
        })
    self._offset = [0, 0, 0]
    self._combine.input0, self._combine.input1, self._combine.input2 = t
    self._combine.connectattr('output', self.holding_node, 'position')

    self.move_holding_node('xyz')
    self.fly_timer = ba.Timer(0.1, ba.WeakCall(self.move_holding_node, 'xyz'), 
        repeat=True)
    return self.holding_node

def move_holding_node(self, move: str = '') -> None:
    if self._combine:
        t = []
        if 'x' in move: t.append(0)
        if 'y' in move: t.append(1)
        if 'z' in move: t.append(2)

        for i in t:
            val = getattr(self._combine, 'input{}'.format(i), None)
            if val is not None:
                ba.animate(self._combine, 'input{}'.format(i), {
                    0: val, 
                    0.5: val + self._offset[i]
                })

def set_fly_mode(self, fly_mode: bool = True) -> None:
    self.can_fly = fly_mode
    self.on_move_up_down(0)
    self.on_move_left_right(0)
    if self.can_fly:
        node = self.spawn_holding_node() 
        self.node.hold_body = 0
        self.node.hold_node = node
    else:
        self.delete_holding_node()
        self.node.hold_body = 0
        self.node.hold_node = None

def on_punch_press(self) -> None:
    if not self.can_fly: 
        self.on_punch_press_fly()
    else: 
        self.fly_speed = self.fly_speed_normal * 0.5

def on_punch_release(self) -> None:
    if not self.can_fly: 
        self.on_punch_release_fly()
    else: 
        self.fly_speed = self.fly_speed_normal

def on_bomb_press(self) -> None:
    if not self.can_fly: 
        self.on_bomb_press_fly()
    else: 
        self.fly_speed = self.fly_speed_normal * 2.5

def on_bomb_release(self) -> None:  
    if not self.can_fly: 
        self.on_bomb_release_fly()
    else: 
        self.fly_speed = self.fly_speed_normal

def on_jump_press(self) -> None:
    if not self.node:
        return
    now = time.time()
    if now - self.last_jump_press_time < 0.29: 
        self.set_fly_mode(not self.can_fly)
    else:
        self.last_jump_press_time = now
        if not self.can_fly: 
            self.on_jump_press_fly()
        else: 
            self._offset[1] = 0.5 * self.fly_speed
            self.move_holding_node('y')

def on_jump_release(self) -> None:
    if not self.can_fly: 
        self.on_jump_release_fly()
    else: 
        self._offset[1] = 0

def on_pickup_press(self) -> None:
    if not self.can_fly:
        self.on_pickup_press_fly()
    elif self.node and self.holding_node: 
        self._offset[1] = -0.5 * self.fly_speed
        self.move_holding_node()

def on_pickup_release(self) -> None:
    if not self.can_fly: 
        self.on_pickup_release_fly()
    else: 
        self._offset[1] = 0

def on_move_up_down(self, value: float) -> None:
    if not self.can_fly: 
        self.on_move_up_down_fly(value)
    elif self.node:
        if self.frozen or self.node.knockout > 0.0:
            self._offset[2] = 0.0
        else:
            self._offset[2] = -value * self.fly_speed

def on_move_left_right(self, value: float) -> None:
    if not self.can_fly: 
        self.on_move_left_right_fly(value)
    elif self.node: 
        if self.frozen or self.node.knockout > 0.0:
            self._offset[0] = 0.0
        else:
            self._offset[0] = value * self.fly_speed

def handlemessage(self, msg: Any) -> Any:
    assert not self.expired

    if isinstance(msg, ba.HitMessage) and self.can_fly:
        if not self.frozen and self.node.knockout <= 0.0:
            return
    self.handlemessage_fly(msg)

def redefine(methods: Dict[str, Callable]) -> None:
    for n, func in methods.items():
        if hasattr(playerspaz.PlayerSpaz, n):
            setattr(playerspaz.PlayerSpaz, n + '_fly', 
                getattr(playerspaz.PlayerSpaz, n))
        setattr(playerspaz.PlayerSpaz, n, func)

def i_was_imported() -> bool:
    result = bool(getattr(ba.app, '_fly_enabled', False))
    setattr(ba.app, '_fly_enabled', True)
    return result

def main() -> None:
    if i_was_imported():
        return
    redefine({
        '__init__': __init__,
        'on_punch_press': on_punch_press,
        'on_punch_release': on_punch_release,
        'on_bomb_press': on_bomb_press,
        'on_bomb_release': on_bomb_release,
        'on_jump_press': on_jump_press,
        'on_jump_release': on_jump_release,
        'on_pickup_press': on_pickup_press,
        'on_pickup_release': on_pickup_release,
        'on_move_up_down': on_move_up_down,
        'on_move_left_right': on_move_left_right,
        'handlemessage': handlemessage,
        'set_fly_mode': set_fly_mode,
        'move_holding_node': move_holding_node,
        'spawn_holding_node': spawn_holding_node,
        'delete_holding_node': delete_holding_node
    })

# ba_meta export plugin
class AdvancedFly(ba.Plugin):
    def on_app_launch(self) -> None:
        main()