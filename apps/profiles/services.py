from uuid import uuid4

from common.storage.storage_service import StorageService
from common.validators.files import ImageFileValidator
from common.constants.messages import Messages
from .models import Profile
from common.exceptions import NotFoundException

class ProfileService:
    
    """
    Cloudinary storage service.

    Responsible only for uploading an profile.
    """
    def __new__(cls):
        raise TypeError("ProfileService cannot be instantiated.")

    @staticmethod
    def update_profile(
        user,
        image,
    ):
        ImageFileValidator()(image)

        # Safely access the profile
        profile = getattr(user, "user_profile", None)

        if profile is None:
            raise NotFoundException(
                message=Messages.NOT_FOUND
            )

        result = StorageService.upload(
            file=image,
            public_id=profile.profile_public_id,
        )

        # Delete previous avatar after successful upload.
        if profile.profile_public_id:
            StorageService.delete(
                public_id=profile.profile_public_id,
            )

        profile.profile_public_id = result["public_id"]
        profile.profile_size = result["bytes"]
        profile.profile_content_type = image.content_type
        profile.profile_name = getattr(image, "name", None).split(".")[0]

        profile.save(
            update_fields=[
                "profile_public_id",
                "profile_size",
                "profile_content_type",
                "profile_name"
            ],
        )

        return profile

    @staticmethod
    def create_profile(
        user,
        image
    ):

        ImageFileValidator()(image)
        
        # The generated public_id with a uuid to make the public id unique
        public_id = f"profiles/{user.id}/avatar/{uuid4()}"

        result = StorageService.upload(
            file=image,
            public_id=public_id,
        )

        profile = Profile.create_profile(
            user=user,
            profile_public_id=result["public_id"],
            profile_size=result["bytes"],
            profile_content_type=image.content_type,
            profile_name=getattr(image, "name", None).split(".")[0]
        )

        return profile