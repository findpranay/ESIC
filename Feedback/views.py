from django.shortcuts import render,redirect
from .forms import PatientCreationForm,PatientUpdationForm,UserLoginForm,INPatientUpdationForm,OTPVerifyForm
from . models import Patient,HOD,PatientIN,Minister
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
import math,random
#from django.generic.views import CreateView
from django.views.generic import View

def homepage(request):
    totalfeedbacks=(len(Patient.objects.all())+len(PatientIN.objects.all()))
    solvedissues=(len(Patient.objects.filter(Status="1"))+len(PatientIN.objects.filter(Status="1")))  
    unsolvedissues=(len(Patient.objects.filter(Status="-1"))+len(PatientIN.objects.filter(Status="-1")))
    pendingissues=totalfeedbacks-solvedissues-unsolvedissues
    if request.session.get('user_session',None):
        currentuser=request.session['user_session']
        return render(request,'Feedback/index2.html',{'currentuser':currentuser,'totalfeedbacks':totalfeedbacks,'solvedissues':solvedissues,'pendingissues':pendingissues,'unsolvedissues':unsolvedissues})
    return render(request,'Feedback/index.html',{'totalfeedbacks':totalfeedbacks,'solvedissues':solvedissues,'pendingissues':pendingissues,'unsolvedissues':unsolvedissues})

def details(request,patient_id):
    req=Patient.objects.filter(id=patient_id)
    currentuser=request.session['user_session']
    return render(request,'Feedback/details.html',{'req':req,'currentuser':currentuser})


def detailsIN(request,patient_id):
    req=PatientIN.objects.filter(id=patient_id)
    currentuser=request.session['user_session']
    return render(request,'Feedback/details.html',{'req':req,'currentuser':currentuser})

def patientcomplaints(request):
    if request.session.get('user_session',None):
        currentuser=request.session['user_session']
        in_Minister=Minister.objects.filter(email=currentuser)
        in_HOD=HOD.objects.filter(email=currentuser)
        currentuser=request.session['user_session']
        if in_Minister.exists():
            patientlist=Patient.objects.filter(Status="2")
        elif in_HOD.exists():
            patientlist=Patient.objects.filter(Status="0")
        return render(request,"Feedback/OUTPatientdash.html",{'patientlist':patientlist,'currentuser':currentuser})
    else:
        return render(request,"Feedback/login.html")

def patientINcomplaints(request):
    if request.session.get('user_session',None):
        currentuser=request.session['user_session']
        in_Minister=Minister.objects.filter(email=currentuser)
        in_HOD=HOD.objects.filter(email=currentuser)
        currentuser=request.session['user_session']
        if(in_Minister.exists()):
            patientlist=PatientIN.objects.filter(Status="2")
        elif(in_HOD.exists()):
            patientlist=PatientIN.objects.filter(Status="0")  
        return render(request,"Feedback/INPatientdash.html",{'patientlist':patientlist,'currentuser':currentuser})
    else:
        return render(request,"Feedback/login.html")

def change(request,patient_id):
    patient_el=Patient.objects.get(id=patient_id)
    patient_el.Status="1"
    patient_el.save()
    return HttpResponseRedirect(reverse('patientcomplaints'))

def change2(request,patient_id):
    patient_el=PatientIN.objects.get(id=patient_id)
    patient_el.Status="1"
    patient_el.save()
    return HttpResponseRedirect(reverse('patientINcomplaints'))


def forward(request,pat_id):
    patient_el=Patient.objects.get(id=pat_id)
    currentuser=request.session['user_session']
    in_HOD=HOD.objects.filter(email=currentuser)
    in_Minister=Minister.objects.filter(email=currentuser)
    if in_HOD.exists():
        patient_el.Status="2"
        patient_el.save()
    elif in_Minister.exists():
        patient_el.Status="-1"
        patient_el.save()
    return HttpResponseRedirect(reverse('patientcomplaints'))


def forward2(request,pat_id):
    patient_el=PatientIN.objects.get(id=pat_id)
    currentuser=request.session['user_session']
    in_HOD=HOD.objects.filter(email=currentuser)
    in_Minister=Minister.objects.filter(email=currentuser)
    if in_HOD.exists():
        patient_el.Status="2"
        patient_el.save()
    elif in_Minister.exists():
        patient_el.Status="-1"
        patient_el.save()
    return HttpResponseRedirect(reverse('patientINcomplaints'))

