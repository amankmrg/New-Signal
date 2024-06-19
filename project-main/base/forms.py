from django.forms import ModelForm
from django import forms
from .models import Appointment, CustomUser, Doctor, diatrize
from django.contrib.auth.forms import UserCreationForm


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        exclude = ["user", "name"]
        widgets = {
            "followupdate": forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "yyyy-mm-dd (DOB)",
                    "class": "form-control",
                }
            )
        }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "username"]


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = []


class NewForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class speech2textForm(forms.Form):
    audio = forms.FileField(label="Audio", required=False)


class SummarizerForm(forms.Form):
    text = forms.CharField(
        label="Text to be Summarized", widget=forms.Textarea, required=False
    )

class YourModelForm(forms.ModelForm):
    class Meta:
        model = diatrize
        fields = ['audio']