#!/usr/bin/env python
"""
To regenerate that module to contain the latest list of  IANA Language
Subtag Registry, either call this module directly from the command line
(``python regenenerate.py``), or call the ``regenerate`` method.
Copy
http://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt
to
iso2.txt

Copy,
http://www-01.sil.org/iso639-3/iso-639-3.tab
to
iso3.txt

attributation: www.sil.org/iso639-3/ 
"""
import os
import re
import codecs
import urllib
from .lang_models import Language
#from .internet_langs import INTERNET_LANGS

#! backup before write

#LangDataISO2 = collections.namedtuple('LangDataISO2', 'code3 code2 name')
#Language = collections.namedtuple('Language', 'code3 code2 scope type name')

def langdataISO3():
    location='http://www-01.sil.org/iso639-3/iso-639-3.tab'
    data = urllib.request.urlopen(location)    
    content = data.read().decode('utf-8')

    languages = []
    for line in content.splitlines():
            data = line.split('\t')
            lang = Language(code3=data[0], code2=data[3], scope=data[4], type=data[5], name=data[6])
            languages.append(lang)
    return languages[1:]
    
        
#def langdataISO2(basename='iso2.txt'):


    ##location='http://www.iana.org/assignments/language-subtag-registry'
    ##lineRE = re.compile('\w\w\w\|[^|]*\|\w\w\|[^|]*\|')
    #sdir = os.path.dirname(os.path.abspath(__file__))
    #filename = os.path.join(sdir, basename)

    ## Get the language list.
    #languages = []
    #with open(filename, 'r') as f:
        #for line in f:
            #data = line.split('|')
            #name_elem = data[3].split(';', 1)
            #name = name_elem[0]
            ## Wrote 486 languages.
            ## Wrote 425 languages.
            #if (not ' languages' in name):
                #lang = LangDataISO2(code3=data[0], code2=data[2], name=name)
                #languages.append(lang)
    #return languages
        
        
        
        
TEMPLATE = u'''# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

{varname} = (
    {langdata}
)

'''


# {'Subtag': 'zbw', 'Added': '2009-07-29', 'Description': 'West Berawan', 'Type': 'language'}
def languages(location='http://www.iana.org/assignments/language-subtag-registry', default_encoding='utf-8'):
    paren = re.compile('\([^)]*\)')

    # Get the language list.
    data = urllib.request.urlopen(location)
    if ('content-type' in data.headers and
                'charset=' in data.headers['content-type']):
        encoding = data.headers['content-type'].split('charset=')[-1]
    else:
        encoding = default_encoding
    content = data.read().decode(encoding)
    languages = []
    info = {}
    p = None
    for line in content.splitlines():
        if line == '%%':
            if 'Type' in info and info['Type'] == 'language':
                languages.append(info)
            info = {}
        elif ':' not in line and p:
            info[p[0]] = paren.sub('', p[2]+line).strip()
        else:
            p = line.partition(':')
            if not p[0] in info: # Keep the first description as it should be the most common
                info[p[0]] = paren.sub('', p[2]).strip()
    return languages
  
  
def write_langfile(basename, varname, langlines):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), basename)
    with open(filename, 'w') as f:
        f.write(TEMPLATE.format(
            varname=varname,
            langdata='\n    '.join(langlines),
        ))
    print('Wrote {0} languages.'.format(len(langlines)))
          
# Wrote 8126 languages.
# Wrote 41 languages.
def regenerate(filename=None):
    """
    Generate the language data
    """
    #langdata = languages()
    #lines = ['("{0}", _(u"{1}")),'.format(l['Subtag'], l['Description']) for l in langdata]
    #write_langfile('languages.py', varname='IANA_LANGDATA', langlines=lines)
            
    #print( str(INTERNET_LANGS))

    #filtered_langdata = [l for l in langdata if l['Description'] in INTERNET_LANGS]
    #! need to uniquify
    #filtered_lines = ['("{0}", _(u"{1}")),'.format(l['Subtag'], l['Description']) for l in filtered_langdata]
    #write_langfile('internet_languages.py', varname='INTERNET_LANGDATA', langlines=filtered_lines)
        
    #langdata = langdataISO2()
    #lines = ['("{0}", _(u"{1}")),'.format(l.code3, l.name) for l in langdata]
    #write_langfile('langdata_iso2_alpha3.py', varname='ALPHA3_LANGDATA', langlines=lines)

    #lines = ['("{0}", _(u"{1}")),'.format(l.code2 if l.code2 else l.code3, l.name) for l in langdata]
    #write_langfile('langdata_iso2_alpha23.py', varname='ALPHA23_LANGDATA', langlines=lines)

    langdata = langdataISO3()
    lines = ['("{0}", "{1}", "{2}", "{3}", _(u"{4}")),'.format(l.code3, l.code2, l.scope, l.type, l.name) for l in langdata if not l.scope == "S"]
    write_langfile('langbase.py', varname='LANGBASE', langlines=lines)
    lines = ['("{0}", "{1}", "{2}", "{3}", _(u"{4}")),'.format(l.code3, l.code2, l.scope, l.type, l.name) for l in langdata if l.scope == "S"]
    write_langfile('langbase_specials.py', varname='LANGBASE_SPECIALS', langlines=lines)


if __name__ == '__main__':
    languages_lines = regenerate()
    print("")
