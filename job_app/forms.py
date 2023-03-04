from django import forms

class postjobform(forms.Form):

    cname = forms.CharField(max_length=30)
    cemail = forms.EmailField()
    ctitle = forms.CharField(max_length=50)
    ctype = forms.CharField(max_length=30)
    cexp = forms.CharField(max_length=30)
    jtype = forms.CharField(max_length=30)

class send_mailform(forms.Form):
    subject = forms.CharField(max_length=30)
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows':3,'cols':30}))


class user_form(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    mob = forms.IntegerField()
    dob = forms.DateField()
    qualification = forms.CharField(max_length=100)
    password = forms.CharField(max_length=10)
    cpassword = forms.CharField(max_length=10)

class user_logform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=10)
