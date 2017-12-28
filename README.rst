Django-languages
================
A field for languages as data.

Please note that this app is not for internationalization, which is translation of the display text in a site etc. This app is for the input and handling of a language code as data (thus it is much simpler than internationalization). The app may be used, for example, to record the languages a user speaks.

If a language is in the data within this app, it does not mean Django has translation ability for that language. If the 'language of Nih' is listed, Django may not be able to translate the 'language of Ni!'. But this app can record that a person can speak the 'language of Ni!' (oh no it can't. because ISO639-3 doesn't record 'Ni!' as a language, which it plainly is, even if it only has one word). 
 
Limitations
-----------
The app is grounded in 639-3, the (slightly contentious) ISO (more or less) standard. So it only deals in three-letter codes, not locale-like codes. That means, for example, the app can not express the full range of Django translations (as Django contains, for example, translations expressed using locale subtags like 'en-gb', 'en-as').

(on the other hand, 639-3 currently can express 7000+ languages in it's three-letter codes, and is a web standard)

Alternatives
------------
A module called 'django-languages' already exists in the Python Software package index,
https://pypi.python.org/pypi/django-languages/0.1 . I have ignored this module. It is not updated for several years.

The app was based in a app called https://github.com/audiolion/django-language-field . This was what I wanted, a form field, but was lacking several facilities (sort, query, etc.) I didn't know how to fork the project, and have replaced the code. 

Some django-languages facilities are taken from an excellent, long-standing django app, django-countries https://github.com/SmileyChris/django-countries/tree/master/django_countries (though I am some way from full replication). Like django-countries, this app is not Model-based.

There are several language apps (though not as many as 'countries' apps),

The original django-language-field,
    https://github.com/audiolion/django-language-field 

As a template tag django-languageselect,
    https://github.com/RegioHelden/django-languageselect
     
     
Model-based 
~~~~~~~~~~~
django-world-languages
    https://github.com/blag/django-world-languages

django-languages-plus. Works with 'django-countries',
    https://pypi.python.org/pypi/django-languages-plus/1.0.0


The app
-------

Language sets
~~~~~~~~~~~~~
There are many language classifications available. Sets that attempt to cover all/most languages are the size of books. I'm tired of apps that do not declare their intent (or bias) on this issue. And it is an issue.


The langbase
~~~~~~~~~~~~
Though the app has no database model, it provides an in-memory language 'base'. This contains much of the data from ISO 639-3. From there, you do a query.

The LanguageChoices class
~~~~~~~~~~~~~~~~~~~~~~~~~~
This class holds a result from the langbase. Of course, because the langbase is a crude in-memory item, the LanguageChoices is not as sharp in it's queries as a database query language. But, for these purposes, it should be enough.

LanguageChoices delivers a set of language pair tuples to a Django field. Within, it contains an attribute 'queryset', which can be queried for the language data held by the choices.

Form some choices, ::

    LanguageChoices()

By default this will include the language data from 639-3 that expresses the official languages of the United Nations.

Form a different set of language data, selecting by three-letter codes, ::

    lc = LanguageChoices(pk_in=['eng', 'por', 'spn'])
    
See the data these codes have selected, ::

    for l in lc:
        print(l)

To select only living languages (big list), use the 'type' column in the langbase ::

    lc = LanguageChoices(type_in=['L'])

See the `639-3 spec`_ for full details.

There is a twist. 639-3 includes some special codes for 'undefined' or 'not a language' marks. By default, the app excludes them. You can put them back in, ::

    lc = LanguageChoices(special_pk_in=['und'])

appends the und(efined) mark to the queryset.


Presets
+++++++
A few presets have been built for 'pk_in'. All are contentious. But then, if you are not contending this issue, why not?

UNITED_NATIONS
    Official languages of the UN. 6 entries.

INTERNET_MOST_CONTENT
    From https://en.wikipedia.org/wiki/Languages_used_on_the_Internet.
    Contentious subject, but a useful near-Europe set. 39 entries.
    
INTERNET_MOST_TRAFFIC
    From a Wikipedia link, a list contending the above and very 
    different (more coverage of languages from Asia). 15 entries.
     
DJANGO_TRANSLATED
    Django translations from django.conf.global_settings, 2017. Not exact; 
    some dialects dropped, and added plain Chinese.
    Will reflect areas with computing and Python coding. 78 entries.

Or make your own.

Other LanguageChoices options
++++++++++++++++++++++++++++++

override
    Change the common name of one of the languages e.g. override = {fra : "Chez nous"} 
     
First
    A trick from 'django-countries'. Pull out some country data and put it first in the list. It can also repeat that data in the main list.

Sorting
    For more accurate sorting of translated country names, install the optional pyuca_ package. Unicode collation. Not customizable, but better than usual.



The Field
~~~~~~~~~
Like this, in a model definition, ::

    from django_languages import LanguageField

        ...
        
        lang = LanguageField(
            "language",
            blank_label = 'Not stated...',
            multiple= False,
            default = 'fra',
            help_text="(main) Language of the text.",
        )
        
Getting and setting
+++++++++++++++++++
The field contains a trick, it coerces the simple three-letter code held in the database into a full Language class. The returned class instance contains the row data from the langbase. Assume TextModel has a LanguageField 'lang', ::

    >>> o = TextModel.objects.get(pk=1)
    >>> o.lang
    <Language "ara", "ar", "I", "L", "Arabic">
    >>> o.lang.name
    "Arabic"

You can also allocate by country, or three-letter code ::

    >>> o.lang = 'fra'
    >>> o.lang
    <Language "fra", "fr", "I", "L", "French">


Options
+++++++

blank_label
    The blank option will use text defined here (because the coder can not define the choice tuples for this field, this option can revise the 'blank' name).
  
multiple
    Use a multiple selector, for many languages
  
blank=True only works on single selectors/selections ('blank' can work oddly on multiple selectors). Alternatively, enable and promote the special 369-3 code 'und'(undedined). 

'default' and other Model field attributes should work as expected.


.. _pyuca: https://pypi.python.org/pypi/pyuca/

