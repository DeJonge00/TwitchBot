from simpleobsws import obsws

from obs.types.filter import add_filter, remove_filter


async def add_color_grading_filter(ws: obsws, source: str,
                                   green: int = 0, blue: int = 0, red: int = 0, all: int = 0,
                                   name: str = 'Color Grading'):
    settings = {
        'Filter.ColorGrade.Lift.Blue': blue,
        'Filter.ColorGrade.Lift.Green': green,
        'Filter.ColorGrade.Lift.Red': red,
        'Filter.ColorGrade.Lift.All': all
    }
    await add_filter(ws=ws, source=source, filter=name, type='streamfx-filter-color-grade', settings=settings)


async def remove_color_grading_filter(ws: obsws, source: str, name: str = 'Color Grading'):
    await remove_filter(ws=ws, source=source, filter=name)
