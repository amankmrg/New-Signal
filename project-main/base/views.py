from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
import os
from django.conf import settings
from django.http import JsonResponse
from pyannote.audio.pipelines import SpeakerDiarization
from pydub import AudioSegment
from pyannote.core import Segment
from pyannote.audio import Model
from transformers import AutoModel
import assemblyai as aai
model = Model.from_pretrained("pyannote/speaker-diarization", 
                             use_auth_token="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")
YOUR_AUTH_TOKEN = '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'




from .forms import (
    AppointmentForm,
    RegistrationForm,
    DoctorForm,
    SummarizerForm,
    speech2textForm,
    YourModelForm,
)
from .models import Appointment, CustomUser, Doctor
import requests

# Create your views here.


def home(request):
    user = request.user
    context = {"user": user}
    return render(request, "base/home.html", context)


def registerPageDoctor(request):
    if request.user.is_authenticated:
        return redirect("home")
    # form = UserCreationForm()
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, "ERROR: Make sure you filled all the fields correctly"
            )
    return render(request, "base/register.html", {"form": form})


def registerPagePatient(request):
    if request.user.is_authenticated:
        return redirect("home")
    # form = UserCreationForm()
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, "ERROR: Make sure you filled all the fields correctly"
            )
    return render(request, "base/register.html", {"form": form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.get(email=email)
        except:
            # messages.error(request,'User does not exist')
            # Create form variable...
            message = "a"
            form = UserCreationForm(
                initial={"email": email, "password1": password, "password2": password}
            )

            # Assign render_value to True
            form.fields["email"].widget.render_value = True
            form.fields["password1"].widget.render_value = True

            # Return template with form...
            return render(
                request, "base/register.html", {"form": form, "message": message}
            )

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is wrong")

    return render(request, "base/login_page.html")


def logoutPage(request):
    logout(request)
    return redirect("home")


def getStarted(request):
    if request.user.is_authenticated:
        return render(request, "base/search.html")
    else:
        return render(request, "base/registernew.html")


def registernew(request):
    return render(request, "base/registernew.html")


def appointmentPage(request, pk):
    form = AppointmentForm()
    context = {"form": form, "indi": "appointment", "pk": pk}
    user = CustomUser.objects.get(id=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = user
            appointment.name = user.name
            appointment.save()
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")
    return render(request, "base/getstarted.html ", context)


def showAppointments(request, pk):
    user = CustomUser.objects.get(id=pk)
    appointments = user.appointment_set.all()
    context = {"user": user, "appointments": appointments}
    return render(request, "base/show_appointment.html", context)


def showdoctorpatients(request, pk):
    user = CustomUser.objects.get(id=pk)
    if user is None:
        return HttpResponse("Not found")
    patients = user.doctorname.all()
    k = []
    for patient in patients:
        email = patient.user.email
        if email not in k:
            k.append(patient)

    context = {"patients": k}
    return render(request, "base/show_appointment.html", context)


def search(request):
    if request.POST.get("q") != None:
        q = request.POST.get("q")
    else:
        q = ""

    users = CustomUser.objects.filter(Q(email__icontains=q) | Q(name__icontains=q))

    return render(request, "base/search.html", {"users": users})


def viewparticular(request, pk):
    user = CustomUser.objects.get(id=pk)
    if user is None:
        return HttpResponse("No such user exist")
    # patients = user.doctorname.filter(name__icontains = request.user)
    # patients = user.doctorname.all()
    # context = {'patients': patients}
    # return render(request,'base/show_appointment.html',context)
    appointments = user.appointment_set.all()
    context = {"user": user, "appointments": appointments}
    return render(request, "base/particularappointment.html", context)


def summarize(request):
    if request.method == "POST":
        form = SummarizerForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            response = requests.post(
                "https://test.norsu.xyz/summarize/", json={"text": text}
            )

            response_json = response.json()
            form = SummarizerForm()
            return render(
                request,
                "base/summarize.html",
                {"response": response_json, "form": form},
            )

    else:
        form = SummarizerForm()

    return render(request, "base/summarize.html", {"form": form})


def speech2text(request):
    if request.method == "POST":
        form = speech2textForm(request.POST, request.FILES)
        if form.is_valid():
            audio = form.cleaned_data["audio"]
            files = {"file": (audio.name, audio.read())}
            response = requests.post("https://test.norsu.xyz/upload/", files=files)
            response_json = response.json()
            form = speech2textForm()
            return render(
                request,
                "base/speech2text.html",
                {"response": response_json, "form": form},
            )

    else:
        form = speech2textForm()

    return render(request, "base/speech2text.html", {"form": form})


def new(request):
    return render(request, "base/index.html")


def diarize_speakers(request):
    if request.method == 'POST':
        form = YourModelForm(request.POST, request.FILES)
        if form.is_valid():
            initial_obj = form.save(commit=False)
            initial_obj.save()
            pathnew = initial_obj.audio.url
            form.save()

        FILE_URL = "D:/Study/copy of project/signal-project-main" + pathnew
        aai.settings.api_key = "fd8229d789de4c3eb54179aac97891b9"
        config = aai.TranscriptionConfig(speaker_labels=True)

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(
        FILE_URL,
        config=config
        )
        return render(request,'base/diarizationresult.html',{"transcript":transcript.utterances})
    else:
        form = YourModelForm()
        return render(request,'base/diarization.html',{'form':form})