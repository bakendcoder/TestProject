import logging 

import pandas as pd
from  zipfile import ZipFile

from django import forms 
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.forms.widgets import TextInput

from generic.utils import validate_email
from .teacher import Teacher

logger = logging.getLogger("teacher_profile")

class TeacherSearchForm(forms.Form):
    
    last_name_query = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'LastName first 2 letters'}))
    subject_query = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Subject first 2 letters'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control-sm", 'maxlength':"2"})


class TeacherProfileBulkCreateForm(forms.Form):
    archive = ""
    df = pd.DataFrame()
    csv_required_columns = {
                            'last name', 'profile picture', 'room number',
                            'subjects taught','email address', 'phone number', 
                            'first name'
                        }
    dropna_subset = ['last name', 'room number', 'email address', 
                    'phone number', 'first name']
    teacher_list_csv_file = forms.FileField(validators=[FileExtensionValidator(['csv'])])
    teacher_images_zip_file = forms.FileField(validators=[FileExtensionValidator(['zip'])])


    def validate_csv(self, df):
        df.columns= df.columns.str.lower()
        # dropna_subset = [column.lower() for column in self.dropna_subset]
        df.dropna(subset=self.dropna_subset, how="any", inplace=True)
        
        if len(df.index) == 0:
             self.add_error('teacher_list_csv_file',
                 'The Csv file is empty.')
        
        if not ({column for column in df.columns if column in self.csv_required_columns} == self.csv_required_columns):
             self.add_error('teacher_list_csv_file',
                 'The Csv columns are not matching.')
        return


    def clean(self):
        cleaned_data = self.cleaned_data

        teacher_list_csv_file_error = False 
        teacher_images_zip_file_error = False
    
        try:
            csv_file = cleaned_data.get("teacher_list_csv_file")
            self.df = pd.read_csv(csv_file)
            self.validate_csv(self.df)
        except Exception as e:
            logger.exception("error occured while reading csv file")
            teacher_list_csv_file_error = True



        try:
            zip_file = cleaned_data.get("teacher_images_zip_file")
            self.archive = ZipFile(zip_file, 'r')
        except:
            logger.exception("error occured while reading zip file")
            teacher_images_zip_file_error = True 

        if teacher_images_zip_file_error:
            self.add_error('teacher_images_zip_file',
                 'The Zip File is not readable')

        if teacher_list_csv_file_error:
            self.add_error('teacher_list_csv_file',
                 'The Csv File is not readable')
        
        return cleaned_data

    def close_zip(self, archive):
        try:
            archive.close()
        except:
            pass        


    def save(self):
        
        df_copy = self.df.copy()
        self.df[["email address"]] = self.df[["email address"]].applymap(lambda x:x.lower() if x else x)
        

        self.df[["is_email_valid"]] =self.df[['email address']].applymap(validate_email)
        df_with_invalid_email_rows = self.df[self.df["is_email_valid"]==False]
        
        df_copy_duplicated = self.df.duplicated(subset=["email address"])
        df_with_duplicated_rows = self.df[df_copy_duplicated]

        self.df = self.df[~df_copy_duplicated]
        self.df = self.df[self.df["is_email_valid"]==True]

        # self.df = self.df[valid_email_check]
        
        existing_teachers_list = {}
        csv_errors = {}
        csv_errors["exists"] = False
        csv_errors["db_exist_rows"] = []
        csv_errors["errors_while_saving_db_rows"] = []
        csv_errors["success_objs"] = []
        obj = None
        obj_created = False
        for index, row in self.df.iterrows():
            first_name = row["first name"]
            last_name = row["last name"]
            email = row["email address"]
            phone_number = row["phone number"]
            room_number = row["room number"]
            subjects = row["subjects taught"]
            
            profile_picture = str(row["profile picture"])
            pic_file = None
            if profile_picture and profile_picture.strip() in self.archive.namelist():
                try:
                    pic_file = File(self.archive.open(profile_picture.strip(), "r"))
                except:
                    pass 

            teacher_obj  = Teacher()
            obj, obj_created, objs_info = teacher_obj.create_obj(
                                first_name = first_name,
                                last_name = last_name,
                                email = email,
                                phone_number = phone_number,
                                room_number = room_number,
                                profile_picture = pic_file,
                                subjects = subjects,
                            )

            if obj and obj_created:
                csv_errors["success_objs"].append(objs_info["success_objs"])
            elif obj and not obj_created:
                if objs_info["error_exists"]:
                    csv_errors["exists"] = True
                    csv_errors["db_exist_rows"].append(objs_info["data_exists_in_db"])
            elif not obj:                
                if objs_info["error_exists"]:
                    csv_errors["exists"] = True
                    csv_errors["errors_while_saving_db_rows"].append(objs_info["errors_while_saving_db_rows"])
        
        self.close_zip(self.archive)

        
        csv_errors["duplicated_rows"] = []
        if not len(df_with_duplicated_rows.index) == 0:
            
            csv_errors["duplicated_rows"] = df_with_duplicated_rows.to_dict('records')
            csv_errors["exists"] = True

        csv_errors["invalid_email_rows"] = []
        if not len(df_with_invalid_email_rows.index) == 0:
            csv_errors["invalid_email_rows"] = df_with_invalid_email_rows.to_dict('records')
            csv_errors["exists"] = True

        return obj, csv_errors