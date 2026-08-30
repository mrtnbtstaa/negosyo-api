from __future__ import annotations
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from common.exceptions import ValidationException

class ImageFileValidator:
    """
    Validates uploaded image files.

    Checks:
    - File size
    - MIME type
    - File extension
    - Actual image format
    - Image dimensions
    """

    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    ALLOWED_FORMATS = {
        "JPEG",
        "PNG",
        "WEBP",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    MAX_WIDTH = 5000
    MAX_HEIGHT = 5000

    def __call__(self, file) -> None:
        self.validate(file)

    def validate(self, file) -> None:
        self._validate_size(file)
        self._validate_mime_type(file)
        self._validate_extension(file)
        self._validate_image(file)

    def _validate_size(self, file) -> None:
        if file.size == 0:
            raise ValidationException(
                message="The uploaded file is empty."
            )

        if file.size > self.MAX_FILE_SIZE:
            raise ValidationException(
                message="The image must not exceed 5 MB."
            )

    def _validate_mime_type(self, file) -> None:

        content_type = getattr(
            file,
            "content_type",
            None,
        )

        if content_type not in self.ALLOWED_MIME_TYPES:
            raise ValidationException(
                message="Unsupported image MIME type."
            )

    def _validate_extension(self, file) -> None:

        extension = Path(file.name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValidationException(
                message="Unsupported image file extension."
            )

    def _validate_image(self, file) -> None:
        
        try:
            file.seek(0)

            image = Image.open(file)

            # Verify the image is actually valid.
            image.verify()

            file.seek(0)

            # Re-open because verify() invalidates the image object.
            image = Image.open(file)

            if image.format not in self.ALLOWED_FORMATS:
                raise ValidationException(
                    message="The actual image format is not supported."
                )

            width, height = image.size

            if not (
                self.MIN_WIDTH <= width <= self.MAX_WIDTH
                and self.MIN_HEIGHT <= height <= self.MAX_HEIGHT
            ):
                raise ValidationException(
                    message="Image dimensions are outside the allowed range."
                )

        except (UnidentifiedImageError, OSError):
            raise ValidationException(
                message="The uploaded file is not a valid image."
            )

        finally:
            file.seek(0)