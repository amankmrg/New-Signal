from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.



# class Patient(models.Model):
#     name = models.ForeignKey(User, on_delete = models.CASCADE)
    

#     def __str__(self):
#         return self.name.username



class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default = False)
    is_patient = models.BooleanField(default = False)
    email = models.EmailField(unique = True)
    name = models.CharField(max_length = 100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name','username']

    def __str__(self):
        return self.name




class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE,limit_choices_to={'is_doctor': True})
    #jab bhi koi doctor register ho to view function me aisa likhna ki Doctor wala model me bhi add ho jaaye 
    def __str__(self):
        return self.user.name


# class Patient(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
#     doctors = models.ForeignKey(Doctor, on_delete = models.CASCADE)

#     def __str__(self):
#         return self.user.name






gender_choice = (("male", "MALE"),("female","FEMALE"),("others","OTHERS"))




class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, null = True)
    age = models.IntegerField(default = 0)
    gender = models.CharField(max_length = 50, choices = gender_choice, default = 'male')
    date = models.DateField(auto_now = True)
    doctor_name = models.ForeignKey(CustomUser, on_delete = models.CASCADE,related_name = 'doctorname',limit_choices_to={'is_doctor': True})
    speciality = models.CharField(max_length = 200)
    symptom = models.CharField(max_length = 400)
    diagnosis = models.CharField(max_length = 400)
    prescriptions = models.CharField(max_length = 400)
    labreport = models.ImageField(upload_to='lab_reports')
    followupdate = models.DateField(null = True )
    def __str__(self):
        return self.name

class diatrize(models.Model):
    audio = models.FileField(upload_to = 'audio')