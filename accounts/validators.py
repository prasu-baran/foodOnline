from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension with the leading dot
    print(ext)  # Debugging purposes; remove this in production
    valid_extensions = ['.png', '.jpeg', '.jpg']  # Include the leading dot in extensions
    if ext.lower() not in valid_extensions:  # Perform the comparison correctly
        raise ValidationError(f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}')