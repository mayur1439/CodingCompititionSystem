from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from Profile.models import Profile_det
from django.contrib import messages
from django.template.context_processors import csrf
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from Home_Module.templates import *
from Home_Module.views import *
from Profile.forms import *

@login_required(login_url='/Login/')
def home(request):
	try:
		c={}
		c.update(csrf(request))
		cur_time=datetime.now()
		cur_time=cur_time.replace(year=2050)
		challenge=compete_details.objects.filter(challenge_status='future')
		for ch in challenge:
			s_time=ch.start_time
			e_time=ch.end_time
			t1=cur_time.replace(year=s_time.year,month=s_time.month,day=s_time.day,hour=s_time.hour,
								minute=s_time.minute,second=s_time.second,microsecond=0)
			if t1 < cur_time:
				cur_time=t1
				c['ch_name']=ch.challenge_name
				c['s_time']=t1
		return render(request,'home.html',c)
	except:
		return HttpResponseRedirect('/Login/')
	
@login_required(login_url='/Login/')
def call_password(request):
	c={}
	c.update(csrf(request))
	#form = PasswordChangeForm(user=request.user)
	return render(request, 'change_password.html')

@login_required(login_url='/Login/')
def call_profile(request):
	c={}
	c.update(csrf(request))
	return render(request,'change_profile.html',c)

def new_registration(request):
	print("new_registration")
	c={}
	c.update(csrf(request))
	return render(request,'registration.html',c)


def registration(request):
	try:
		print("P.registration")
		pid=request.POST.get('userID')
		pname = request.POST.get('uname')
		pdob = request.POST.get('dob')
		pgender = request.POST.get('gender')
		pprof = request.POST.get('prof')
		puni = request.POST.get('uni')
		ppass = request.POST.get('pass')
		pemail = request.POST.get('email')
		pcontact = request.POST.get('contact')
		pmoto = request.POST.get('moto')
		c={}
		c['object_list']=pname
		user = authenticate(username=pid,password=ppass)
		if user is None:
			user=User.objects.create_user(pid,pemail,ppass)
			user.save()
			auth.login(request,user)
			s=Profile_det(user_id=pid,user_name=pname,email=pemail,dob=pdob,gender=pgender,Profession=pprof,University=puni,contact =pcontact,moto=pmoto)
			s.save()
			return HttpResponseRedirect('/Profile/home/')
		else:
			return HttpResponseRedirect('/Profile/new_registration/')
	except:
		return HttpResponseRedirect('/Profile/new_registration/')

@login_required(login_url='/Login/')
def login_user_profile(request):
	try:
		print(request.user.username)
		print("login_user_profile")
		c={}
		user_id=request.user.username
		request.session['user_id']=user_id
		username=Profile_det.objects.filter(user_id=user_id)
		c['id']=user_id
		c['name']=username[0].user_name
		c['email']=username[0].email
		c['dob']=username[0].dob
		c['gender']=username[0].gender
		c['prof']=username[0].Profession
		c['uni']=username[0].University
		c['contact']=username[0].contact
		c['moto']=username[0].moto
		return render(request,'profile.html',c)
	except:
		return HttpResponseRedirect('/Profile/')

@login_required(login_url='/Login/')
def search_user(request):
	try:
		print("search_user")
		c={}
		user_id=request.POST.get('user')
		username=Profile_det.objects.filter(user_id=user_id)
		if not username:
			messages.add_message(request,messages.INFO,'No such User Exist')
		else:
			request.session['user_id']=user_id
			c['id']=username[0].user_id
			c['name']=username[0].user_name
			c['email']=username[0].email
			c['dob']=username[0].dob
			c['gender']=username[0].gender
			c['prof']=username[0].Profession
			c['uni']=username[0].University
			c['contact']=username[0].contact
			c['moto']=username[0].moto
		return render(request,'user_profile.html',c)
	except:
		return HttpResponseRedirect('/Profile/')

'''def password_change(request):
	print("password_change")
	if request.method == 'POST':
		form = PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			print("hello")
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your password was successfully updated!')
			return HttpResponseRedirect('/Profile/home/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		
		form = PasswordChangeForm(request.user)
	return render(request, 'change_password.html')'''

@login_required(login_url='/Login/login/')
def password_change(request):
	try:
		print("change_password")
		c={}
		c.update(csrf(request))
		old_pass=request.POST.get('old_password')
		new_pass=request.POST.get('new_password1')
		renew_pass=request.POST.get('new_password2')
		user_id=request.user.username
		user=authenticate(username=user_id,password=old_pass)
		if user is not None:
			if new_pass==renew_pass:
				u=User.objects.get(username__exact=user_id)
				u.set_password(new_pass)
				u.save()
		return HttpResponseRedirect('/Login/login/')
	except:
		return HttpResponseRedirect('/Profile/login_user_profile/')

@login_required(login_url='/Login/')
def change_profile(request):
	try:
		print("change_profile")
		c={}
		c.update(csrf(request))
		new_user=request.POST.get('new_username')
		new_email=request.POST.get('new_email')
		new_dob=request.POST.get('new_dob')
		new_gender=request.POST.get('new_gender')
		new_prof=request.POST.get('new_prof')
		new_uni=request.POST.get('new_uni')
		new_contact=request.POST.get('new_contact')
		new_moto=request.POST.get('new_moto')
		user_id=request.user.username
		user=Profile_det.objects.filter(user_id=user_id)
		user.update(user_name=new_user,email=new_email,dob=new_dob,gender=new_gender,Profession=new_prof,University=new_uni,moto=new_moto)
		messages.add_message(request,messages.INFO,'your profile changed sucessfully')
		return HttpResponseRedirect('/Profile/login_user_profile/')
	except:
		return HttpResponseRedirect('/Profile/login_user_profile/')
