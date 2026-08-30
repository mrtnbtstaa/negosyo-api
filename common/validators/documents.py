from pathlib import Path

from docx import Document
from pypdf import PdfReader

from common.exceptions.api import ValidationException


class DocumentFileValidator:

    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Microsoft Compound File Binary Format signature.
    DOC_SIGNATURE = b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"

    def __call__(self, file) -> None:
        self.validate(file)

    def validate(self, file) -> None:
        self._validate_size(file)
        self._validate_mime_type(file)
        self._validate_extension(file)
        self._validate_file(file)

    def _validate_size(self, file) -> None:
        if file.size == 0:
            raise ValidationException(
                message="The uploaded file is empty."
            )

        if file.size > self.MAX_FILE_SIZE:
            raise ValidationException(
                message="The document must not exceed 10 MB."
            )

    def _validate_mime_type(self, file) -> None:
        content_type = getattr(file, "content_type", None)

        if content_type not in self.ALLOWED_MIME_TYPES:
            raise ValidationException(
                message="Unsupported document MIME type."
            )

    def _validate_extension(self, file) -> None:
        extension = Path(file.name).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValidationException(
                message="Unsupported document file extension."
            )

    def _validate_file(self, file) -> None:
        extension = Path(file.name).suffix.lower()

        if extension == ".pdf":
            self._validate_pdf(file)

        elif extension == ".docx":
            self._validate_docx(file)

        elif extension == ".doc":
            self._validate_doc(file)

    def _validate_pdf(self, file) -> None:
        try:
            file.seek(0)

            PdfReader(file)

        except Exception:
            raise ValidationException(
                message="The uploaded PDF file is invalid."
            )

        finally:
            file.seek(0)

    def _validate_docx(self, file) -> None:
        try:
            file.seek(0)

            Document(file)

        except Exception:
            raise ValidationException(
                message="The uploaded DOCX file is invalid."
            )

        finally:
            file.seek(0)

    def _validate_doc(self, file) -> None:
        try:
            file.seek(0)

            signature = file.read(len(self.DOC_SIGNATURE))

            if signature != self.DOC_SIGNATURE:
                raise ValidationException(
                    message="The uploaded DOC file is invalid."
                )

        except ValidationException:
            raise

        except Exception:
            raise ValidationException(
                message="The uploaded DOC file is invalid."
            )

        finally:
            file.seek(0)