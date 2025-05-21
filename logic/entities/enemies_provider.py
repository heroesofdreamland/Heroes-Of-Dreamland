from typing import TypeAlias, Callable

EnemiesProvider: TypeAlias = Callable[[], list[object | None]]
