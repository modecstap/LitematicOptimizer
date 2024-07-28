import aiofiles
from aiohttp import web
from aiohttp.web_request import Request

from utils.litematic_optimizer import LitematicOptimizer


async def get_optimized_litematic(request: Request):
    try:
        file_storage_path = "C:/Users/modecstap/Desktop/lt"
        reader = await request.multipart()

        field = await reader.next()
        filename = field.filename
        file_path = f"{file_storage_path}/{filename}"

        async with aiofiles.open(file_path, 'wb') as f:
            while True:
                chunk = await field.read_chunk()  # 8192 байт по умолчанию.
                if not chunk:
                    break
                await f.write(chunk)

        litematic_optimizer = LitematicOptimizer(file_path)
        litematic_optimizer.optimize()
        optimized_file_path = litematic_optimizer.save_optimized_schematic(file_storage_path, filename)

        async with aiofiles.open(optimized_file_path, 'rb') as f:
            optimized_file = await f.read()

        return web.Response(
            body=optimized_file,
            content_type='application/octet-stream'
        )

    except Exception as e:
        print(e)
        return web.Response(
            status=500,
            text="ошибка при обработке файла"
        )
