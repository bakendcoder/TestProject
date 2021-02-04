from django.db import models

from generic.models import BaseModel

class Subject(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "subjects"
        ordering = ["name"]

    def __str__(self):
        return self.name