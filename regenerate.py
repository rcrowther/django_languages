#!/usr/bin/env python3
"""
To regenerate the langbase from ISO 369-3, either call this module directly from the command line
(``python regenenerate.py``), or call the ``regenerate`` method.

Copy,
http://www-01.sil.org/iso639-3/iso-639-3.tab
to
iso3.txt

attributation: www.sil.org/iso639-3/ 
"""
import os
import re
import codecs
from urllib import request
from lang_models import Language

#! backup before write

def langdataISO3():
    location='http://www-01.sil.org/iso639-3/iso-639-3.tab'
    data = request.urlopen(location)    
    content = data.read().decode('utf-8')

    languages = []
    for line in content.splitlines():
            data = line.split('\t')
            lang = Language(code3=data[0], code2=data[3], scope=data[4], type=data[5], name=data[6])
            languages.append(lang)
    return languages[1:]
        
        
        
TEMPLATE = u'''# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

{varname} = (
    {langdata}
)

'''
  
def write_langfile(basename, varname, langlines):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), basename)
    with open(filename, 'w') as f:
        f.write(TEMPLATE.format(
            varname=varname,
            langdata='\n    '.join(langlines),
        ))
    print('Wrote {0} languages.'.format(len(langlines)))
          
def regenerate(filename=None):
    """
    Generate the language data
    """
    print('Generating files.')
    print('Please wait, this can take some time...')
    langdata = langdataISO3()
    lines = ['("{0}", "{1}", "{2}", "{3}", _(u"{4}")),'.format(l.code3, l.code2, l.scope, l.type, l.name) for l in langdata if not l.scope == "S"]
    write_langfile('langbase.py', varname='LANGBASE', langlines=lines)
    lines = ['("{0}", "{1}", "{2}", "{3}", _(u"{4}")),'.format(l.code3, l.code2, l.scope, l.type, l.name) for l in langdata if l.scope == "S"]
    write_langfile('langbase_specials.py', varname='LANGBASE_SPECIALS', langlines=lines)
    print('Done')

if __name__ == '__main__':
    regenerate()
