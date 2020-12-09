from asyncio import sleep
from random import randint

from simpleobsws import obsws

from obs.types.filters.crop_pad import add_crop_pad_filter, remove_crop_pad_filter
from obs.types.filters.scroll import remove_scroll_filter, add_scroll_filter
from obs.types.source import set_source_location
from obs.types.sources.text import set_text_properties, change_text


async def setup_scrolling_announcement(ws: obsws, source='testannouncement'):
    await set_text_properties(ws, source=source, font_size=50, align='right')
    await remove_crop_pad_filter(ws, source=source)
    await add_crop_pad_filter(ws, source=source, relative=True, left=-1920, right=-6000)


async def scrolling_announcement(ws: obsws, source='testannouncement', text='announcement'):
    await remove_scroll_filter(ws, source=source)
    # await set_source_location(ws, source, -200, randint(0, 1030))
    await change_text(ws, source, text)
    await add_scroll_filter(ws, source=source, speed_x=250)
