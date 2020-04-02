from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from job_app.forms import (SignUpForm,Profile_InfoForm,Education_levelForm, Preference_Form,
                           Employement_DetailForm,File_UploadForm,)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from job_app.models import (Profile, Education_level, Employment_details, Preference, File_uploaded,)
from django.http.response import JsonResponse
from django.core import serializers


# Create your views here.

def index(request):
    return render(request, 'job_app/main_site.html')


def application_guide(request):
    return render(request, 'job_app/application_guide.html')


def activation_sent_view(request):
    return render(request, 'job_app/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'activation_invalid.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account.'
            message = render_to_string('job_app/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # return redirect('activation_sent')

    else:
        form = SignUpForm()

    return render(request, 'job_app/registration.html', {'form': form})


@login_required(login_url='/accounts/login/')
def get_userPage(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)

    # print("user profile certification ", profile.education_level)
    if profile is None:
        profile_form = Profile_InfoForm(instance=profile)
    else:
        profile_form = Profile_InfoForm(instance=profile)

    if profile.education_level is None:
        edu_form = Education_levelForm(instance=profile.education_level)
    else:
        edu_form = Education_levelForm(initial={'user': user, 'certification': profile.education_level.certification,'issuing_org': profile.education_level.issuing_org,'identification_number': profile.education_level.identification_number,'issue_date': profile.education_level.issue_date,'expiration_date': profile.education_level.expiration_date},instance=profile.education_level)
    if profile.employment_details is None:
        emp_form = Employement_DetailForm(instance=profile.employment_details)
    else:
        emp_form = Employement_DetailForm(instance=profile.employment_details)

    if profile.Preference is None:
        pref_form = Preference_Form(instance=profile.Preference)
    else:
        pref_form = Preference_Form(instance=profile.Preference)

    if profile.file_upload is None:
        uploaded_file_form = File_UploadForm(instance=profile.file_upload)
    else:
        uploaded_file_form = File_UploadForm(instance=profile.file_upload)

    # print("printing profile form\n.... {}".format(profile_form))
    context = {'user': request.user, 'user_info': request.user.profile, 'edu_details': profile.education_level, 'emp_details': profile.employment_details,'prof_form':profile_form, 'emp_form': emp_form, 'pref_form': pref_form, 'edu_form': edu_form,'files_form': uploaded_file_form ,'preference': profile.Preference,'file':profile.file_upload,}
    print("context var {}\n\n".format(context.items()))
    return render(request, 'job_app/application_info.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('user_email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # if user.is_active():
            login(request, user)
            return HttpResponseRedirect(reverse('application_details'))
            # else:
            return HttpResponse('Account not activated')
        else:
            print("Access denied due to invalid credential")
            print("username : {} and password entered : {}".format(username, password))
            return HttpResponse("Invalid username or password combination")
    else:
        return render(request, 'job_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def get_profile(request, user_id):
    # user = User.objects.get(pk=request.user.id)
    # profile = Profile.objects.get(user=user.id)
    # form = Education_levelForm(request.POST)
    # if request.method == 'POST':
    #     form = Education_levelForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    return render(request, 'job_app/client_detail_form.html')


def add_eduInfo(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    form = Education_levelForm()
    status = "";
    if request.method == 'POST':
        form = Education_levelForm(request.POST, instance=profile.education_level)
        if form.is_valid():
            instance = form.save(commit=False)
            status = "saved"
            instance.save()
            print("Education level added")
        else:
            print("Error while saving")
            status = "error"
    return HttpResponseRedirect(reverse('application_details'))


def add_userInfo(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    form = Profile_InfoForm(instance=profile)
    status = "";
    if request.method == 'POST':
        form = Profile_InfoForm(request.POST, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            print(instance)
            status = "saved"
            instance.save()
            print("user profile added")
        else:
            print("Error while saving")
            status = "error"
    return HttpResponseRedirect(reverse('application_details'))


def add_empInfo(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    form = Employement_DetailForm(instance=profile.employment_details)
    status = "";
    if request.method == 'POST':
        form = Employement_DetailForm(request.POST, instance=profile.employment_details)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            status = "saved"
            print("employment details added")
        else:
            print("Error while saving")
            status = "error"
    return HttpResponseRedirect(reverse('application_details'))


def add_Prefinfo(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    form = Preference_Form()
    status = "";
    if request.method == 'POST':
        form = Preference_Form(request.POST, instance=profile.Preference)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            status = "saved"
            print("prefernce info added")
        else:
            print("Error while saving")
            status = "error"
    return HttpResponseRedirect(reverse('application_details'))


def upload_file(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    form =File_UploadForm(instance=profile.file_upload)
    print(form)
    if request.method == 'POST':
        form = File_UploadForm(request.POST, instance=profile.file_upload)
        if form.is_valid():
            instance = form.save(commit=False)
            print(instance)
            instance.save()
            status = "saved"
            print("File uploaded ")
        else:
            print("Error while saving")
            status = "error"
    return HttpResponseRedirect(reverse('application_details'))


def UpdateEduInfo(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)

    if request.is_ajax or request.method == "POST":
        form = Education_levelForm(request.POST, instance=profile.education_level)
        if form.is_valid():
            print("form is valid")
            instance = form.save(commit=False)
            instance.refresh_from_db()
            instance.certification = form.cleaned_data.get('certification')
            instance.issuing_org = form.cleaned_data.get('issuing_org')
            instance.identification_number = form.cleaned_data.get('identification_number')
            instance.issue_date = form.cleaned_data.get('issue_date')
            instance.expiration_date = form.cleaned_data.get('expiration_date')
            instance.save()
            print("Education level  updated")

            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance, }, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def UpdateUserInfo(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    form = Profile_InfoForm( instance=profile)
    if request.is_ajax and request.method == "POST":
        form = Profile_InfoForm(request.POST, instance=profile)
        if form.is_valid():
            print("form is valid")
            instance = form.save(commit=False)
            instance.refresh_from_db()
            instance.user = form.cleaned_data.get('user')
            instance.first_name = form.cleaned_data.get('first_name ')
            instance.last_name = form.cleaned_data.get('last_name')
            instance.email = form.cleaned_data.get('email')

            instance.save()
            print("user profile  updated")

            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance, }, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def UpdateEmploymentDetails(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)

    if request.is_ajax and request.method == "POST":

        form = Employement_DetailForm(request.POST, instance=profile.employment_details)

        if form.is_valid():
            print("form is valid")
            instance = form.save(commit=False)
            instance.refresh_from_db()
            instance.employer = form.cleaned_data.get(' employer')
            instance.job_function = form.cleaned_data.get('job_function')
            instance.current_job_status = form.cleaned_data.get(' current_job_status')
            instance.start_date = form.cleaned_data.get('start_date')
            instance.end_date = form.cleaned_data.get('end_date')
            instance.save()
            print("user employment deatails  updated")

            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance, }, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def UpdatePreferenceDetails(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    if request.is_ajax and request.method == "POST":
        form = Preference_Form(request.POST, instance=profile.Preference)
        if form.is_valid():
            print("form is valid")
            instance = form.save(commit=False)
            instance.refresh_from_db()
            instance.job_field_pref = form.cleaned_data.get('job_field_pref ')
            instance.location_pref = form.cleaned_data.get('location_pref')

            instance.save()
            print("user preference details  updated")

            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance, }, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def Update_fileUploads(request, user_id):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    #form = File_UploadForm()

    if request.is_ajax and request.method == "POST":
        form = File_UploadForm(request.POST, instance=profile.file_upload)
        if form.is_valid():
            print("form is valid")
            instance = form.save(commit=False)
            instance.refresh_from_db()
            instance.file_name = form.cleaned_data.get('file_name')
            instance.submitted_date = form.cleaned_data.get('submitted_date')
            instance.comments = form.cleaned_data.get('comments')

            instance.save()
            print("user preference details  updated")

            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance, }, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)
