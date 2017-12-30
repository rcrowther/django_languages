from django.db.models.fields import CharField, BLANK_CHOICE_DASH
from django.forms.fields import TypedChoiceField, TypedMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core import checks

from .language_choices import LanguageChoices
from .lang_models import Language, EmptyLanguage
from .selectors import DJANGO_TRANSLATED, UNITED_NATIONS





#? duplicates are passing?
#! README
#? style
#? more presets
#? weak ref to page base out of memory?
class LanguageField(CharField):
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }
    
    # cached away from 'choices', so the queryset is available
    lang_choices = LanguageChoices()

    """
    A language field for Django models.
    """
    def __init__(self, *args, **kwargs):
        lang_choices = kwargs.pop('lang_choices', None)
        if lang_choices:
            self.lang_choices = lang_choices
        self.blank_label = kwargs.pop('blank_label', None)
        self.multiple = kwargs.pop('multiple', None)
        kwargs['choices'] = self.lang_choices
        if self.multiple:
            kwargs['max_length'] = len(self.lang_choices) * 3
        else:
            kwargs['max_length'] = 3
        super(CharField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_not_null())
        errors.extend(self._check_multiple_mul())
        errors.extend(self._check_blank_und())
        errors.extend(self._check_multiple_blank())
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
                hint='These are different names for the same condition. '
                'The condition is not forbidden. '
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
                hint='These may be different names for the same condition. '
                'The configuration is not forbidden. '
                'blank=True writes an empty string to the database, "und" is used by ISO for "undefined".'
                'They may express different types of non-definition?',
            )
        ]

    def _check_multiple_blank(self):
        if (not (self.multiple and self.blank)):
            return []
        return [
            checks.Error(
                'Field specifies multiple=True and blank=True.',
                obj=self,
                id='django_languages.E004',
                hint='blank entries can not be highlighted. '
                'This muddles the multiple widget display. '
                'Try propmoting "mul" or "und"?',
            )
        ]
        
    def deconstruct(self):
        # NB: no ``blank_label`` property, as this isn't database related.
        name, path, args, kwargs = super().deconstruct()
        # is the lang_choices, allocated, so remove
        kwargs.pop('choices')
        # include multiple and the lang_choices
        if self.multiple:
            kwargs['multiple'] = self.multiple
        kwargs['lang_choices'] = self.lang_choices #.__class__
        return name, path, args, kwargs

    def get_choices(
        self, 
        include_blank=True, 
        blank_choice=BLANK_CHOICE_DASH, 
        limit_choices_to=None
    ):
        # Need to provide a blank label.
        # our choices are auto-generated, so no internal-defined option
        if self.blank_label:
            blank_choice = [('', self.blank_label)]
        # defensive - it is checked
        if self.multiple:
            include_blank = False
        # NB: blank_choice always used as there is no internal 'choices'
        # definition for coders to interact with
        choices = super().get_choices(
            include_blank=include_blank, 
            blank_choice=blank_choice
        )
        return choices

    def _to_lang(self, value):
        if not value:
            return value
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
        if (isinstance(value, list)):
            return [self._to_lang(e) for e in value]
        else:
          return self._to_lang(value)
                  
    def formfield(self, **kwargs):
        # need a multiple choices form
        argname = 'choices_form_class'
        if argname not in kwargs:
            if self.multiple:
                kwargs[argname] = TypedMultipleChoiceField
            else:
                kwargs[argname] = TypedChoiceField
        if 'coerce' not in kwargs:
            kwargs['coerce'] = super().to_python
        return super().formfield(**kwargs)

    def _to_code(self, value):
        if (isinstance(value, Language)):
            return value.code3
        return value
          
    def get_prep_value(self, value):
        "Python to database value."
        if (isinstance(value, list)):
            return ','.join(self._to_code(l) for l in value)
        else:
            return self._to_code(value)
                  
    def _parse_codes_to_langs(self, langstr):
        b = []
        try:
            for code in langstr.split(','):
                # can be empty string for blank
                # no need to add a blank option, Django creates
                if code:
                    b.append(self.lang_choices.queryset[code])
        except KeyError:
            raise ValidationError("Invalid value supplied for choices. code: '{}'".format(
            code
            ))
        return b
         
    def from_db_value(self, value, expression, connection, context):
        "Database value to Python."
        r = self._parse_codes_to_langs(value)
        return r
        
    def to_python(self, value):
        "Deserialization and clean to Python."
        if (isinstance(value, list)):
            return [self._to_lang(e) for e in value]
        else:
          return self._to_lang(value)
  
    def _validate_code(self, value):
        if not value.code3 in self.lang_choices.queryset:
            raise ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': lang.code3},
            )      
            
    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return
                       
        if (not isinstance(value, list)):
            # brief validation for blank fields.
            if not value:
                if not self.blank:
                    raise exceptions.ValidationError(
                        self.error_messages['blank'], code='blank')
                else:
                    return
            self._validate_code(value)
        else:
            for v in value:
                self._validate_code(v)

