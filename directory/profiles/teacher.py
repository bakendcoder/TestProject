import logging

from django.core.files.base import ContentFile
from django.core.files import File
from subjects.models import Subject
from .models import TeacherProfile 

logger = logging.getLogger("teacher_profile")

class Teacher(object):
    teachers_subject_count = 5
    search_fields = {
        "last_name_query":"last_name__istartswith",
        "subject_query":"subjects__name__istartswith"
    }

    def qs_filter(self, request):    
        return {query_name:request.GET.get(query_field) for query_field, query_name in self.search_fields.items() if request.GET.get(query_field,"")}
    
    def queryset(self, request):

        qs = TeacherProfile.objects.all()
        qs = qs.filter(**self.qs_filter(request))
        return qs


    def create_obj(
            self,
            first_name,
            last_name,
            email,
            phone_number,
            room_number,
            profile_picture,
            subjects=None,
        ):
        objs_info = {}
        objs_info["error_exists"] = False
        objs_info["errors_while_saving_db_rows"] = {}
        objs_info["data_exists_in_db"] = {}
        objs_info["success_objs"] = {}
        obj, obj_created = None, False
        try:
            obj, obj_created = TeacherProfile.objects.get_or_create(
                            email=str(email).strip().lower(),
                            defaults={
                                "first_name": str(first_name).strip(),
                                "last_name": str(last_name).strip(),
                                "phone_number": str(phone_number).strip(),
                                "room_number": str(room_number).strip()
                            }
                        )

            success_objs = {}
            success_objs["email address"] = email
            success_objs["first name"] = first_name
            success_objs["last name"] = last_name
            success_objs["phone number"] = phone_number
            success_objs["room number"] = room_number
            objs_info["success_objs"] = success_objs
            if profile_picture is not None and obj_created:
                obj.profile_picture.save(profile_picture.name, profile_picture, save=True)
            try:
                if profile_picture is not None:
                    profile_picture.close()
            except:
                pass
        except Exception as e:
            logger.exception("error occured while saving the teacher profile")

            objs_info["error_exists"] = True
            errors_while_saving = {}
            errors_while_saving["email address"] = email
            errors_while_saving["first name"] = first_name
            errors_while_saving["last name"] = last_name
            errors_while_saving["phone number"] = phone_number
            errors_while_saving["room number"] = room_number
            objs_info["errors_while_saving_db_rows"] = errors_while_saving

        if obj and not obj_created:
            objs_info["error_exists"] = True
            data_exists_in_db = {}
            data_exists_in_db["email address"] = email
            data_exists_in_db["first name"] = first_name
            data_exists_in_db["last name"] = last_name
            data_exists_in_db["phone number"] = phone_number
            data_exists_in_db["room number"] = room_number
            objs_info["data_exists_in_db"] = data_exists_in_db

        if all([obj is not None, obj_created, subjects is not None]):
            try:
                subjects = str(subjects).split(',')
                subjects_list = list({subject.strip().lower() for subject in subjects if subject })
                for subject in subjects_list[:self.teachers_subject_count]:
                    sobj, created = Subject.objects.get_or_create(name=subject)
                    obj.subjects.add(sobj)
            except Exception as e:
                logger.exception("error occured while saving the teacher subject")
                pass
        
        return obj, obj_created, objs_info