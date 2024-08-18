import aiofiles
from aiohttp.web_request import Request

from feachers.DTO.file_path import FilePath
from feachers.custom_exceptions.file_type_exception import FileTypeException


class RequestFileWriter:
    BASE_DIRECTORY = "C:/Users/modecstap/Desktop/lt"

    def __init__(self, request: Request):
        self.field = None
        self.file_path = None
        self.request = request

    async def write(self) -> None:
        self.field = await self._read_field()
        self._check_file_type()
        self.file_path = FilePath(file_directory=self.BASE_DIRECTORY, filename=self.field.filename)
        await self._write_litematic_file()

    async def _write_litematic_file(self):
        async with aiofiles.open(self.file_path.get_file_path(), 'wb') as f:
            while True:
                chunk = await self.field.read_chunk()  # 8192 байт по умолчанию.
                if not chunk:
                    break
                await f.write(chunk)

    async def _read_field(self):
        reader = await self.request.multipart()
        return await reader.next()

    def _check_file_type(self):
        if not self.field.filename.endswith(".litematic"):
            raise FileTypeException("Invalid file type. Expected .litematic")
