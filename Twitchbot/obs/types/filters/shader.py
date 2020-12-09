from simpleobsws import obsws

from obs.types.filter import add_filter, remove_filter
from secret.secrets import user_defined_shader_folder


async def add_shader_filter(ws: obsws, source: str, shader: str, name: str = 'User-defined-shader'):
    settings = {
        'from_file': True,
        'shader_file_name': user_defined_shader_folder + shader
    }
    await add_filter(ws=ws, source=source, filter=name, type='shader_filter', settings=settings)


async def remove_shader_filter(ws: obsws, source: str, name: str = 'User-defined-shader'):
    await remove_filter(ws=ws, source=source, filter=name)
