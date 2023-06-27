from django.core.exceptions import ValidationError

def validate_file_size(file):
	if file.size > 2 * 1024 * 1024:
		raise ValidationError('The maximum file size that can be uploaded is 2MB')
	else:
		return file