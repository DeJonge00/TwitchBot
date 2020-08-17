from asyncio import get_event_loop, sleep

from simpleobsws import obsws

from obs.change_theme import change_border_color, change_theme, change_audio_visualizer_color
from obs.constants import COLOR_RED, COLOR_BLUE, COLOR_RAINBOW
from obs.source import get_source_settings
from obs.temp_blur_filter import get_source_filters


async def request(ws: obsws, function, *args):
    await ws.connect()
    if len(args) == 1 and isinstance(args[0], dict):
        r = await function(ws, **args[0])
    else:
        r = await function(ws, *args)
    await ws.disconnect()
    return r


async def change_text(ws: obsws):
    r = await ws.call(
        'GetSceneItemProperties',
        {
            'scene-name': 'test',
            'item': 'testtext'
        })
    print(r)

    r = await ws.call(
        'SetSceneItemProperties',
        {
            'scene-name': 'test',
            'item': 'testtext'
        })
    print(r)


async def get_source_filter_info(ws: obsws, source: str, filter: str):
    r = await ws.call(
        'GetSourceFilterInfo',
        {
            'sourceName': source,
            'filterName': filter
        }
    )
    print("Source filter info\nResponse: {}\n".format(r))


async def get_version(websocket: obsws):
    result = await websocket.call('GetVersion')
    print(result)


def get_ws_and_loop():
    loop = get_event_loop()
    return obsws(
        host='127.0.0.1',
        port=4444,
        # password='MYSecurePassword',
        # loop=loop
    ), loop


if __name__ == '__main__':
    ws, loop = get_ws_and_loop()

    source = 'StreamerName'
    # loop.run_until_complete(request(ws, get_version))
    loop.run_until_complete(request(ws, get_source_settings, source))
    loop.run_until_complete(request(ws, get_source_filters, source))

    # -- Filters
    # loop.run_until_complete(request(ws, temp_blur_filter, test_source, 1))
    # params = {'source': test_source, 'color': COLOR_PINK, 'seconds': 1}
    # loop.run_until_complete(request(ws, temp_color_filter, params))
    # params['color'] = COLOR_RED
    # loop.run_until_complete(request(ws, temp_color_filter, params))
    # params['color'] = COLOR_BLUE
    # loop.run_until_complete(request(ws, temp_color_filter, params))
    # loop.run_until_complete(request(ws, temp_shader_filter, source, SHADER_CELL_SHADED, 1))

    # -- Theme
    # loop.run_until_complete(request(ws, change_theme, COLOR_RAINBOW))
    # loop.run_until_complete(request(ws, change_theme, COLOR_RED))
    loop.run_until_complete(request(ws, change_theme, COLOR_BLUE))
    # loop.run_until_complete(request(ws, change_audio_visualizer_color, source, 4294949411))
