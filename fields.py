from django.db.models.fields import CharField, BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _

#from .languages import IANA_LANGDATA
#from .internet_languages import INTERNET_LANGDATA
#from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA
from .queryset import QuerySet
from .selectors import DJANGO_TRANSLATED

#! display code or common lamguage name
#! select vurrent choice

class LanguageField(CharField):
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }
    
    queryset = QuerySet(pk_in=DJANGO_TRANSLATED)


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
        self.languages_flag_url = kwargs.pop('languages_flag_url', None)
        self.blank_label = kwargs.pop('blank_label', None)
        #! what? where?
        #kwargs['empty_value'] = 'und'
        self.multiple = kwargs.pop('multiple', None)
        kwargs['choices'] = self.queryset
        if self.multiple:
            kwargs['max_length'] = len(self.queryset) * 5 - 1
        else:
            kwargs['max_length'] = 3
            #! what? where?
            #kwargs['min_length'] = 2

        #kwargs.setdefault('max_length', 3)
        #kwargs.setdefault('choices', LANGUAGES)
        super(CharField, self).__init__(*args, **kwargs)


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
            include_blank=include_blank, blank_choice=blank_choice, *args,
            **kwargs)

    def formfield(self, **kwargs):
        # need a muliple choices form
        argname = 'choices_form_class'
        if argname not in kwargs:
            if self.multiple:
                kwargs[argname] = TypedMultipleChoiceField
            #else:
            #    kwargs[argname] = TypedChoiceField
        field = super().formfield(**kwargs)
        return field
        
    def to_python(self, value):
        if not self.multiple:
            return super().to_python(value)
        if not value:
            return value
        output = []
        for item in value:
            output.append(super().to_python(item))
        return output
        
    def validate(self, value):
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

#class LanguageField(ChoiceField):
    #choices = QuerySet(pk_in=DJANGO_TRANSLATED)

    #def __init__(self, **kwargs):
        #super().__init__(**kwargs)
        #self.choices = choices
        #choices = kwargs.pop('choices', None)
        ### languages default is Django languages
        #if choices:
            #self.choices = choices
            
