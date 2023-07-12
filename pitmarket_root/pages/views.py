from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import RegisterForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from . import config
import defender
from decouple import config as env

class Register(CreateView):
	template_name = 'registration/register.html'
	form_class = RegisterForm
	success_url = reverse_lazy('register-success')
	
	def form_valid(self,form):
		form.save()
		return HttpResponseRedirect(self.success_url + '?next=' + self.request.POST.get('next'))

	def get_context_data(self,**kwargs):
		context = super(Register,self).get_context_data(**kwargs)
		next = self.request.GET.get('next')
		context['next'] = next if next is not None else ''
		return context

class RegisterSuccess(TemplateView):
	template_name = 'registration/success.html'

	def get_context_data(self,**kwargs):
		context = super(RegisterSuccess,self).get_context_data(**kwargs)
		context['next'] = self.request.GET.get('next')
		return context

class LoginView(LoginView):
	template_name = 'registration/login.html'

def login(request):
	context = {
		'next': request.GET.get('next')
	}
	return render(request,'registration/login.html',context)

def credit(request):
	context = {
		'current': 'credit'
	}
	return render(request,'pages/credit.html', context)


def lockout_response(request):
	''' if we are locked out, here is the response '''
	if config.LOCKOUT_TEMPLATE:
		context = {
         'cooloff_time_seconds': config.COOLOFF_TIME,
         'cooloff_time_minutes': config.COOLOFF_TIME / 60,
         'failure_limit': config.FAILURE_LIMIT,
			'next': request.GET.get('next')
      }
		return render(request, config.LOCKOUT_TEMPLATE, context)
	if config.LOCKOUT_URL:
		return HttpResponseRedirect(config.LOCKOUT_URL)
	
	if config.COOLOFF_TIME:
		return HttpResponse(
   		'Account locked: too many login attempts.  ' 'Please try again later.'
      )
	else:
		return HttpResponse(
         'Account locked: too many login attempts.  '
         'Contact an admin to unlock your account.'
      )

defender.utils.lockout_response = lockout_response