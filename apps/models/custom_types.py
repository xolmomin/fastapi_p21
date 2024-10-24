import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from PIL import Image, UnidentifiedImageError
from fastapi_storages import StorageImage
from fastapi_storages.exceptions import ValidationException
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import Dialect


class CustomImageType(ImageType):

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value
        if len(value.file.read(1)) != 1:
            return None

        try:
            image_file = Image.open(value.file)
            image_file.verify()
        except UnidentifiedImageError:
            raise ValidationException("Invalid image file")

        path = datetime.today().strftime(self.storage._path)
        Path(os.path.join(self.storage.MEDIA_URL, path)).mkdir(parents=True, exist_ok=True)

        image = StorageImage(
            name=os.path.join(path, value.filename),
            storage=self.storage,
            height=image_file.height,
            width=image_file.width,
        )
        image.write(file=value.file)

        image_file.close()
        value.file.close()
        return os.path.join(path, value.filename)

    def process_result_value(
            self, value: Any, dialect: Dialect
    ) -> Optional[StorageImage]:
        if value is None:
            return value

        with Image.open(value) as image:
            return StorageImage(
                name=value, storage=self.storage, height=image.height, width=image.width
            )
