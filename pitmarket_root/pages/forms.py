from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
class RegisterForm(UserCreationForm):
	captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox(),error_messages = {'required': 'Please verify that you are not a robot.'})