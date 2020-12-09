from simpleobsws import obsws

from obs.types.filter import add_filter, remove_filter


async def add_scroll_filter(ws: obsws, source: str, name: str = 'Scroll',
                              speed_x: int=0, speed_y: int = 0):
    settings = {
        'speed_x': speed_x,
        'speed_y': speed_y
    }
    await add_filter(ws=ws, source=source, filter=name, type='scroll_filter', settings=settings)


async def remove_scroll_filter(ws: obsws, source: str, name: str = 'Scroll'):
    await remove_filter(ws=ws, source=source, filter=name)
