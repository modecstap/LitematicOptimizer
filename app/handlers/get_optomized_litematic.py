import logging

import aiofiles
from aiohttp import web
from aiohttp.web_request import Request

from app.request_file_writer import RequestFileWriter
from feachers.DTO import FilePath
from feachers.custom_exceptions import FileTypeException
from utils.litematic_optimizer import LitematicOptimizer

async def get_optimized_litematic(request: Request):
    logger = logging.getLogger(__name__)
    try:
        file_path = await _write_file(request)

        logger.info(f"Старт оптимизации {file_path.get_filename()}")

        optimized_file = await _optimize_file(file_path)

        return web.Response(
            body=optimized_file,
            content_type='application/octet-stream'
        )

    except FileTypeException as e:
        logger.exception(f"File type error: {e}")
        return web.Response(
            status=406,
            text="Проверьте формат файла, он должен быть .litematic"
        )

    except Exception as e:
        logger.exception(f"Processing error: {e}")
        return web.Response(
            status=500,
            text="Ошибка при обработке файла"
        )


async def _write_file(request: Request) -> FilePath:
    request_file_writer = RequestFileWriter(request)
    await request_file_writer.write()
    return request_file_writer.file_path


async def _optimize_file(file_path: FilePath) -> bytes:
    litematic_optimizer = LitematicOptimizer(file_path.get_file_path())
    litematic_optimizer.optimize()

    optimized_file_path = litematic_optimizer.save_optimized_schematic(
        file_path.get_file_directory(),
        file_path.get_filename()
    )

    async with aiofiles.open(optimized_file_path, 'rb') as f:
        return await f.read()
