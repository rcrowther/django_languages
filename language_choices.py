
from django.utils.encoding import force_text
import locale
import collections
from itertools import chain, islice

from .langbase import LANGBASE
from .langbase_specials import LANGBASE_SPECIALS
from .lang_models import Language, LangData
from .selectors import UNITED_NATIONS, DJANGO_TRANSLATED

try:
    import pyuca
except ImportError:
    pyuca = None

# Use UCA sorting if it's available.
if pyuca:
    collator = pyuca.Collator()

    def sort_key(item):
        return collator.sort_key(item[1])
else:
    # if no UCA, use locale
    def sort_key(item):   
        return locale.strxfrm(item[1])   
        
           

class QuerySet():
    def __init__(self, langtuples):
        # make a new list so modifications to originals
        # have no effect i.e. on list level, now immutable 
        self._langtuples = list(langtuples)
        self._index = {l.code3:l for l in self._langtuples}

    def __bool__(self):
        return bool(self._index)
        
    def __contains__(self, code):
        # test code exists
        return (code in self._index)

    def __getitem__(self, key):
        # get by key
        return self._index[key]
        
    def __len__(self):
        return len(self._index)        

    def __str__(self):
        return ('<QuerySet len:{}>'.format(len(self)))
        
    def __repr__(self):
        b = []
        for i in self._langtuples:
            b.append(str(i))
        return ', '.join(b)
        

        
QuerySetEmpty = QuerySet(())




_query_template = '''\
for row in LANGBASE:
    if ({query}):  
        body.append(Language(*row))

'''
#? make full __getattr__
#? index respects two_letter_codes
from django.utils.deconstruct import deconstructible

@deconstructible
class LanguageChoices():
    '''
    List of language codes.

    The current langbase is a reduction of one from from SIL, 
    http://www-01.sil.org/iso639-3/iso-639-3.tab.
    
    It is organised thus,
    - Three-letter 639-3
    - Equivalent 639-1
    - Scope I(ndividual), M(acrolanguage)
    - Type A(ncient), C(onstructed), E(xtinct), H(istorical), L(iving), S(pecial)
    - Reference language name
    
    Macrolanguages are names for collections (e.g. 'ara' "arabic 
    languages"). 
    
    Note that specials do not appear (Scope/Type "S") in the main table.
    Specials are magic codes. They are in a separate table, with a 
    query by name. 'special_pk_in' can be,
    
    'mis'
        is a language, but no code for it. 
    'mul' 
        multiple languages
    'und' 
        undetermined (e.g. never got labeled)
    'zxx'
        not a human language (e.g. animal calls)
    Any of these can be used in the list. They appear at the end, 
    unless specials_at_end=False.Think before using these codes - they 
    express useful ideas in a standard form. But they may clash, for 
    example, with the use of a 'blank=True' option.
    
    Use the ..._in entries to specify data to match. By default, no 
    entries are returned.
    
    First entries are in declared order. The body entries are sorted if
    'sort' is True (if not, body entries are in databse order).
      
    Sorting opens a can of worms,
    https://stackoverflow.com/questions/1097908/how-do-i-sort-unicode-strings-alphabetically-in-python
    https://pypi.python.org/pypi/PyICU
    At present, if UCA is available 
    https://pypi.python.org/pypi/pyuca/1.2 (all Python solution), the 
    app uses it, otherwise it uses a locale sort. 
    
    @param pk_in use these codes [code, ...]
    @param override override a provided language with a new common name 
    Works on all entries, including firsts and specials [(code, common name)] 
    @param first data to go first in the list [codes]
    @param first_repeat repeat any items in 'first' in the main list
    @param sort sort the body, else leave in database order
    @param reverse reverse the sort order
    @param sort_key sort by this key. Can be none (no sorting, iterate as data supplied)
    '''
    pk_in = UNITED_NATIONS
    scope_in=[]
    type_in=[]
    special_pk_in=['und', 'mul', 'zxx']
        
    override={'spa' : 'Ole!', 'zxx' : 'gabble!'}
    first_pk_in=['ara', 'spa']
    first_repeat=True
    specials_at_end = True
    sort=True
    reverse = False
    two_letter_codes = False
    
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.queryset = QuerySetEmpty
        self._first_cache = []
        self._body_cache = []
        self._specials_cache = []
        self._code3_index = {}
        self._code2_index = {}
        self.cache_langmap()


    def _override_names(self, langcoll):
        b = []
        override_keys = self.override.keys()
        for l in langcoll:
            if (not(l.code3 in override_keys)):
                b.append(l)
            else:
                key = l.code3
                override_val = self.override[key]
                if override_val:
                    #b.append(l._replace(name=override_val))
                    l.name=override_val
                    b.append(l)
        return b
            
    def cache_langmap(self):
        # Dynamically construct the query
        pk_select = 'row[0] in self.pk_in' if self.pk_in else ''
        scope_select = 'row[2] in self.scope_in' if self.scope_in else ''
        type_select = 'row[3] in self.type_in' if self.type_in else ''
        select_tmpl = ' '.join((pk_select, scope_select, type_select))
        query_tmpl = _query_template.format(query=select_tmpl)
        # Execute the query in this namespace 
        body = []
        try:
            exec(query_tmpl) #in namespace
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + query_tmpl)

        # now query the specials
        specials = []
        for row in LANGBASE_SPECIALS:
            if (row[0] in self.special_pk_in):  
                specials.append(Language(*row))
                                    
        # add any overrides
        if (self.override):
            body = self._override_names(body)
            specials = self._override_names(specials)

        # The options for selecting and modifying data are done.
        # cache and build the queryset
        self.queryset = QuerySet(chain(body, specials))
        
        # get firsts
        first = [0] * len(self.first_pk_in)
        for idx, code in enumerate(self.first_pk_in):
            first[idx] = self.queryset[code]
        
        # if not repeating firsts, need to filter body
        if (not self.first_repeat):
            body = [l for l in body if (not (l[0] in self.first_pk_in))]

        # cache the completed iteration data
        self._first_cache = first
        self._body_cache = body
        self._specials_cache = specials

    def _translate_pair(self, lang):
        code = lang.code2 if (self.two_letter_codes and lang.code2) else lang.code3
        return LangData(code, force_text(lang.name))
        
    def __iter__(self):        
        # Yield countries that should be displayed first.            
        first = (self._translate_pair(lang) for lang in self._first_cache)

        body = (self._translate_pair(lang) for lang in self._body_cache)
        if (self.sort or self.reverse):   
            body = sorted(body, key=sort_key, reverse=self.reverse)
        specials = (self._translate_pair(lang) for lang in self._specials_cache)

        if (not self.specials_at_end):
           langs = chain(specials, first, body)
        else:
           langs = chain(first, body, specials)
        
        for entry in langs:
            yield entry 
 
    def __bool__(self):
        return len(self) != 0

    def __getitem__(self, index):
        """
        May be helpful to access choices by index.
        """
        try:
            return next(islice(self.__iter__(), index, index+1))
        except TypeError:
            return list(islice(self.__iter__(), index.start, index.stop,
                               index.step))

    def __len__(self):
        size = len(self._first_cache)
        size += len(self._body_cache)
        size += len(self._specials_cache)
        return size

    def __str__(self):
        return ('<LanguageChoices sort:{} len:{}>'.format(self.sort, len(self)))
        
    def __repr__(self):
        b = []
        for i in self:
            b.append(str(i))
        return ', '.join(b)
