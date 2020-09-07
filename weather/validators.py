from django.core.exceptions import ValidationError

# Model level validation.
def validate_file_extension(value):
    if not value.name.lower().endswith('.csv'):
        raise ValidationError(value.name.split('.')[1]+' is not a supported file extension. Please use .csv')