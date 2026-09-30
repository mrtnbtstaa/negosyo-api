from django.contrib.auth import get_user_model
from apps.users.selectors import UserSelector
from common.exceptions.api import ConflictException, NotFoundException
from common.constants.messages import Messages
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from apps.branches.models import BranchMember, Branch
from .models import Merchant, MerchantStaff, MerchantInvitation
from django.utils import timezone

from uuid import uuid4

from common.storage.storage_service import StorageService
from common.validators.files import ImageFileValidator
from common.constants.messages import Messages
from common.exceptions import NotFoundException

User = get_user_model()

class MerchantService:

    def __new__(cls):
        raise TypeError("MerchantService cannot be instantiated.")

    @classmethod
    def register_merchant_account(
        cls,
        full_name: str, 
        email: str,
        password: str
    ) -> None:
        
        if UserSelector.exists(email=email):
            raise ConflictException(
                errors={
                    "email": [Messages.CONFLICT]
                }
            )
            
        User.objects.create_user(
            full_name=full_name,
            email=email,
            password=password,
            account_type="owner"
        )
        
    @classmethod
    @transaction.atomic
    def create_business_information(
        cls,
        user: AbstractUser, 
        business_name: str,
        business_category: str,
        business_email: str,
        business_phone: str,
        branch_name: str,
        address: str,
        phone_number: str,
        operating_hours: dict,
    ) -> None:
        
        if not UserSelector.exists(email=user.email):
            raise ConflictException(
                errors={
                    "email": [Messages.NO_USER_FOUND]
                }
            )
            
        created_merchant = Merchant.objects.create(
            owner=user,
            business_name=business_name,
            business_category=business_category,
            business_email=business_email,
            business_phone=business_phone,
        )
      
        MerchantStaff.objects.create(
            merchant=created_merchant,
            user=user,
            role="owner"
        )
        
        Branch.objects.create(
            merchants=created_merchant,
            branch_name=branch_name,
            address=address,
            phone_number=phone_number,
            operating_hours=operating_hours
        )
        
        # BranchMember.objects.create(
        #     branch=created_branch,
        #     business_member=created_business_member
        # )
    
    @classmethod
    @transaction.atomic
    def complete_business_owner_onboarding(cls, user: AbstractUser):
                
        owner = getattr(user, "owned_business", None)
        
        if owner is None:
            raise NotFoundException(
                message="No owned business found."
            )
        
        user.onboarding_completed = True
        user.save(update_fields=["onboarding_completed"])
        
        owner.setup_completed = True
        owner.setup_completed_at = timezone.now()
        owner.save(
            update_fields=[
                "setup_completed",
                "setup_completed_at"
            ]
        )
        
class MerchantImageService:
    
    """
    Cloudinary storage service.

    Responsible only for uploading an profile.
    """
    def __new__(cls):
        raise TypeError("ProfileService cannot be instantiated.")

    @staticmethod
    def update_merchant_image(
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
    def upload_merchant_image(
        user,
        image
    ):

        ImageFileValidator()(image)
        
        # The generated public_id with a uuid to make the public id unique
        public_id = f"{user.id}/{uuid4()}"

        result = StorageService.upload(
            file=image,
            public_id=public_id,
            folder="merchants"
        )

        return result["public_id"]