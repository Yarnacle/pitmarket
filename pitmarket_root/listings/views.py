from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Listing
from .forms import ListingForm,DeleteListingForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ListingList(ListView):
	template_name = 'listings/listing-list.html'
	model = Listing
	context_object_name = 'all_listings'
	ordering = '-list_date'
	paginate_by = 100

	def post(self,request):
		tags = request.POST.get('tags')
		if tags:
			return HttpResponseRedirect('/?filter=' + request.POST.get('tags'))
		else:
			return HttpResponseRedirect('/')

	def get_queryset(self):
		queryset = Listing.objects.all()
		filter = self.request.GET.get('filter',None)
		if filter:
			filter = filter.split(',')
			queryset = queryset.filter(tags__name__in=filter).distinct()
		return queryset.order_by(self.ordering)

	def get_context_data(self,**kwargs):
		context = super(ListingList,self).get_context_data(**kwargs)
		filter = self.request.GET.get('filter')
		if (filter):
			context['filter'] = ','.join(self.request.GET.get('filter',None).split(','))
		return context

class ListingView(DetailView):
	template_name = 'listings/listing_detail.html'
	model = Listing
	context_object_name = 'listing'

	def get_context_data(self,**kwargs):
		context = super(ListingView,self).get_context_data(**kwargs)
		if 'my-listings' in self.request.path_info:
			context['back'] = 'my-listings'
			context['current'] = 'my-listing-list'
		if self.request.GET.get('filter'):
			context['filter'] = self.request.GET.get('filter')
		if self.request.GET.get('page'):
			context['page_number'] = int(self.request.GET.get('page'))
		return context

class MyListingList(LoginRequiredMixin,ListingList):
	login_url = reverse_lazy('login')
	template_name = 'listings/my_listing_list.html'
	model = Listing
	context_object_name = 'my_listings'
	ordering = '-list_date'
	paginate_by = 100

	def post(self,request):
		form = DeleteListingForm(request.POST,user = request.user)
		if form.is_valid():
			Listing.objects.filter(pk__in=request.POST.getlist('listings')).delete()
		return HttpResponseRedirect('/my-listings/')

	def get_context_data(self,**kwargs):
		context = super(MyListingList,self).get_context_data(**kwargs)
		context['current'] = 'my-listing-list'
		return context
	
	def get_queryset(self):
		return Listing.objects.filter(username = self.request.user).order_by(self.ordering)

@login_required(login_url = reverse_lazy('login'))
def listing_req(request):
	submitted = False
	if request.method == 'POST':
		form = ListingForm(request.POST,request.FILES)
		if form.is_valid():
			form.instance.username = request.user
			form.save()
			return HttpResponseRedirect('/sell/?submitted=True')
	else:
		form = ListingForm()
		if 'submitted' in request.GET:
			submitted = True
	context = {
		'form': form,
		'submitted': submitted,
		'current': 'sell'
	}
	return render(request,'listings/make_listing_form.html',context)
