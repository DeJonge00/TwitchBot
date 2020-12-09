from simpleobsws import obsws


async def get_source_filters(ws: obsws, source: str):
    r = await ws.call(
        'GetSourceFilters',
        {
            'sourceName': source
        }
    )
    if r.get('filters'):
        print("Get source filters\nFilters:\n{}".format('\n'.join([str(x) for x in r.get('filters')])))
        return
    print("Get source filters\nResponse: {}\n".format(r))


async def add_filter(ws: obsws, source: str, filter: str, type: str, settings: dict):
    r = await ws.call(
        'AddFilterToSource',
        {
            'sourceName': source,
            'filterName': filter,
            'filterType': type,
            'filterSettings': settings
        }
    )
    print("Added '{}' to '{}'\nResponse: {}\n".format(filter, source, r))


async def remove_filter(ws: obsws, source: str, filter: str):
    r = await ws.call(
        'RemoveFilterFromSource',
        {
            'sourceName': source,
            'filterName': filter
        }
    )
    print("Removed '{}' from '{}'\nResponse: {}\n".format(filter, source, r))
