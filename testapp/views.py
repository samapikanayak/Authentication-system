from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .models import CUser, OTP

from django.core.mail import send_mail

def send_email(subject,body,from_email,to):
    send_mail(subject,body,from_email,to)

def login_view(request):
    if request.method == "POST":
        mobile = request.POST['mobile']    
        if (otp:=OTP.objects.filter(email_or_mobile=mobile).first()):
            otp.save()
        otp=OTP.objects.create(email_or_mobile=mobile)
        print(otp.otp)
        request.session['otp'] = otp.otp
        request.session['email_or_mobile'] = otp.email_or_mobile
        return redirect('/otp')
    return render(request,'login.html')

def otp(request):
    email_or_mobile = request.session.get('email_or_mobile')
    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp:=OTP.objects.filter(otp=otp,email_or_mobile=email_or_mobile).first():
            if not otp.is_expired:
                if (user:=CUser.objects.filter(mobile=email_or_mobile)).exists():
                    return HttpResponse(user.first().name)
        return HttpResponse('not ok')

    return render(request,'otp.html')

def login_with_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if (user:=CUser.objects.filter(email=email,password=password)).exists():
            user = user.first()
            send_email('password rest token',f'your password reset token {user.password_token}','sangrampattnaik09@gmail.com',[user.email])
            pwd = user.password_token
            return render(request,'login-email.html',{'pwd':pwd})
    return render(request,'login-email.html')

