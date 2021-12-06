from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import generic
from django.template.context_processors import csrf
from django.contrib import messages
from CodeHacker.settings import *
from online_judge.models import *
from leaderboard import *
import os,io
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.template import Context
#from somewhere import handle_uploaded_file

@login_required(login_url='/Login/login/')
def upload_file(request):
	try:
		c={}
		c.update(csrf(request))
		problem=request.session.get('problem')
		c['input']=str(problem).lower()+"_input.txt"
		return render(request,'upload.html',c)
	except:
		return HttpResponseRedirect('/Home_Module/view_problem/')

@login_required(login_url='/Login/login/')
def compare(request):
	try:
		c={}
		code_file=request.FILES['code_file']
		file1 =request.FILES['file1']
		user_id=request.user.username
		challenge=request.session.get('challenge')
		problem=request.session.get('problem')
		path = BASE_DIR + "/online_judge/static/my_output/"+str(problem)+".txt"
		myfile=open(path,'br')
		l3=""
		l4=""
		for line in file1:
			for i in line:
				if i!='\n' and i!="\n" and i!='\t' and i!=" " and i!=' ' and i!='\r':
					l3+=str(i)
	    
		for line in myfile:
			for i in line:
				if i!='\n' and i!="\n" and i!='\t' and i!=" " and i!=' ' and i!='\r':
					l4+=str(i)

		myfile.close()
		file1.close()
		status=True
		if l3!=l4:
			status=False
			messages.add_message(request, messages.INFO, 'your submission status: WRONG ANSWER')
		else:
			messages.add_message(request, messages.INFO, 'your submission status: ACCEPTED')

		c['object_list']=status
		sub_count=submissions.objects.filter().count()+1
		file_name=str(sub_count)+".txt"
		code_link=BASE_DIR + "/online_judge/static/user_output/" +file_name
		file_writer=open(code_link,'wb+')
		cur_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		s=submissions(sub_num=sub_count,user_id=user_id,problem_code=problem,challnge_name=challenge,sub_status=status,time=cur_time)
		s.save()
		for line in code_file:
			line.strip()
			file_writer.write(line)
		code_file.close()
		request.session['status']=status
		return HttpResponseRedirect('/leaderboard/update_leaderboard/')
	except:
		return HttpResponseRedirect('/online_judge/upload_file/')

@login_required(login_url='/Login/login/')
def my_submission(request):
	try:
		user_id=request.user.username
		problem_code=request.session.get('problem')
		challenge=request.session.get('challenge')
		print(problem_code,challenge)
		tot_sub=submissions.objects.filter(user_id=user_id,problem_code=problem_code,challnge_name=challenge)
		return render(request,'submission.html',{'tot_sub':tot_sub})
	except:
		return HttpResponseRedirect('/Home_Module/view_problem/')

@login_required(login_url='/Login/login/')
def all_submission(request):
	try:
		print("all_submission")
		problem_code=request.session.get('problem')
		challenge=request.session.get('challenge')
		tot_sub=submissions.objects.filter(problem_code=problem_code,challnge_name=challenge)
		return render(request,'submission.html',{'tot_sub':tot_sub})
	except:
		return HttpResponseRedirect('/Home_Module/view_problem/')

@login_required(login_url='/Login/login/')
def user_submission(request):
	try:
		print("user_submission")
		user_id=request.session.get('user_id')
		print(user_id)
		tot_sub=submissions.objects.filter(user_id=user_id)
		return render(request,'submission.html',{'tot_sub':tot_sub})
	except:
		return HttpResponseRedirect('/Profile/search_user/')

@login_required(login_url='/Login/login/')
def home_submission(request):
	try:
		print("home_submissions")
		tot_sub=submissions.objects.filter()
		return render(request,'submission.html',{'tot_sub':tot_sub})
	except:
		return HttpResponseRedirect('/Profile/')
