from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, Optional

from ._redefine import redefine


def make_factory(
        target: Optional[str],
        update_factory_method: Callable,
        pass_warnings: bool = False) -> Any:
    @classmethod
    def get(cls) -> Any:
        """Rebuilded by mainfactory."""
        factory = cls.get_hcmp()
        if not getattr(factory, '_updated', False):
            factory.update()
        return factory
    redefine(
        target=target, methods={
            'get': get,
            'update': update_factory_method
        },
        set_past=True,
        pass_warnings=pass_warnings)
