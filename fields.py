from django.db.models.fields import CharField, BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _

#from .languages import IANA_LANGDATA
#from .internet_languages import INTERNET_LANGDATA
#from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA
from .queryset import QuerySet
from .selectors import DJANGO_TRANSLATED




#! display code or common lamguage name
#! select vurrent choice
#! blank label works?
#! multiple works?
#? can set set object to work?
#! error cases?
#! what is called where and when?
#! empty valies?

class LanguageDescriptor(object):
    """
    A descriptor for country fields on a model instance. Returns a Country when
    accessed so you can do things like::

        >>> from people import Person
        >>> person = Person.object.get(name='Chris')

        >>> person.country.name
        'New Zealand'

        >>> person.country.flag
        '/static/flags/nz.gif'
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            return self
        # Check in case this field was deferred.
        if self.field.name not in instance.__dict__:
            instance.refresh_from_db(fields=[self.field.name])
        value = instance.__dict__[self.field.name]
        if self.field.multiple:
            return [self.queryset(code) for code in value]
        return self.queryset(value)

    #def country(self, code):
        #return Country(
            #code=code, flag_url=self.field.countries_flag_url,
            #custom_countries=self.field.countries)

    #def __set__(self, instance, value):
        #if self.field.multiple:
            ##if isinstance(value, (basestring, Language)):
            #if isinstance(value, str):
                #value = force_text(value).split('|')
            #value = [l.code3 for l in value]
        #else:
            #value = value.code3
        #instance.__dict__[self.field.name] = value



class LanguageField(CharField):
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }
    
    queryset = QuerySet(pk_in=DJANGO_TRANSLATED)

    descriptor_class = LanguageDescriptor


    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        # strip=True,
        
        # Local import so the languages aren't loaded unless they are needed.
        queryset = kwargs.pop('queryset', None)
        # languages default is Django languages
        if queryset:
            self.queryset = queryset
        #self.languages_flag_url = kwargs.pop('languages_flag_url', None)
        self.blank_label = kwargs.pop('blank_label', None)
        #! what? where?
        #kwargs['empty_value'] = 'und'
        self.multiple = kwargs.pop('multiple', None)
        kwargs['choices'] = self.queryset
        if self.multiple:
            kwargs['max_length'] = len(self.queryset) * 3
        else:
            kwargs['max_length'] = 3

        #kwargs.setdefault('max_length', 3)
        #kwargs.setdefault('choices', LANGUAGES)
        super(CharField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        # ensure it's a charfield
        return "CharField"

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))
        
    def deconstruct(self):
        # NB: no ``blank_label`` property, as this isn't database related.
        name, path, args, kwargs = super().deconstruct()
        # is the queryset, allocated, so remove
        kwargs.pop('choices')
        # include multiple and the queryset
        if self.multiple:
            kwargs['multiple'] = self.multiple
        kwargs['queryset'] = self.queryset.__class__
        return name, path, args, kwargs

    def get_choices(self, 
        include_blank=True, 
        blank_choice=BLANK_CHOICE_DASH, 
        limit_choices_to=None
    ):
        # Need to provide a blank label for auto-generated choices
        if self.blank_label:
            blank_choice = [('und', self.blank_label)]
        if self.multiple:
            include_blank = False
        return super().get_choices(
            include_blank=include_blank, blank_choice=blank_choice
            )

    def formfield(self, **kwargs):
        # need a multiple choices form
        argname = 'choices_form_class'
        if argname not in kwargs:
            if self.multiple:
                kwargs[argname] = TypedMultipleChoiceField
            #else:
            #    kwargs[argname] = TypedChoiceField
        field = super().formfield(**kwargs)
        return field

    def get_prep_value(self, value):
        "Python to database value."
        if isinstance(value, str):
            return super().get_prep_value(value)
        if not self.multiple:
            return value.code3
        return '|'.join(l.code3 for l in value)
            
    def _parse_multiple(self, langstr):
        b = []
        for l in langstr.split('|'):
             b.append(QuerySet.get_language(value))
        return b
         
    def from_db_value(self, value, expression, connection, context):
        "Database value to Python."
        if value is None:
            return value
        if not self.multiple:
            return self.queryset.get_language(value)
        return self._parse_multiple(value)
        
    def to_python(self, value):
        "Deserialozation and clean to Python."
        if not self.multiple:
            return super().to_python(value)
        if not value:
            return value
        return self._parse_multiple(value)

        
    def validate(self, value, model_instance):
        # super tests for editable, checks choices, checks blanks
        if not self.multiple:
            return super().validate(value, model_instance)

        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if value:
            for v in value:
                if v not in self.queryset:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': v},
                    )

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(
                self.error_messages['blank'], code='blank')
