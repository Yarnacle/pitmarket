from django import forms
from django.forms import ModelForm
from .models import Listing

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = ['item','price','tags','description','contact','image']

class DeleteListingForm(forms.Form):
	listings = forms.MultipleChoiceField(
      widget  = forms.CheckboxSelectMultiple,
		required = False
    )

	def __init__(self,*args,**kwargs):
		user = kwargs.pop('user')
		super(DeleteListingForm, self).__init__(*args, **kwargs)
		self.fields['listings'].choices = [(listing.id,listing) for listing in Listing.objects.filter(username = user)]