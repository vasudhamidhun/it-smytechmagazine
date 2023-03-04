from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
import uuid
from job_pro.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth import authenticate

#super user: admin control panel
# username :chithira2
# password :arun16
# company : arun 1234/ Luminar 1234
# user : chithira.ah@gmail.com 1234/ arunvelayudhank@yahoo.co.in 1234

def index(request):
    return render(request,'index.html')

def c_registration(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password==cpassword:
            #checking
            if User.objects.filter(username=username).first():
                messages.success(request,'Username already taken')
                return redirect(c_registration)
            if User.objects.filter(email=email).first():
                messages.success(request,'email already exist')
                return redirect(c_registration)
            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=companyprofile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_regis(email,auth_token)
            return redirect(success)

        else:
            return HttpResponse("<h1 style='color:blue;text-align:center'>password entered incorrectly</h1>")

    return render(request,'registration.html')


def send_mail_regis(email,token):
    subject = "Your account has been verified"
    message = f'click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject, message, email_from, recipient)


def success(request):
    return render(request,'success.html')

def verify(request,auth_token):
    profile_obj=companyprofile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(c_login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(c_login)
    else:
        return redirect(error)


def error(request):
    return render(request,'error.html')

def c_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj= User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'company not found')
            return redirect(c_login)
        profile_obj=companyprofile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your mail inbox')
            return redirect(c_login)
        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'Incorrect email or password')
            return redirect(c_login)
        obj=companyprofile.objects.filter(user=user)
        return render(request,'company_index.html',{'obj':obj})

    return render(request,'login.html')

def post_job(request,id):
    com = companyprofile.objects.get(id=id)
    if request.method == 'POST':
        a = postjobform(request.POST)
        if a.is_valid():
            cn = a.cleaned_data['cname']
            ce = a.cleaned_data['cemail']
            ct = a.cleaned_data['ctitle']
            cty = a.cleaned_data['ctype']
            cx = a.cleaned_data['cexp']
            jt = a.cleaned_data['jtype']

            b = jobpost(cname=cn,cemail=ce,ctitle=ct,ctype=cty,cexp=cx,jtype=jt)
            b.save()
            return render(request,'jobsuccess.html')
        else:
            return redirect(error)

    return render(request,'post_job.html',{'com':com})



def navbar(request):
    return render(request,'navbar.html')

def companies(request):
    us=User.objects.all()
    li=[]
    eml=[]
    idc =[]
    for i in us:
        cname=i.username
        li.append(cname)
        cemail= i.email
        eml.append(cemail)
        cid= i.id
        idc.append(cid)

    # admin position must be of 0th position
    li1=li[1:]
    eml1=eml[1:]
    idc1=idc[1:]
    mylist = zip(li1,eml1,idc1)
    return render(request,'reg_list.html',{'user':mylist})


def sendmail_company(request,id):
    a = User.objects.get(id=id)
    u=a.username
    b=a.email
    if request.method== 'POST':
        x=send_mailform(request.POST)
        if x.is_valid():
            sub = x.cleaned_data['subject']
            mes = x.cleaned_data['message']
            send_mail(str(sub)+'||'+'JobsGuru',mes,EMAIL_HOST_USER,[b],fail_silently=False)

            return render(request,'emailsuccess.html')

    return render(request,'company_mail.html',{'u':u,'b':b})

#applicant/user module starts here

def u_registration(request):
    if request.method =='POST':
        u = user_form(request.POST)
        if u.is_valid():
            unm = u.cleaned_data['username']
            eml = u.cleaned_data['email']
            mb = u.cleaned_data['mob']
            db = u.cleaned_data['dob']
            qn = u.cleaned_data['qualification']
            pw = u.cleaned_data['password']
            pwc = u.cleaned_data['cpassword']

            if pw == pwc:
                mod = user_model(username=unm,email=eml,mob=mb,dob=db,qualification=qn,password=pw)
                mod.save()
                return redirect(u_login)
            else:
                return render(request,'user_pwderr.html')
        else:
            return render(request,'ureg_failed.html')

    return render(request,'user_reg.html')


