from django.db.models.fields import CharField, BLANK_CHOICE_DASH
from django.forms.fields import TypedChoiceField, TypedMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core import checks
#from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA
from .language_choices import LanguageChoices
from .lang_models import Language, EmptyLanguage
from .selectors import DJANGO_TRANSLATED, UNITED_NATIONS





#? duplicates are passing?
#! default should be valid country code
#! error cases?
#! README
#? enable blank
#? style
#? more presets
#? choices init too complex?
class LanguageField(CharField):
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }
    
    #lang_choices = LanguageChoices(pk_in=DJANGO_TRANSLATED)
    lang_choices = LanguageChoices(pk_in=UNITED_NATIONS)

    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        # strip=True,
        lang_choices = kwargs.pop('lang_choices', None)
        if lang_choices:
            self.lang_choices = lang_choices
        self.blank_label = kwargs.pop('blank_label', None)
        #! what? where?
        #kwargs['empty_value'] = 'und'
        self.multiple = kwargs.pop('multiple', None)
        kwargs['choices'] = self.lang_choices
        if self.multiple:
            kwargs['max_length'] = len(self.lang_choices) * 3
        else:
            kwargs['max_length'] = 3

        #kwargs.setdefault('max_length', 3)
        #kwargs.setdefault('choices', LANGUAGES)
        super(CharField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_not_null())
        errors.extend(self._check_multiple_mul())
        errors.extend(self._check_blank_und())
        return errors

    def _check_not_null(self):
        if not self.null:
            return []
        return [
            checks.Error(
                'null=True not allowed on this field.',
                obj=self,
                id='django_languages.E001',
                hint='For unstated entries use blank=True, or ISO639-3 "und"',
            )
        ]
        
    def _check_multiple_mul(self):
        if (not (self.multiple and 'mul' in self.lang_choices.queryset)):
            return []
        return [
            checks.Warning(
                'Field specifies multiple=True, and "mul" available as a choice.',
                obj=self,
                id='django_languages.E002',
                hint='These are different names for the same condition.'
                'The condition is not forbidden.'
                'It may express "several"/"too many to list"?',
            )
        ]

    def _check_blank_und(self):
        if (not (self.blank and 'und' in self.lang_choices.queryset)):
            return []
        return [
            checks.Warning(
                'Field specifies blank=True, and "und" available as a choice.',
                obj=self,
                id='django_languages.E003',
                hint='These may be different names for the same condition.'
                'The configuration is not forbidden.'
                'blank=True writes an empty string to the database, "und" is used by ISO for "undefined".'
                'They may express different types of non-definition?',
            )
        ]
                
    def deconstruct(self):
        # NB: no ``blank_label`` property, as this isn't database related.
        name, path, args, kwargs = super().deconstruct()
        # is the LanguageChoices, allocated, so remove
        kwargs.pop('choices')
        # include multiple and the lang_choices
        if self.multiple:
            kwargs['multiple'] = self.multiple
        kwargs['lang_choices'] = self.lang_choices.__class__
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

    def _to_lang(self, value):
        if (isinstance(value, Language)):
            return value
        lang = None
        try:
            lang = self.lang_choices.queryset[value]
        except KeyError:
            raise ValidationError("Invalid value supplied for choices. code: '{}'".format(
            value
            ))
        return lang

    def _to_languages(self, value):
        #"Deserialization and clean to Python."
        print('_to_languages')
        print(str(value))
        if (isinstance(value, list)):
            return [self._to_lang(e) for e in value]
        else:
          return self._to_lang(value)
                  
    def formfield(self, **kwargs):
        print('formfield:')
        print(str(kwargs))
        # need a multiple choices form
        argname = 'choices_form_class'
        if argname not in kwargs:
            if self.multiple:
                kwargs[argname] = TypedMultipleChoiceField
            else:
                kwargs[argname] = TypedChoiceField
        #kwargs[argname].widget = Select2
        if 'coerce' not in kwargs:
            #kwargs['coerce'] = self._to_languages
            kwargs['coerce'] = super().to_python
        return super().formfield(**kwargs)

    def _to_code(self, value):
        if (isinstance(value, Language)):
            return value.code3
        return value
          
    def get_prep_value(self, value):
        "Python to database value."
        print('get_prep_value:')
        print(str(value))
        if (isinstance(value, list)):
            return ','.join(self._to_code(l) for l in value)
        else:
            return self._to_code(value)
                  
    def _parse_codes_to_langs(self, langstr):
        b = []
        try:
            for code in langstr.split(','):
                b.append(self.lang_choices.queryset[code])
        except KeyError:
            raise ValidationError("Invalid value supplied for choices. code: '{}'".format(
            code
            ))
        return b
         
    def from_db_value(self, value, expression, connection, context):
        "Database value to Python."
        print('from_db_value:')
        print(str(value))
        r = self._parse_codes_to_langs(value)
        return r
        
    def to_python(self, value):
        "Deserialization and clean to Python."
        print('to_python')
        print(str(value))
        if (isinstance(value, list)):
            return [self._to_lang(e) for e in value]
        else:
          return self._to_lang(value)
  
    def validate(self, value, model_instance):
        print('validate:')
        print(str(value))
        if not self.editable:
            # Skip validation for non-editable fields.
            return
            
        # super tests for editable, checks choices, checks blanks
        if (not isinstance(value, list)):
            code = value.code3
            if not code in self.lang_choices.queryset:
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': code},
                )
        else:
            for lang in value:
                if not lang.code3 in self.lang_choices.queryset:
                    raise ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': lang.code3},
                    )
