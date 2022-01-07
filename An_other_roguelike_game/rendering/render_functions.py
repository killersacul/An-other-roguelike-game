from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

import config.color as color
import engine.tile_types as tile_types
import numpy as np
import tcod as tc
from config.settings import MAP_HEIGHT, MAP_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH

if TYPE_CHECKING:
    from tcod import Console
    from engine.engine import Engine
    from engine.game_map import GameMap
    from engine.tile_types import graphic_dt


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(entity.name for entity in game_map.entities if entity.x == x and entity.y == y)

    return names.capitalize()


def render_bar(console: Console, current_value: int, maximum_value: int, total_width: int) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled)

    console.print(x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text)


def render_dungeon_level(console: Console, dungeon_level: int, location: Tuple[int, int]) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")


def render_names_at_mouse_location(console: Console, x: int, y: int, engine: Engine) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, game_map=engine.game_map)
    console.print(x=x, y=y, string=names_at_mouse_location)


def render_vline(
    console: Console,
    x: int,
    y: int,
    total_length: int,
    width: Optional[int] = 1,
    graphic_dt: Optional[graphic_dt] = (64, [220, 220, 220], [220, 220, 220]),
) -> None:
    console.tiles_rgb[x : x + total_length, y : y + width] = graphic_dt  # top bar


def render_hline(
    console: Console,
    x: int,
    y: int,
    total_length: int,
    width: Optional[int] = 1,
    graphic_dt: Optional[graphic_dt] = (64, [220, 220, 220], [220, 220, 220]),
) -> None:
    console.tiles_rgb[x : x + width, y : y + total_length] = graphic_dt  # bottom bar


def render_game_layout(console: Console, engine: Engine) -> None:
    render_vline(console, 0, SCREEN_HEIGHT - 1, SCREEN_WIDTH, 1, tile_types.BORDER)
    render_hline(console, 0, 55, SCREEN_HEIGHT - 55, 1, tile_types.BORDER)
    render_hline(console, SCREEN_WIDTH - 1, 55, SCREEN_HEIGHT - 55, 1, tile_types.BORDER)
    render_vline(console, 0, 55, SCREEN_WIDTH, 1, tile_types.BORDER)
    render_hline(console, 50, 55, 15, 1, tile_types.BORDER)
    render_hline(console, 100, 55, 15, 1, tile_types.BORDER)
