from django.urls import path,include
from online_judge import views
from django.conf.urls import url

urlpatterns=[
	url(r'upload_file',views.upload_file),
	url(r'compare',views.compare),
	url('all_submission',views.all_submission),
	url('my_submission',views.my_submission),
	url('home_submission',views.home_submission),
	url('user_submission',views.user_submission),
]
