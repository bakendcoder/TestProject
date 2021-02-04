from django.db import models
from generic.custom_middlewares.CustomRequestMiddleware import (
                get_current_authenticated_user
)

class BaseModel(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("auth.User", 
                            null=True,
                            on_delete = models.SET_NULL,
                            related_name="%(class)s_created")
    updated_by = models.ForeignKey("auth.User", 
                            null=True,
                            on_delete = models.SET_NULL,
                            related_name="%(class)s_updated")

    class Meta:
        abstract = True


    def save(self,*args, **kwargs):
        
        user_obj = get_current_authenticated_user()
        if user_obj is not None:
            if self._state.adding:
                self.created_by = user_obj
            self.created_by = user_obj
        super().save(*args, **kwargs)