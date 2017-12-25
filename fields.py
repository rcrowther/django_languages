from django.db.models.fields import CharField, BLANK_CHOICE_DASH
from django.forms.fields import TypedChoiceField, TypedMultipleChoiceField
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
#from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA
from .language_choices import LanguageChoices
from .lang_models import Language, EmptyLanguage
from .selectors import DJANGO_TRANSLATED, UNITED_NATIONS



#class LanguageDescriptor(object):
    #"""
    #A descriptor for country fields on a model instance. Returns a Country when
    #accessed so you can do things like::

        #>>> from people import Person
        #>>> person = Person.object.get(name='Chris')

        #>>> person.country.name
        #'New Zealand'

        #>>> person.country.flag
        #'/static/flags/nz.gif'
    #"""
    #def __init__(self, field):
        #self.field = field

    ##def __get__(self, instance=None, owner=None):
        ##print('__get__:')
        ##if instance is None:
            ##return self
        ### Check in case this field was deferred.
        ##if self.field.name not in instance.__dict__:
            ##instance.refresh_from_db(fields=[self.field.name])
        ##value = instance.__dict__[self.field.name]
        ##print(str(value))

        ###if self.field.multiple:
        ##if isinstance(value, list):
            ##return [self.field.LanguageChoices.get_language(code) for code in value]
        ##return self.field.LanguageChoices.get_language(value)

    #def _to_code(self, value):
        #if (isinstance(value, Language)):
            #return value.code3
        #else:
            #return value
            
    #def __set__(self, instance, value):
        #print('__set__:')
        ##if self.field.multiple:
        #if isinstance(value, list):
            #r = [self._to_code(l) for l in value]
        #else:
            #r = self._to_code(value)
        #print(str(r))
        #instance.__dict__[self.field.name] = r



#! null not allowed
#? fix errors
#! default should be valid country code
#! multiple works?
#? can set setobject to work?
#! error cases?
#! what is called where and when?

class LanguageField(CharField):
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }
    
    #LanguageChoices = LanguageChoices(pk_in=DJANGO_TRANSLATED)
    LanguageChoices = LanguageChoices(pk_in=UNITED_NATIONS)
    #descriptor_class = LanguageDescriptor


    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        # strip=True,
        
        # Local import so the languages aren't loaded unless they are needed.
        LanguageChoices = kwargs.pop('LanguageChoices', None)
        # languages default is Django languages
        if LanguageChoices:
            self.LanguageChoices = LanguageChoices
        self.blank_label = kwargs.pop('blank_label', None)
        #! what? where?
        #kwargs['empty_value'] = 'und'
        self.multiple = kwargs.pop('multiple', None)
        kwargs['choices'] = self.LanguageChoices
        if self.multiple:
            kwargs['max_length'] = len(self.LanguageChoices) * 3
        else:
            kwargs['max_length'] = 3

        #kwargs.setdefault('max_length', 3)
        #kwargs.setdefault('choices', LANGUAGES)
        super(CharField, self).__init__(*args, **kwargs)


    #def contribute_to_class(self, cls, name):
        #super().contribute_to_class(cls, name)
        #setattr(cls, self.name, self.descriptor_class(self))

    def deconstruct(self):
        # NB: no ``blank_label`` property, as this isn't database related.
        name, path, args, kwargs = super().deconstruct()
        # is the LanguageChoices, allocated, so remove
        kwargs.pop('choices')
        # include multiple and the LanguageChoices
        if self.multiple:
            kwargs['multiple'] = self.multiple
        kwargs['LanguageChoices'] = self.LanguageChoices.__class__
        return name, path, args, kwargs

    def get_choices(
        self, 
        include_blank=True, 
        blank_choice=BLANK_CHOICE_DASH, 
        limit_choices_to=None
    ):
        # Need to provide a blank label.
        # our choices are auto-generated, so no internal-defined option
        #if self.blank_label:
        #    blank_choice = [('', self.blank_label)]
        #if self.multiple:
        #    include_blank = False
        include_blank =  False
        # blank_choice always used as there is no internal 'choices'
        # definition
        choices = super().get_choices(
            include_blank=include_blank, 
            blank_choice=blank_choice
        )
        print('choices:')
        print(str(choices))
        return choices
        
    def formfield(self, **kwargs):
        # need a multiple choices form
        argname = 'choices_form_class'
        if argname not in kwargs:
            if self.multiple:
                kwargs[argname] = TypedMultipleChoiceField
            else:
                kwargs[argname] = TypedChoiceField
        return super().formfield(**kwargs)

    #def get_prep_value(self, value):
        #"Python to database value."
        #print('get_prep_value:')
        #print(str(value))
        #if (isinstance(value, list)):
            #return ','.join(l.code3 for l in value)
        #else:
            #return value.code3

    def get_prep_value(self, value):
        "Python to database value."
        print('get_prep_value:')
        print(str(value))
        if (isinstance(value, list)):
            return ','.join(code for code in value)
        else:
            return value
            
    def _to_lang(self, value):
        if (isinstance(value, Language)):
            return value
            
        lang = None
        try:
            lang = self.LanguageChoices.get_language(value)
        except KeyError:
            raise ValidationError("Invalid value for this language LanguageChoices. code: '{}'".format(
            value
            ))
        return lang
        
    def _parse_codes_to_langs(self, langstr):
        b = []
        try:
            for code in langstr.split(','):
                b.append(self.LanguageChoices.get_language(code))
        except KeyError:
            raise ValidationError("Invalid value for this language LanguageChoices. code: '{}'".format(
            code
            ))
        return b
         
    #def from_db_value(self, value, expression, connection, context):
        #"Database value to Python."
        #print('from_db_value:')
        #print(str(value))
        #r = self._parse_codes_to_langs(value)
        #return r
    def from_db_value(self, value, expression, connection, context):
        "Database value to Python."
        print('from_db_value:')
        print(str(value))
        b = []
        for code in value.split(','):
            b.append(code)
        return b
        
    #def to_python(self, value):
        #"Deserialization and clean to Python."
        #print('to_python')
        #print(str(value))
        #if (isinstance(value, list)):
            #return [self._to_lang(e) for e in value]
        #else:
          #return self._to_lang(value)

    def to_python(self, value):
        "Deserialization and clean to Python."
        print('to_python')
        print(str(value))
        if (isinstance(value, list)):
            return [super(LanguageField, self).to_python(e) for e in value]
        else:
          return super(LanguageField, self).to_python(value)
          
    #def validate(self, value, model_instance):
        #print('validate:')
        #print(str(value))
        #if not self.editable:
            ## Skip validation for non-editable fields.
            #return
            
        ## super tests for editable, checks choices, checks blanks
        #if (not isinstance(value, list)):
            #code = value.code3
            #if not code in self.LanguageChoices:
                #raise exceptions.ValidationError(
                    #self.error_messages['invalid_choice'],
                    #code='invalid_choice',
                    #params={'value': code},
                #)
        #else:
            #for lang in value:
                #if not lang.code3 in self.LanguageChoices:
                    #raise exceptions.ValidationError(
                        #self.error_messages['invalid_choice'],
                        #code='invalid_choice',
                        #params={'value': lang.code3},
                    #)

    def validate(self, value, model_instance):
        print('validate:')
        print(str(value))
        if not self.editable:
            # Skip validation for non-editable fields.
            return
            
        # super tests for editable, checks choices, checks blanks
        if (not isinstance(value, list)):
            if not value in self.LanguageChoices:
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': value},
                )
        else:
            for code in value:
                if not code in self.LanguageChoices:
                    raise ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': code},
                    )
