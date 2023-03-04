from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('clogin',c_login),
    path('reg',c_registration),
    path('send',send_mail_regis),
    path('success',success),
    path('verify/<auth_token>',verify),
    path('error',error),
    path('jpost/<int:id>',post_job),
    path('nav',navbar),
    path('cdis',companies),
    path('sendc/<int:id>',sendmail_company),
    path('ulogin', u_login),
    path('ureg', u_registration),
    path('editprofile/<int:id>',edit_user),
    path('joblist/<int:id>',view_jobs),
    path('jobdetails/<int:id1>/<int:id2>',job_details),
    path('apply/<int:id1>/<int:id2>',apply),
    path('applicant/<int:id>',view_applicants),
    path('application/<int:id>',view_applications),


]



