from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Event,Invitee,Attendee
from django.contrib.auth.models import User
from .forms import EventForm

def home(request):
	obj=Event.objects.all()
	context = {
        'obj': obj,
    }
	return render(request,'home.html',context)


def event(request,event_id):
	eve = Event.objects.get(pk=event_id)
	i   = eve.invitee_set.all()
	context = {'eve' : eve, 'i' : i}
	return render(request,'event.html',context)

def event_detail(request,event_id):
	eve = Event.objects.get(pk=event_id)
	i   = eve.invitee_set.all()
	u   = request.user.username
	t   = User.objects.get(username=u)
	context = {'eve' : eve , 'i' : i}
	if eve.attendee_set.filter(name__username=u).count() :
		return render(request,'event_unregister.html',context)
	else:
		return render(request,'event_register.html',context)


def event_delete(request,event_id):
	eve = Event.objects.get(pk=event_id)
	e   =Event.objects.filter(id=event_id)
	if e.count() :
		e.delete()
	#gives error if event has already been deleted or does not exist
	return HttpResponse("event created by you whose name was %s , has been deleted" %eve.name)

def event_register(request,event_id):
	eve  = Event.objects.get(pk=event_id)
	u    = request.user.username
	t    = User.objects.get(username=u)

	obj  = Event.objects.all()
	ob   = Event.objects.filter(creator__username=u)
	i1   = Invitee.objects.filter(name__username=u)
	if i1.count() !=0:
		i    = i1[0].event.all()		
	else:
		i = 'none'

	if eve.limit_of_guests!=0 and eve.limit_of_guests < eve.attendee_set.count()+1:
		return HttpResponse("Sorry cannot register for event, limit exceeded")
	attobj= Attendee.objects.filter(name__username=u)
	if attobj.count():
		a = attobj[0].event.all() 	
		#logged in user ke saare events ki date current event ki date se match kro
		for i in a:
			if eve.date == i.date :
				return HttpResponse("Sorry cannot register for event")

	if ((eve.attendee_set.filter(name__username=u).count())==0):
		a=Attendee()
		a.name=t
		a.save()
		eve.attendee_set.add(a) 
	context = {
	'u'  : u,
	'obj': obj,
	'ob' : ob,		   	 		   
	'i'  : i
	}
	return render(request,'profile.html',context)

def event_unregister(request,event_id):
	eve = Event.objects.get(pk=event_id)
	u   = request.user.username
	t   = User.objects.get(username=u)
	e   = eve.attendee_set.filter(name__username=u)

	obj  = Event.objects.all()
	ob   = Event.objects.filter(creator__username=t.username)
	i1   = Invitee.objects.filter(name__username=t.username)
	if i1.count() !=0:
		i    = i1[0].event.all()
	else:
		i = 'none'
	if e.count(): 
		e.delete()
	context = {
	'u'  : u,
	'obj': obj,
	'ob' : ob,		   	 		   
	'i'  : i
	}
	return render(request,'profile.html',context)

def profile(request):
#request.user is User model object.
#request.user.FIELDNAME will allow you 
#to access all the fields of the user model
	u    = request.user.username
	obj  = Event.objects.all()
	t    = User.objects.get(username=u)
	ob   = Event.objects.filter(creator__username=t.username)
	#gives error if user has not been invited to any event

	i1   = Invitee.objects.filter(name__username=t.username)
	if i1.count() !=0:
		i    = i1[0].event.all()
	else:
		i = 'none'
	context = {
			   'u' : u,
			   'obj': obj,
			   'ob'	: ob,		   	 		   
	 		   'i': i
	 		   }
	return render(request,'profile.html',context)

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def form(request):
	#submitbutton= request.POST.get("submit")
	context = {}
	if request.method == 'POST':
		form    = EventForm(request.POST or None, request.FILES or None)
		form.creator = request.user
		if form.is_valid() :
			instance = form.save(commit=False)
			instance.creator = request.user
			instance.save()
			return redirect('profile')
	else:
		form = EventForm()

	context['form']=form
	return render(request,'form.html',context)

# same name same eventname same date not possible;
# user apne event mei khud register nahi kar skta

# Django will complain if more than one item matches 
# the get() query. In this case, it will raise MultipleObjectsReturned,
# which again is an attribute of the model class itself.
#----------------------------------------------------------------------
# class Author(models.Model):
#     author_name = models.CharField(max_length=50, default='unknown')
# class Quote(models.Model):
#     author = models.ForeignKey(Author)
# Quote.objects.filter(author__author_name=name)
# Quote.objects.filter(author=name)-->this gives error:
# invalid literal for int() with base 10
#----------------------------------------------------------------------
# FLAWS IN THIS PROJECT:
# * User shouldn't be allowed to register in its own event.
# * While registering an event, user should be allowed to add invitees
# * Same name aur same date aur same user ke multiple events nahi ho sakte. check for that.
