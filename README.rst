Django-languages
================
Some support for languages as data.

Please note that this app is not for internationalization, which is translation of the display text in a site etc. This app is for the input and handling of a language code as a field of data (thus it is much simpler than internationalization). The app may be used, for example, to record what languages a user speaks.

If a language is in the data within this app, it does not mean Django has translation ability for that language. If the 'language of Nih' is listed, Django may not be able to translate the 'language of Nih'. But this app can record that a person can speak the 'language of Nih'. 
 
Limitations
~~~~~~~~~~~~~
The app is grounded in 639-3, the (slightly contentious) ISO (more or less) standard. So it only deals in three-letter codes, not locale-like codes. That means, for example, the app can not express the full range of Django translations (as Django contains, for example, translations expressed using locale subtags like 'en-gb', 'en-as').

(on the other hand, 639-3 currently can express 7000+ languages in it's three-letter codes, and is a web standard)

Alternatives
~~~~~~~~~~~~~
A module called 'django-languages' already exists in the Python Software package index,
https://pypi.python.org/pypi/django-languages/0.1 . I have ignored this module. It is not updated for several years.

The app is based in a nice effort called https://github.com/audiolion/django-language-field . This was what I wanted, a form field, but was lacking several facilities (sort, query, etc.) I didn't know how to fork the project, and have now replaced all the code. 

Some django-languages facilities are taken from an excellent, long-standing django app, django-counties https://github.com/SmileyChris/django-countries/tree/master/django_countries (though I am some way from full replication). Like django-countries, this app is not Model-based.

There are several language apps (though not as many as 'countries' apps),

The original django-language-field,
    https://github.com/audiolion/django-language-field 

As a template tag django-languageselect,
    https://github.com/RegioHelden/django-languageselect
     
     
Model-based 
-----------
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
++++++++++++
Though the app has no database model, it provides an in-memory language 'base'. This contains much of the data from ISO 639-3. From there, you do a query.

The Queryset class
~~~~~~~~~~~~~~~~~~
A queryset is a result from the langbase. Of course, because the langbase is a crude in-memory item, the Queryset is not as sharp in it's queries as a database query language. But, for these purposes, it should be enough.

Form a queryset, ::

    QuerySet()

By default this will include the language data from 639-3 that can express Django translations.

Form a different set of language data, selecting by three-letter code, ::

    qs = QuerySet(pk_in=['eng', 'por', 'spn'])
    
See the data these codes have selected, ::

    for l in qs
        print(l)

Select only living languages (big list), ::

    qs = QuerySet(type_in=['L'])

See the `639-3 spec`_ for full details.

There is a twist. 639-3 includes some special codes for 'undefined' or 'not a language' marks. These are, by  default, exculded. You can put them back in,

    qs = QuerySet(special_pk_in=['und'])

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

First
+++++
Queryset can do a nice trick from 'django-countries', it can pull out some country data and put it first in the list. It can also repeat that data in the main list.

Sorting
+++++++
For more accurate sorting of translated country names, install the optional
pyuca_ package.

.. _pyuca: https://pypi.python.org/pypi/pyuca/

Unicode collation. Not customizable, but better than the usual.



The Field
~~~~~~~~~
