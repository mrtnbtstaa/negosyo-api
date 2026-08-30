from __future__ import annotations

from typing import Any

import cloudinary
import cloudinary.uploader
import cloudinary.api

class StorageService:

    """
    Cloudinary storage service.

    Responsible only for interacting with Cloudinary.
    """

    def __new__(cls):
        raise TypeError("ProfileService cannot be instantiated.")

    @staticmethod
    def upload(
        *,
        file: Any,
        public_id: str,
        folder: str | None = "images",
        resource_type: str = "image",
    ) -> dict[str, Any]:
        """
        Upload a file to Cloudinary.
        """

        result = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            folder=folder,
            resource_type=resource_type,
            overwrite=False,
        )

        return {
            "public_id": result["public_id"],
            # "url": result.get("url"),
            # "secure_url": result.get("secure_url"),
            # "resource_type": result.get("resource_type"),
            # "format": result.get("format"),
            "bytes": result.get("bytes"),
            # "width": result.get("width"),
            # "height": result.get("height"),
        }

    @staticmethod
    def delete(
        *,
        public_id: str,
        resource_type: str = "image",
        type: str = "upload",
    ) -> None:
        """
        Delete an object from Cloudinary.
        """

        cloudinary.uploader.destroy(
            public_id,
            resource_type=resource_type,
            type=type,
        )

    @staticmethod
    def exists(
        *,
        public_id: str,
        resource_type: str = "image",
    ) -> bool:
        """
        Check whether an object exists.
        """

        try:
            cloudinary.api.resource(
                public_id,
                resource_type=resource_type,
            )

            return True

        except cloudinary.exceptions.NotFound:
            return False

    @staticmethod
    def get_url(
        *,
        public_id: str,
        secure: bool = True,
    ) -> str:
        """
        Generate a Cloudinary URL.
        """

        url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            secure=secure,
        )

        return url