def u_login(request):
    if request.method == 'POST':
        user = user_logform(request.POST)
        if user.is_valid():
            email = user.cleaned_data['email']
            pwd = user.cleaned_data['password']

            x = user_model.objects.all()
            for i in x:
                if email == i.email and pwd == i.password:
                    unm = i.username
                    eml = i.email
                    mb = i.mob
                    ql = i.qualification
                    id1 = i.id
                    return render(request,'user_profile.html',{'unm':unm,'eml':eml,'mb':mb,'ql':ql,'id':id1})
            else: #this else must be in line with for loop otherwise the else part will work for each iteration
                return render(request,'error.html')

    return render(request,'user_log.html')

def edit_user(request,id):
    user = user_model.objects.get(id=id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.mob = request.POST.get('mob')
        # user.dob = request.POST.get('dob')
        user.qualification = request.POST.get('qualification')
        user.save()
        return redirect(u_login)
    return render(request,'editprofile.html',{'user':user})

def view_jobs(request,id):
    user_id= id
    job = jobpost.objects.all()
    cnm=[]
    ceml=[]
    jtitle=[]
    wrktype=[]
    exp=[]
    jtype=[]
    idj=[]
    for i in job:
        cnm1 = i.cname
        cnm.append(cnm1)
        ceml1 = i.cemail
        ceml.append(ceml1)
        jtitle1 = i.ctitle
        jtitle.append(jtitle1)
        wrktype1 = i.ctype
        wrktype.append(wrktype1)
        exp1 = i.cexp
        exp.append(exp1)
        jtype1 = i.jtype
        jtype.append(jtype1)
        id1 = i.id
        idj.append(id1)


    job_list = zip(cnm,ceml,jtitle,wrktype,exp,jtype,idj)

    return render(request,'jobs_list.html',{'jobs':job_list,"user":user_id})

def job_details(request,id1,id2):
    user_id =id2
    job_id =id1
    job = jobpost.objects.get(id=id1)
    a = job.cname
    b = job.cemail
    c = job.ctitle
    d = job.ctype
    e = job.cexp
    f = job.jtype
    context={"a":a,"b":b,"c":c,"d":d,"e":e,"f":f,"user":user_id,"job":job_id}
    return render(request,'job_details.html',context)

def apply(request,id1,id2):
    user = user_model.objects.get(id=id1)
    job = jobpost.objects.get(id=id2)
    name= user.username
    email= user.email
    cname= job.cname
    jtitle= job.ctitle
    context = {"a":cname,"b":jtitle,"c":name,"d":email}
    if request.method== 'POST':
        application = applyjob() #model
        application.cname = request.POST.get('cname')
        application.jtitle = request.POST.get('jtitle')
        application.name = request.POST.get('name')
        application.email = request.POST.get('email')
        application.quali = request.POST.get('quali')
        application.phone = request.POST.get('phone')
        application.uexp = request.POST.get('uexp')
        application.resume = request.FILES['resume']
        application.save()
        return render(request,'apply_success.html')

    return render(request,'apply_job.html',context)

def view_applicants(request,id):
    com = companyprofile.objects.get(id=id)
    com_name = com.user.username
    data = applyjob.objects.all()
    job=[]
    nam=[]
    eml=[]
    quali=[]
    ph=[]
    exp=[]
    cv=[]
    for i in data:
        if i.cname==com_name:
            jtitle1 = i.jtitle
            job.append(jtitle1)
            name1 = i.name
            nam.append(name1)
            email1 = i.email
            eml.append(email1)
            quali1 = i.quali
            quali.append(quali1)
            phone1 = i.phone
            ph.append(phone1)
            uexp1 = i.uexp
            exp.append(uexp1)
            resume1 = i.resume
            cv.append(str(resume1).split('/')[-1])
    applicants = zip(job,nam,eml,quali,ph,exp,cv)

    return render(request,'show_hover.html',{'applicants':applicants})

def view_applications(request,id):
    user= user_model.objects.get(id=id)
    username= user.username
    data = applyjob.objects.all()
    job = []
    cnam = []
    cv = []
    for i in data:
        if i.name == username:
            jtitle1 = i.jtitle
            job.append(jtitle1)
            cname1 = i.cname
            cnam.append(cname1)
            resume1 = i.resume
            cv.append(str(resume1).split('/')[-1])
    application = zip(job,cnam,cv)
    return render(request, 'show_applications.html', {'application': application})

















