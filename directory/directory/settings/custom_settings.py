from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

# make uuid as primary key
# DEFAULT_AUTO_FIELD = 'django.db.models.UUIDField'

# LOGIN REDIRECT AND LOGIN URL
LOGIN_URL = reverse_lazy("auth:login")
LOGOUT_REDIRECT_URL = reverse_lazy("auth:login")
LOGIN_REDIRECT_URL = reverse_lazy("profiles:teachers_list")


# SETTNGS FOR CRISPTY FORMS TO USE BOOTSTRAP4 
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# to map with bootstrap4 alert classes
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}



# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             # exact format is not important, this is the minimum information
#             'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'file',
#             'filename': 'teacher_profile.log'
#         }
#     },
#     'loggers': {
#         '': {
#             'level': 'WARNING',
#             'handlers': ['console'],
#         },
#          'teacher_profile': {
#             'level': 'DEBUG',
#             'handlers': ['file'],
#         },
#     },
# })

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'teacher_profile_logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'console',
            'filename': 'teacher_profile.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    
    'loggers': {
       
        'teacher_profile': {
            'level': 'DEBUG',
            'handlers': ['teacher_profile_logfile', 'console'],
        },
    },
}