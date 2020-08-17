from asyncio import sleep

from simpleobsws import obsws

from obs.constants import hue_shift_colors
from secret.secrets import user_defined_shader_folder


async def get_source_filters(ws: obsws, source: str):
    r = await ws.call(
        'GetSourceFilters',
        {
            'sourceName': source
        }
    )
    if r.get('filters'):
        print("Get source filters\nFilters:\n{}".format('\n'.join([str(x) for x in r.get('filters')])))
        return
    print("Get source filters\nResponse: {}\n".format(r))


async def add_filter(ws: obsws, source: str, filter: str, type: str, settings: dict):
    r = await ws.call(
        'AddFilterToSource',
        {
            'sourceName': source,
            'filterName': filter,
            'filterType': type,
            'filterSettings': settings
        }
    )
    print("Added '{}' to '{}'\nResponse: {}\n".format(filter, source, r))


async def remove_filter(ws: obsws, source: str, filter: str):
    r = await ws.call(
        'RemoveFilterFromSource',
        {
            'sourceName': source,
            'filterName': filter
        }
    )
    print("Removed '{}' from '{}'\nResponse: {}\n".format(filter, source, r))


async def add_blur_filter(ws: obsws, source: str, size=15):
    settings = {
        'Filter.Blur.Type': 'Box',
        'Filter.Blur.Subtype': 'Area',
        'Filter.Blur.Size': size
    }
    await add_filter(ws=ws, source=source, filter='Blur', type='streamfx-filter-blur', settings=settings)


async def remove_blur_filter(ws: obsws, source: str):
    await remove_filter(ws=ws, source=source, filter='Blur')


async def add_color_correction_filter(ws: obsws, source: str, gamma=0, contrast=0, brightness=0, saturation=0,
                                      hue_shift=0, opacity=100, color=None):
    settings = {
        'gamma': gamma,
        'contrast': contrast,
        'brightness': brightness,
        'saturation': saturation,
        'hue_shift': hue_shift,
        'opacity': opacity,
        'color': color
    }
    await add_filter(ws=ws, source=source, filter='Color Correction', type='color_filter', settings=settings)


async def remove_color_correction_filter(ws: obsws, source: str):
    await remove_filter(ws=ws, source=source, filter='Color Correction')


async def add_shader_filter(ws: obsws, source: str, shader: str):
    settings = {
        'from_file': True,
        'shader_file_name': user_defined_shader_folder + shader
    }
    await add_filter(ws=ws, source=source, filter='User-defined-shader', type='shader_filter', settings=settings)


async def remove_shader_filter(ws: obsws, source: str):
    await remove_filter(ws=ws, source=source, filter='User-defined-shader')


async def temp_blur_filter(websocket: obsws, source: str, seconds: int = 10):
    await add_blur_filter(websocket, source)
    await sleep(seconds)
    await remove_blur_filter(websocket, source)


async def temp_color_filter(ws: obsws, source: str, color: str, seconds: int = 10):
    await add_color_correction_filter(ws, source, hue_shift=hue_shift_colors.get(color))
    await sleep(seconds)
    await remove_color_correction_filter(ws, source)


async def temp_shader_filter(ws: obsws, source: str, shader: str, seconds: int = 10):
    await add_shader_filter(ws, source, shader=shader)
    await sleep(seconds)
    await remove_shader_filter(ws, source)
