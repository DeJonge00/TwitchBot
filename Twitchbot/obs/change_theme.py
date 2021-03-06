from asyncio import sleep
from re import match

from simpleobsws import obsws

from obs.constants import COLOR_RAINBOW, COLOR_RED, color_to_int, COLOR_GREEN, COLOR_PINK
from obs.types.filters.color_grading import remove_color_grading_filter, add_color_grading_filter
from obs.types.source import get_source_settings, set_source_settings


async def set_browser_source_url(ws: obsws, source: str, url: str):
    await set_source_settings(ws, source, 'browser_source', {'url': url})


def replace_type(url: str, type: str, new: str):
    m = match('.*(' + type + '=.*?)&.*', url)
    if not m:
        return url
    return url.replace(m.groups()[0], type + '=' + new)


async def change_border_type(ws: obsws, source: str, type: str):
    settings = await get_source_settings(ws, source=source)
    if not settings:
        return False
    await set_browser_source_url(ws, source, replace_type(settings.get('url'), 'gradientType', type))


async def change_border_color(ws: obsws, source: str, gradient_type='fadeToWhite', hue=226, hue_offset=90,
                              brightness=58):
    settings = await get_source_settings(ws, source=source)
    if not settings:
        return False
    url = settings.get('url')
    for key, value in [('gradientType', gradient_type),
                       ('hue', str(hue)),
                       ('hueOffset', str(hue_offset)),
                       ('brightness', str(brightness))]:
        if not (key == 'hueOffset' and gradient_type == 'fadeToWhite') \
                and not (gradient_type == 'rainbow' and key != 'gradientType'):
            url = replace_type(url, key, value)
    await set_browser_source_url(ws, source, url)


async def change_audio_visualizer_color(ws: obsws, source: str, color: int = 4294949411):
    # 35  186  255
    await set_source_settings(ws, source, 'spectralizer', {'color': color})


async def change_label_text_color(ws: obsws, source: str, color: int = 4294922496):
    await set_source_settings(ws, source, 'text_gdiplus_v2', {
        'color': color
    })


async def change_theme(ws: obsws, color: str):
    # 'Fullscreen Border',
    border_sources = ['Webcam Border', 'Webcam Border Discord', 'Handcam Border']
    av_sources = ['Audio Visualizer', 'Audio Visualizer (Chatting)']
    label_sources = ['StreamerName', 'Just Chatting Label', 'TransitionLabel', 'AnnouncementLabel']
    browser_sources = ['Infographic', 'Transition Widget']
    if color == COLOR_RAINBOW:
        border_color_settings = {'gradient_type': 'rainbow'}
        widget_color_settings = {'blue': 100, 'all': 20}
    elif color == COLOR_RED:
        border_color_settings = {'gradient_type': 'twoTone', 'hue': 0, 'brightness': 67, 'hue_offset': 35}
        widget_color_settings = {'red': 100}
    elif color == COLOR_GREEN:
        border_color_settings = {'gradient_type': 'twoTone', 'hue': 130, 'brightness': 60, 'hue_offset': 40}
        widget_color_settings = {'green': 100, 'all': 40}
    elif color == COLOR_PINK:
        border_color_settings = {'gradient_type': 'fadeToWhite', 'hue': 300, 'brightness': 65}
        widget_color_settings = {'red': 100, 'blue': 100, 'all': 40}
    else:
        # color == COLOR_BLUE:
        border_color_settings = {}
        widget_color_settings = {'blue': 100, 'all': 20}

    for source in border_sources:
        await change_border_color(ws, source, **border_color_settings)
    for source in av_sources:
        await change_audio_visualizer_color(ws, source, color_to_int.get(color))
    for source in label_sources:
        await change_label_text_color(ws, source, color_to_int.get(color))
    for source in browser_sources:
        await remove_color_grading_filter(ws, source)
        await add_color_grading_filter(ws, source, **widget_color_settings)


async def test_border_type(ws: obsws, source: str):
    await change_border_type(ws, source, 'rainbow')
    await sleep(2)
    await change_border_type(ws, source, 'twoTone')
    await sleep(2)
    await change_border_type(ws, source, 'fadeToWhite')
