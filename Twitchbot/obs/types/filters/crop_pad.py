from simpleobsws import obsws

from obs.types.filter import add_filter, remove_filter


async def add_crop_pad_filter(ws: obsws, source: str, name: str = 'Crop/Pad',
                              relative: bool = False,
                              left: int = 0, right: int = 0, top: int = 0, bottom: int = 0, ):
    settings = {
        'relative': relative,
        'x': left,
        'y': top,
        'cx': right,
        'cy': bottom,
        'top': top,
        'bottom': bottom,
        'left': left,
        'right': right
    }
    await add_filter(ws=ws, source=source, filter=name, type='crop_filter', settings=settings)


async def remove_crop_pad_filter(ws: obsws, source: str, name: str = 'Crop/Pad'):
    await remove_filter(ws=ws, source=source, filter=name)
