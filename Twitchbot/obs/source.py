from simpleobsws import obsws


async def get_source_settings(ws: obsws, source: str, type: str = None):
    print(ws)
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
