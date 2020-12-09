from simpleobsws import obsws

from obs.types.filter import add_filter, remove_filter


async def add_blur_filter(ws: obsws, source: str, size=15, name: str = 'Blur'):
    settings = {
        'Filter.Blur.Type': 'Box',
        'Filter.Blur.Subtype': 'Area',
        'Filter.Blur.Size': size
    }
    await add_filter(ws=ws, source=source, filter=name, type='streamfx-filter-blur', settings=settings)


async def remove_blur_filter(ws: obsws, source: str, name: str = 'Blur'):
    await remove_filter(ws=ws, source=source, filter=name)
