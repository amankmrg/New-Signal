from django.contrib import admin
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name="home"),
    path("registerpatient/", views.registerPagePatient, name="registerpatient"),
    path("registernew/", views.registernew, name="registernew"),
    path("registerdoctor/", views.registerPageDoctor, name="registerdoctor"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("getstarted/", views.getStarted, name="getstarted"),
    path("appointment/<str:pk>", views.appointmentPage, name="appointment"),
    path("viewappointment/<str:pk>/", views.showAppointments, name="viewappointment"),
    path("search/", views.search, name="search"),
    path(
        "doctorappointments/<str:pk>",
        views.showdoctorpatients,
        name="doctorappointments",
    ),
    path(
        "particularappointments/<str:pk>",
        views.viewparticular,
        name="particularappointments",
    ),
    path("summarize/", views.summarize, name="summarize"),
    path("speech2text/", views.speech2text, name="speech2text"),
    path("new/", views.new, name = "new"),
    path("diarize/", views.diarize_speakers, name = "diarize"),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