def dashboard(request):
    if request.session.get('user_session',None):
        values=len(Patient.objects.filter(AreaofIssue="hygiene"))
        values1=len(Patient.objects.filter(AreaofIssue="doctor"))
        values2=len(Patient.objects.filter(AreaofIssue="waiting"))
        values3=len(Patient.objects.filter(AreaofIssue="pharmacy"))
        values4=len(Patient.objects.filter(AreaofIssue="nurse"))
        values5=len(PatientIN.objects.filter(AreaofIssue="admission"))
        values6=len(PatientIN.objects.filter(AreaofIssue="nurse"))
        values7=len(PatientIN.objects.filter(AreaofIssue="doctor"))
        values8=len(PatientIN.objects.filter(AreaofIssue="allot"))
        values9=len(PatientIN.objects.filter(AreaofIssue="discharge"))
        currentuser=request.session['user_session']
        return render(request,'Feedback/dashboard.html',{'currentuser':currentuser,'values':values,'values1':values1,'values2':values2,'values3':values3,'values4':values4,'values5':values5,'values6':values6,'values7':values7,'values8':values8,'values9':values})
    else:
        return render(request,'Feedback/login.html')


def thankyou(request):
    return render(request,'Feedback/thankyou.html')

def login(request): 
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            input_email=form.cleaned_data['email']
            passwd=form.cleaned_data['password']
            in_HOD=HOD.objects.filter(email=input_email,password=passwd)
            in_Minister=Minister.objects.filter(email=input_email,password=passwd)
            if in_HOD.exists():
                request.session['user_session']=input_email
                return HttpResponseRedirect(reverse('dashboard'))
            elif in_Minister.exists():
                request.session['user_session']=input_email
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                no_account="Invalid Employee ID or Password"
                return render(request,'Feedback/login.html',{'form':form,'no_account':no_account})         
        else:
            field_error="Invalid Fields"
            return render(request,'Feedback/login.html',{'form':form,'field_error':field_error})

    else:
        form=UserLoginForm()
    return render(request,'Feedback/login.html',{'form':form})


def askingpage(request):
    return render(request,"Feedback/askingpage.html")

'''def adminaskingpage(request):
    return render(request,"Feedback/adminaskingpage.html")'''

def patientfeedback(request):
    if request.method=='POST':
        form=PatientCreationForm(request.POST)
        if form.is_valid():
            digits="0123456789"
            OTPcode=""
            for i in range(4) : 
                OTPcode += digits[math.floor(random.random() * 10)]
            user=form.cleaned_data['mobile_number']
            ip=form.cleaned_data['ip_number']
            request.session['patient_session']=user
            currentuser=request.session['patient_session']
            record=Patient(mobile_number=user,otp=OTPcode,ip_number=ip)
            record.save()   
            send_mail('OTP for ESIC',
            'Your One Time Password is'+OTPcode,
            '',
            [user])
            return HttpResponseRedirect(reverse('verifyotp'))
        else:
            field_error="Please Check Your Fields"
            return render(request,'Feedback/feedbackstart.html',{'form':form,'field_error':field_error})
    else:
        form=PatientCreationForm()
    return render(request,'Feedback/feedbackstart.html',{'form':form})

def patientINfeedback(request):
    if request.method=='POST':
        form=PatientCreationForm(request.POST)
        if form.is_valid():
            digits="0123456789"
            OTPcode=""
            for i in range(4): 
                OTPcode += digits[math.floor(random.random() * 10)]
            user=form.cleaned_data['mobile_number']
            request.session['patient_session']=user
            currentuser=request.session['patient_session']
            
            record=PatientIN(mobile_number=user,otp=OTPcode)
            record.save()
            send_mail('OTP for ESIC',
            'Your One Time Password is: '+OTPcode,
            '',
            [user])
            return HttpResponseRedirect(reverse('verifyotp'))
        else:
            field_error="Please Check Your Fields"
            return render(request,'Feedback/feedbackinstart.html',{'form':form,'field_error':field_error})
    else:
        form=PatientCreationForm()
    return render(request,'Feedback/feedbackinstart.html',{'form':form})



