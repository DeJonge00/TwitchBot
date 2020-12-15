from simpleobsws import obsws


async def set_scene(ws: obsws, scene: str):
    r = await ws.call(
        'SetCurrentScene',
        {
            'scene-name': scene
        }
    )
    print("Scene changed to '{}'\nResponse: {}".format(scene, r))


async def get_curent_scene(ws: obsws) -> str:
    r = await ws.call(
        'GetCurrentScene'
    )
    print("Get current scene\nResponse: {}".format(r))
    return r
