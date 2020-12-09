from simpleobsws import obsws


async def add_scene_item(ws: obsws, source: str, scene: str, visible: bool = True):
    r = await ws.call(
        'AddSceneItem',
        {
            'sourceName': source,
            'sceneName': scene,
            'setVisible': visible
        }
    )
    print("Add source '{}' to scene '{}'\nResponse: {}".format(source, scene, r))
