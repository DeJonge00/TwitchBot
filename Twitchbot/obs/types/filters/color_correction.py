from simpleobsws import obsws

from obs.types.filter import add_filter, remove_filter


async def add_color_correction_filter(ws: obsws, source: str, gamma=0, contrast=0, brightness=0, saturation=0,
                                      hue_shift=0, opacity=100, color=None, name: str = 'Color Correction'):
    settings = {
        'gamma': gamma,
        'contrast': contrast,
        'brightness': brightness,
        'saturation': saturation,
        'hue_shift': hue_shift,
        'opacity': opacity,
        'color': color
    }
    await add_filter(ws=ws, source=source, filter=name, type='color_filter', settings=settings)


async def remove_color_correction_filter(ws: obsws, source: str, name: str = 'Color Correction'):
    await remove_filter(ws=ws, source=source, filter=name)
