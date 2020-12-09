from simpleobsws import obsws


async def get_source_settings(ws: obsws, source: str, type: str = None):
    r = await ws.call(
        'GetSourceSettings',
        {
            'sourceName': source,
            'sourceType': type
        }
    )
    print("Get source settings\nResponse: {}\n".format(r))
    s = r.get('sourceSettings')
    if s:
        return s
    return False


async def set_source_settings(ws: obsws, source: str, type: str, settings: dict):
    await ws.call(
        'SetSourceSettings',
        {
            'sourceName': source,
            'sourceType': type,
            'sourceSettings': settings
        }
    )


async def set_source_location(ws: obsws, source: str, x: int = 0, y: int = 0):
    r = await ws.call(
        'SetSourceSettings',
        {
            'sourceName': source,
            'sourceSettings': {
                'left': 100
            }
        }
    )
    print("Set source location for '{}'\nResponse: {}".format(source, r))
