from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class ContactForm(forms.Form):
	name = forms.CharField(max_length = 100,label = 'Name')
	email = forms.EmailField(required = False,label = 'EMail')
	subject = forms.CharField(max_length = 100)
	message = forms.CharField(widget = forms.Textarea)
	captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox(),error_messages = {'required': 'Please verify that you are not a robot.'})

class RegisterForm(UserCreationForm):
	captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox(),error_messages = {'required': 'Please verify that you are not a robot.'})