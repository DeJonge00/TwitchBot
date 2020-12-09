from simpleobsws import obsws


async def set_scene(ws: obsws, scene: str):
    r = await ws.call(
        'SetCurrentScene',
        {
            'scene-name': scene
        }
    )
    print("Scene changed to '{}'\nResponse: {}".format(scene, r))
