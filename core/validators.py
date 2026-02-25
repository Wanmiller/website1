from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

ALLOWED_IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
MAX_UPLOAD_SIZE_BYTES = 3 * 1024 * 1024

image_extension_validator = FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)


def validate_file_size(value):
    file_obj = getattr(value, "file", value)
    size = getattr(file_obj, "size", None)
    if size is None:
        return
    if size > MAX_UPLOAD_SIZE_BYTES:
        raise ValidationError(_("File size must be less than or equal to 3MB."))
