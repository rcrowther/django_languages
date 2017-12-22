
from django.utils.encoding import force_text
import locale
import collections

from .langbase import LANGBASE
from .langbase_specials import LANGBASE_SPECIALS
from .language import Language
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
        
           

LangData = collections.namedtuple('LangData', 'code name')


_query_template = '''\
for row in LANGBASE:
    if ({query}):  
        b.append(Language(*row))

'''
#? make full __getattr__
#? index respects two_letter_codes
class QuerySet():
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
    Any of these can be used in the list. They appear at the end. 
    However, think before including 'und' - LanguageField uses this for 
    'blank'. If you are not sure, do not include.
    
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
    # Us DJANGO_TRANSLATED as default
    pk_in = UNITED_NATIONS
    #pk_in = DJANGO_TRANSLATED
    scope_in=[]
    type_in=[]
    special_pk_in=['mul', 'zxx']
        
    override={'spa' : 'Ole!', 'zxx' : 'gabble!'}
    first=['ara', 'spa']
    first_repeat=True
    sort=True
    reverse = False
    two_letter_codes = False
        
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._cache = []
        self._first_cache = []
        self._body_cache = []
        self._specials_cache = []
        self._code3_index = {}
        self._code2_index = {}
        self.cache_langmap()


    def override_names(self, langcoll):
        b = []
        override_keys = self.override.keys()
        for l in langcoll:
            if (not(l.code3 in override_keys)):
                b.append(l)
            else:
                key = l.code3
                override_val = self.override[key]
                if override_val:
                    b.append(l._replace(name=override_val))
        return b
            
    def cache_langmap(self):
        # Dynamically construct the query
        # then fill in the query action template
        pk_select = 'row[0] in self.pk_in' if self.pk_in else ''
        scope_select = 'row[2] in self.scope_in' if self.scope_in else ''
        type_select = 'row[3] in self.type_in' if self.type_in else ''
        select_tmpl = ' '.join((pk_select, scope_select, type_select))
        query_tmpl = _query_template.format(query=select_tmpl)
        #print('query_tmpl:')
        #print(query_tmpl)
        # Execute the query in this namespace 
        b = []
        try:
            exec(query_tmpl) #in namespace
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + query_tmpl)

        languages = b
                    
        # add any overrides
        if (self.override):
            languages = self.override_names(languages)

        # The options for selecting and modifying data are done.
        # cache and build an index
        self._cache = languages
        self._code3_index = {l.code3:l for l in self._cache}
        self._code2_index = {l.code2:l for l in self._cache if l.code2}
        #print('query:')
        #print(str(languages))
        
        #grab or extract first
        first = [0] * len(self.first)
        b = []
        if (self.first):
            for l in languages:
                if (not(l[0] in self.first)):
                    b.append(l)
                else:                
                    idx = self.first.index(l[0])   
                    first[idx] = l

                    if (self.first_repeat):
                        b.append(l)
            languages = b

        # Add specials to the end by name
        specials = []
        for row in LANGBASE_SPECIALS:
            if (row[0] in self.special_pk_in):  
                specials.append(Language(*row))
        # add any overrides
        specials = self.override_names(specials)
        
        #print(str(first))
        self._first_cache = first
        self._body_cache = languages
        self._special_cache = specials

    def get_name(self, code):
        return self._code3_index[code].name

    def get_language(self, code):
        return self._code3_index[code]


    def translate_pair(self, lang):
        code = lang.code2 if (self.two_letter_codes and lang.code2) else lang.code3
        return LangData(code, force_text(lang.name))
        
    def __iter__(self):        
        # Yield countries that should be displayed first.
        first = (self.translate_pair(lang) for lang in self._first_cache)
        for item in first:
            yield item
            
        body = (self.translate_pair(lang) for lang in self._body_cache)
        if self.sort:   
            for item in sorted(body, key=sort_key, reverse=self.reverse):
                yield item
        else:
            for item in body:
                yield item

        specials = (self.translate_pair(lang) for lang in self._special_cache)
        for entry in specials:
            yield entry
                
    def __bool__(self):
        return bool(self._cache)
                     
    def __contains__(self, code):
        # test code exists
        return (code in self._code3_index)

    def __getitem__(self, index):
        # get by index
        return self._cache[index]
        
    def __len__(self):
        size = len(self._first_cache)
        size += len(self._body_cache)
        return size

    #def __str__(self):

    def __repr__(self):
        b = []
        for i in self:
            b.append(str(i))
        return ', '.join(b)
