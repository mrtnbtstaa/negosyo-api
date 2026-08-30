from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

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


class RequiredFloatField(serializers.FloatField):

    def __init__(self, *, label: str, min_value: int, max_value: int, **kwargs):
    
        kwargs.setdefault(
            "error_messages",
            {
                "blank": f"{label} cannot be blank",
                "required": f"{label} is required",
                "invalid": f"{label} valid number is required.",
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


class RequiredFileField(serializers.FileField):

    def __init__(self, *, label: str, **kwargs):
        
        kwargs.setdefault(
            "error_messages",
            {
                "required": f"{label} file is required",
                "empty": f"{label} file is empty"
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
                "min_length": f"{label} is too short.",
                "max_length": f"{label} is too long.",
            }
        )

        super().__init__(**kwargs)

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
                "invalid": f"{label} not a valid email address.",
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