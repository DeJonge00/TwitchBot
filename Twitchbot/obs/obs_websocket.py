from asyncio import get_event_loop

from simpleobsws import obsws

from obs.change_theme import change_theme
from obs.constants import COLOR_GREEN, COLOR_PINK, COLOR_BLUE
from obs.scrolling_announcement import setup_scrolling_announcement, scrolling_announcement
from obs.types.filter import get_source_filters
from obs.types.source import get_source_settings
from secret.secrets import obs_password, obs_port, obs_address


async def exec_func(ws, f, args):
    if len(args) == 1 and isinstance(args[0], dict):
        return await f(ws, **args[0])
    return await f(ws, *args)


async def request(ws: obsws, function, *args):
    await ws.connect()
    r = await exec_func(ws, function, args)
    await ws.disconnect()
    return r


async def multi_request(ws: obsws, functions: [], args: []):
    await ws.connect()
    for f, a in zip(functions, args):
        await exec_func(ws, f, a)
    await ws.disconnect()


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
        host=obs_address,
        port=obs_port,
        password=obs_password
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
    # loop.run_until_complete(request(ws, change_theme, COLOR_GREEN))
    # loop.run_until_complete(request(ws, change_theme, COLOR_PINK))
    # loop.run_until_complete(request(ws, change_audio_visualizer_color, source, 4294949411))

    # -- Scrolling Announcement
    # loop.run_until_complete(request(ws, setup_scrolling_announcement, source))
    # loop.run_until_complete(
    #     request(ws, scrolling_announcement, source, 15 * '1234567890'))
