from django.db.models.fields import CharField, BLANK_CHOICE_DASH
from django.forms.fields import MultipleChoiceField, TypedMultipleChoiceField
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
#from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA
from .queryset import QuerySet
from .lang_models import Language, EmptyLanguage
from .selectors import DJANGO_TRANSLATED




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

    #def get_internal_type(self):
        # ensure it's a charfield
        #return "CharField"

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
        return super().get_choices(
            include_blank=include_blank, 
            blank_choice=blank_choice
        )

    def formfield(self, **kwargs):
        # need a multiple choices form
        argname = 'choices_form_class'
        if argname not in kwargs:
            if self.multiple:
                kwargs[argname] = TypedMultipleChoiceField
            else:
                kwargs[argname] = TypedChoiceField
        field = super().formfield(**kwargs)
        return field

    def get_prep_value(self, value):
        "Python to database value."
        print('get_prep_value:')
        print(str(value))
        #if isinstance(value, str):
            #?
            #return super().get_prep_value(value)
        if not self.multiple:
            return value.code3
        return ','.join(l.code3 for l in value)

    def _code_to_lang(self, langstr):
        lang = None
        try:
            lang = self.queryset.get_language(langstr)
        except KeyError:
            raise ValidationError("Invalid value for this language queryset. code: '{}'".format(
            langstr
            ))
        return lang

    def _codes_to_langs(self, langs_str, sep=','):
        b = []
        try:
            for code in langs_str(sep):
                b.append(self.queryset.get_language(code))
        except KeyError:
            raise ValidationError("Invalid value for this language queryset. code: '{}'".format(
            code
            ))
        return b
                            
    def _parse_codes_to_langs(self, langstr, sep=','):
        b = []
        try:
            for code in langstr.split(sep):
                b.append(self.queryset.get_language(code))
        except KeyError:
            raise ValidationError("Invalid value for this language queryset. code: '{}'".format(
            code
            ))
        return b
         
    def from_db_value(self, value, expression, connection, context):
        "Database value to Python."
        print('from_db_value:')
        print(str(value))
        if not self.multiple:
            return self._code_to_lang(value)
        return self._parse_codes_to_langs(value, ',')
        
    def to_python(self, value):
        "Deserialozation and clean to Python."
        print('to_python')
        print(str(value))
        if (isinstance(value, Language)):
            return value
        if not self.multiple:
            return self._code_to_lang(value)
        return self._codes_to_langs(value, ',')

    def validate(self, value, model_instance):
        print('validate:')
        print(str(value))
        print(str(self.empty_values))
        if not self.editable:
            # Skip validation for non-editable fields.
            return
            
        # super tests for editable, checks choices, checks blanks
        if not self.multiple:
            code = value.code3
            if not code in self.queryset:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': code},
                )
        else:
            for lang in value:
                if not lang.code3 in self.queryset:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': lang.code3},
                    )
