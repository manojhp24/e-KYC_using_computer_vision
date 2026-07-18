from pathlib import Path
from uuid import uuid4
from werkzeug.datastructures import FileStorage


class UploadService:

    def save_file(self, file: FileStorage,folder:str) -> str:
        if not file.filename:
            raise ValueError("No file selected or filename is empty")

        upload_directory = Path(f"uploads/{folder}")

        upload_directory.mkdir(
            parents=True,
            exist_ok=True
        )
        extension = Path(file.filename).suffix

        filename = f"{uuid4()}{extension}"

        file_path = upload_directory / filename

        file.save(file_path)

        return str(file_path)