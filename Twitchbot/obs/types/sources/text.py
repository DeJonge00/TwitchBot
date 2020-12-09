from simpleobsws import obsws

from secret.secrets import default_font


async def set_text_properties(ws: obsws, source: str,
                              font_face: str = default_font,
                              font_size: int = 24,
                              outline: bool = False,
                              text='text',
                              align: str='left'):
    r = await ws.call(
        'SetSourceSettings',
        {
            'sourceName': source,
            'sourceType': 'text_gdiplus_v2',
            'sourceSettings': {
                'align': align,
                'font': {
                    'face': font_face,
                    'size': font_size
                },
                'outline': outline,
                'text': text
            }
        })
    print("Set text properties of '{}'\nResponse: {}".format(source, r))


async def change_text(ws: obsws, source: str, text: str):
    r = await ws.call(
        'SetSourceSettings',
        {
            'sourceName': source,
            'sourceType': 'text_gdiplus_v2',
            'sourceSettings': {
                'text': text
            }
        })
    print("Set text of '{}'\nResponse: {}".format(source, r))