def verifyotp(request):
    if request.method=="POST":
        form=OTPVerifyForm(request.POST)
        if form.is_valid():
            otpsubm=form.cleaned_data['otp']
            currentuser=request.session['patient_session']
            actual=Patient.objects.filter(mobile_number=currentuser,otp=otpsubm)
            actualin=PatientIN.objects.filter(mobile_number=currentuser,otp=otpsubm)
            if actual.exists():
                actual=Patient.objects.filter(mobile_number=currentuser,otp=otpsubm).update(otp=None)               
                return HttpResponseRedirect(reverse('Feedbackform'))
            elif actualin.exists():
                actualin=Patient.objects.filter(mobile_number=currentuser,otp=otpsubm).update(otp=None)               
                return HttpResponseRedirect(reverse('IPDFeedbackForm'))
            else:
                error_msg="Incorrect OTP"
                return render(request,"Feedback/otpverify.html",{'form':form, 'error_msg':error_msg})
        else:
            error_msg = "Invalid Details"
            return render(request,"Feedback/otpverify.html",{'form':form, 'error_msg':error_msg})
    else:
        form=OTPVerifyForm()
        return render(request,"Feedback/otpverify.html",{'form':form})




def IPDFeedbackForm(request):
    if request.method=='POST':
        form=INPatientUpdationForm(request.POST)
        if form.is_valid():
            rating=form.cleaned_data['Rating']
            SorF=form.cleaned_data['sandf']
            Dep=form.cleaned_data['department']
            aoi=form.cleaned_data['AreaofIssue']
            admis=form.cleaned_data['AdmissionIssue']
            nursis=form.cleaned_data['NurseIssue']
            doctis=form.cleaned_data['DoctorIssue']
            allotis=form.cleaned_data['AllotmentIssue']
            disch=form.cleaned_data['DischargeIssue']
            Explanation=form.cleaned_data['explanation']
            currentuser=request.session['patient_session']
            record=PatientIN.objects.filter(mobile_number=currentuser).update(Rating=rating,sandf=SorF,department=Dep,AreaofIssue=aoi,AdmissionIssue=admis,NurseIssue=nursis,DoctorIssue=doctis,AllotmentIssue=allotis,DischargeIssue=disch,explanation=Explanation)
            try:
                del request.session['patient_session']
            except KeyError:    
                pass
            return HttpResponseRedirect(reverse('thankyou'))         
        else:
            field_error="Please Check Your Fields"
            return render(request,'Feedback/IPDFeedbackform.html',{'form':form,'field_error':field_error})

    else:
        form=INPatientUpdationForm()
    
    return render(request,'Feedback/IPDFeedbackform.html',{'form':form})



def Feedbackform(request):
    if request.method=='POST':
        form=PatientUpdationForm(request.POST)
        if form.is_valid():
            rating=form.cleaned_data['Rating']
            SorF=form.cleaned_data['sandf']
            Dep=form.cleaned_data['department']
            aoi=form.cleaned_data['AreaofIssue']
            hyg=form.cleaned_data['Hygiene']
            docb=form.cleaned_data['DoctorBehaviour']
            waT=form.cleaned_data['WaitingTime']
            phar=form.cleaned_data['Pharmacy']
            nurse=form.cleaned_data['Nurse']
            Explanation=form.cleaned_data['explanation']
            currentuser=request.session['patient_session']
            record=Patient.objects.filter(mobile_number=currentuser).update(Rating=rating,sandf=SorF,department=Dep,AreaofIssue=aoi,Hygiene=hyg,DoctorBehaviour=docb,WaitingTime=waT,Pharmacy=phar,Nurse=nurse,explanation=Explanation)
            
            try:
                del request.session['patient_session']
            except KeyError:
                pass
            return HttpResponseRedirect(reverse('thankyou'))         
        else:
            field_error="Please Check Your Fields"
            return render(request,'Feedback/Feedbackform.html',{'form':form,'field_error':field_error})

    else:
        form=PatientUpdationForm()
    
    return render(request,'Feedback/Feedbackform.html',{'form':form})



    


def logout(request):
    try:
        del request.session['user_session']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('homepage'))



