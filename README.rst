Django-languages
================
Some support for languages as data.

Please note that this app is not for internationalization, which is translation of the display text in a site, alternative translations of output texts etc. This app is for the input and handling of a language code as a field of data (thus it is much simpler than internationalization). The app may be used, for example, to record what languages a user speaks.

If a language is in the data within this app, it does not mean Django has translation ability for that language. If the 'language of Nih' is listed, Django may not be able to translate, or have translations for, the 'language of Nih'. But this app can record that a person can speak the 'language of Nih'. 
 
 
Alternatives
=============
A module called 'django-languages' already exists in the Python Software package index,
https://pypi.python.org/pypi/django-languages/0.1 . I have ignored this module. It is not updated for several years.

The app is based in a nice effort called https://github.com/audiolion/django-language-field . This was what I wanted, a form field, but was lacking several facilities (sort, query, etc.)

I have pushed django-languages towards the facilities offered by an excellent, long-standing django app, django-counties https://github.com/SmileyChris/django-countries/tree/master/django_countries (though I am some way from full replication). Like django-countries, the app is not Model-based.

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
There are many language classifications available. Sets that attempt to cover all/most languages are the size of books. This is unusable/unwanted for most computing environments.

I've provided,

- a programming-language locale-like set. 

    This is constructed from ISO 3166-1 alpha-2 (2-letter country) and ISO 639 (language) codes. It is not a mark as defined in any programming language, but close. xxx entries.

- ISO 639-1

    2 letter codes. As used by Wikipedia and other web software to identify general language speaking areas. 184 entries.
    
- ISO 639-2
    3-letter codes. As used incresingly in areas of computing sensitive to languages, or needing finer classification. 464 entries.

A reduced list
~~~~~~~~~~~~~~
Sometimes it is ok to generalize i.e. all that is needed is a broad idea of where a language is located.


Avoided
+++++++++
https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory


Maybe I will do?
+++++++++++++++++++++
https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers .
    Arguable but useful 

https://en.wikipedia.org/wiki/Language_family
    Would do justice to Eskimo and Tibetian, but has confusing nomenclature,


You get
+++++++
https://en.wikipedia.org/wiki/Languages_used_on_the_Internet
    Useful, expected, if majority bias. I removed Norwegian Bokmål because, as far as I know (very little), the situation in Norway is more involved, and the simple split does no justice here. Catalan is present. Mix of 2 and 3 letter ISO codes. 38 entries.

Django translations from django.conf.global_settings
    Bias, in a wierd way (Django users). But an interesting list which picks it's way between high web-usage languages 'Tamil', and political issues, 'Afrikaans', 'Catalan'.  Mix of 2 and 3 letter ISO codes with extensions, locale-like e.g. 'it', 'en-gb' 88 entries.
    
Both the above cover the official UN languages; Arabic, Chinese, English, French, Russian and Spanish. They are likely usable for internet and western commerce/academia. They will fail general and specialist cases. For example, Turkish and African languages are not well-represented.
