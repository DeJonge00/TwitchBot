from asyncio import sleep

from simpleobsws import obsws

from obs.constants import hue_shift_colors
from obs.types.filters.blur import add_blur_filter, remove_blur_filter
from obs.types.filters.color_correction import add_color_correction_filter, remove_color_correction_filter
from obs.types.filters.shader import add_shader_filter, remove_shader_filter


async def temp_blur_filter(ws: obsws, source: str, seconds: int = 10):
    await add_blur_filter(ws, source)
    await sleep(seconds)
    await remove_blur_filter(ws, source)


async def temp_color_filter(ws: obsws, source: str, color: str, seconds: int = 10):
    await add_color_correction_filter(ws, source, hue_shift=hue_shift_colors.get(color))
    await sleep(seconds)
    await remove_color_correction_filter(ws, source)


async def temp_shader_filter(ws: obsws, source: str, shader: str, seconds: int = 10):
    await add_shader_filter(ws, source, shader=shader)
    await sleep(seconds)
    await remove_shader_filter(ws, source)
