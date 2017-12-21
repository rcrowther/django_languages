from django.db.models.fields import CharField

#from .languages import IANA_LANGDATA
from .internet_languages import INTERNET_LANGDATA
from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA

#! display code or common lamguage name
#! select vurrent choice

class LanguageField(CharField):
    langdata = DJANGO_LANGDATA
    
    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        # Local import so the languages aren't loaded unless they are needed.
        langdata = kwargs.pop('langdata', None)
        # languages default is Django languages
        if langdata:
            self.languages = langdata
        self.languages_flag_url = kwargs.pop('languages_flag_url', None)
        self.blank_label = kwargs.pop('blank_label', None)
        self.multiple = kwargs.pop('multiple', None)
        kwargs['choices'] = self.langdata
        if self.multiple:
            kwargs['max_length'] = len(self.langdata) * 5 - 1
        else:
            kwargs['max_length'] = 5
        #kwargs.setdefault('max_length', 3)
        #kwargs.setdefault('choices', LANGUAGES)
        super(CharField, self).__init__(*args, **kwargs)
