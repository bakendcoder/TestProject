from django.db import models
from django.urls import reverse

from generic.models import BaseModel
from subjects.models import Subject 


class TeacherProfile(BaseModel):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)
    room_number = models.CharField(max_length=50)
    room_number = models.CharField(max_length=50)
    profile_picture = models.FileField(
                    default="default_picture.jpeg",
                    upload_to="teachers/"
                )
    subjects = models.ManyToManyField(Subject, related_name="teachers")

    class Meta:
        db_table = "teacher_profiles"
        ordering = ["-created_by"]

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):        
        return reverse("profiles:teachers_detail", args=[(self.id)])