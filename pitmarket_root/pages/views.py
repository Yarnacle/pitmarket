from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from .forms import ContactForm,RegisterForm
from .models import BlogPost
import smtplib as smtp
from urllib import parse
from django.views.generic.edit import CreateView
from django.views.generic import View,TemplateView
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

def blog(request,postname = ''):
	if postname:
		post = BlogPost.objects.get(title__iexact = parse.unquote(postname))
		context = {
			'title': post.title,
			'content': post.content,
			'upload_date': post.upload_date,
			'current': 'blog'
		}
		return render(request,'pages/post.html',context)
	else:
		context = {
			'post_list': BlogPost.objects.all().order_by('-upload_date'),
			'current': 'blog'
		}
		return render(request,'pages/blog.html',context)

def contact(request):
	submitted = False
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			connection = smtp.SMTP_SSL('smtp.gmail.com', 465)
			email_addr = env('EMAIL')
			email_pass = env('EMAIL_KEY')
			connection.login(email_addr,email_pass)
			connection.sendmail(
				from_addr = email_addr,
				to_addrs = email_addr,
				msg = f'Subject: [Pit Market Contact Submission] {cd["subject"]}\n\n{cd["message"]}\n\n-{cd["name"]} ({cd["email"]})'
			)
			connection.close()
			return HttpResponseRedirect('/contact/?submitted=true')
	else:
		form = ContactForm()
		if 'submitted' in request.GET:
			submitted = True
	context = {
		'form': form,
		'submitted': submitted,
		'current': 'contact'
	}
	return render(request,'pages/contact.html',context)
	
def login(request):
	context = {
		'next': request.GET.get('next')
	}
	return render(request,'registration/login.html',context)

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