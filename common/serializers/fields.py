from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from decimal import Decimal
from datetime import date
from uuid import UUID

class RequiredCharField(serializers.CharField):

    def __init__(self, *, label: str, **kwargs):

        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid string.",
                "min_length": f"{label} is too short.",
                "max_length": f"{label} is too long."
            }
        )

        super().__init__(**kwargs)
    
    def to_internal_value(self, data):
        
        if not isinstance(data, str):
            self.fail("invalid")
        
        return super().to_internal_value(data)

    def run_validation(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().run_validation(data)
    
    
class RequiredUUIDField(serializers.UUIDField):

    def __init__(self, *, label: str, **kwargs):

        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid uuid.",
            }
        )

        super().__init__(**kwargs)
    
    def to_internal_value(self, data):
        
        if not isinstance(data, UUID):
            self.fail("invalid")
        
        return super().to_internal_value(data)

    def run_validation(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().run_validation(data)


class RequiredEmailField(serializers.EmailField):

    def __init__(self, *, label: str, **kwargs):

        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid email address.",
                "min_length": f"{label} is too short.",
                "max_length": f"{label} is too long.",
            }
        )

        super().__init__(**kwargs)

    def run_validation(self, data):

        if isinstance(data, str):
            data = data.strip()

        return super().run_validation(data)


class RequiredIntegerField(serializers.IntegerField):

    def __init__(self, *, label: str, **kwargs):

        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid value.",
                "min_length": f"{label} is too short.",
                "max_length": f"{label} is too long.",
            }
        )

        super().__init__(**kwargs)
        
    def to_internal_value(self, data):
        
        if data == "" or data == None:
            self.fail("blank")
        
        # if not isinstance(data, int):
        #     self.fail("invalid")
        
        return super().to_internal_value(data)

    def run_validation(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().run_validation(data)

class RequiredDecimalField(serializers.DecimalField):

    def __init__(self, *, label: str, **kwargs):

        kwargs.setdefault("max_digits", 12)
        kwargs.setdefault("decimal_places", 2)

        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid value.",
                "min_length": f"{label} is too short.",
                "max_length": f"{label} is too long."
            }
        )

        super().__init__(**kwargs)

    # def to_internal_value(self, data):

    #     # If the value is not a decimal instance
    #     if not isinstance(data, Decimal):
    #         self.fail("invalid")

    #     return super().to_internal_value(data)
        
class RequiredImageField(serializers.ImageField):

    def __init__(self, label: str, **kwargs):
        
        kwargs.setdefault(
            "error_messages",
            {
                "invalid_image": f"{label} you uploaded was either not an image or a corrupted image."
            }
        )
        
        
        super().__init__(**kwargs)

class RequiredFloatField(serializers.FloatField):

    def __init__(self, *, label: str, min_value: int, max_value: int, **kwargs):
    
        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not valid number.",
                "min_value": f"Ensure {label} value is greater than or equal to {min_value}",
                "max_length": f"Ensure {label} value is less than or equal to {max_value}.",
                "overflow": f"{label} value too large to convert to float",
                "max_string_length": f"{label} value too large."
            }
        )

        super().__init__(
            min_value=min_value,
            max_value=max_value,
            **kwargs
        )
        
    def to_internal_value(self, data):
        
        if not isinstance(data, float):
            self.fail("invalid")
            
        return super().to_internal_value(data)


class RequiredFileField(serializers.FileField):

    def __init__(self, *, label: str, **kwargs):
        
        kwargs.setdefault(
            "error_messages",
            {
                "required": f"{label} file is required",
                "empty": f"{label} file is empty",
                "invalid": f"{label} was not a file. Check the encoding type on the form."
            }
        )

        super().__init__(
            **kwargs
        )


class RequiredDateField(serializers.DateField):

    def __init__(self, *, label: str, **kwargs):

        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid date format.",
                "datetime": f"{label} expected a date but got a datetime."
            }
        )

        super().__init__(**kwargs)
        
    def to_internal_value(self, value):
        
        if value == "" or value == None:
            self.fail("blank")
        
        # if not isinstance(value, date):
        #     self.fail("datetime")
        
        return super().to_internal_value(value)

    def run_validation(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().run_validation(data)


class RequiredPhoneNumber(PhoneNumberField):

    def __init__(self, *, label: str, **kwargs):
    
        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} not a valid phone number.",
                "min_length": f"{label} is too short.",
                "max_length": f"{label} is too long.",
            }
        )

        super().__init__(**kwargs)


class RequiredListField(serializers.ListField):

    def __init__(self, *, label: str, min_length: int, **kwargs):

        kwargs.setdefault("allow_empty", False)
        
        kwargs.setdefault(
            "error_messages",
            {
                "not_a_list": f"{label} Expected a list of items",
                "empty": f"{label} may not be empty",
                "invalid": f"{label} not a valid list.",
                "min_length": f"Ensure {label} field has at least {min_length} elements."
            }
        )

        super().__init__(
            min_length=min_length,
            **kwargs
        )
        
    def run_validation(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().run_validation(data)
        
class RequiredJsonField(serializers.JSONField):
    
    def __init__(self, label: str, **kwargs):
        
        kwargs.setdefault(
            "error_messages",
            {
                "invalid": f"{label} must be a valid JSON."
            }
        )
        
        super().__init__(
            **kwargs
        )
        
        
class RequiredTimeField(serializers.TimeField):

    def __init__(self, *, label: str, valid_format: str | None = None, **kwargs):
    
        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "invalid": f"{label} has wrong format. Use one of these formats instead: {valid_format}.",
            }
        )

        super().__init__(**kwargs)

    def to_internal_value(self, value):

        if value == "":
            self.fail("blank")

        return super().to_internal_value(value)

    def run_validation(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().run_validation(data)