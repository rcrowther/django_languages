
from django.utils.encoding import force_text
import locale
import collections
#from operator import itemgetter

from .langbase import LANGBASE
from .regenerate import Language

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

class QuerySet():
    '''
    List of language codes.

    The current langbase is a reduction of one from from SIL, 
    http://www-01.sil.org/iso639-3/iso-639-3.tab.
    
    It is organised thus,
    - Three-letter 639-3
    - Equivalent 639-1
    - Scope I(ndividual), M(acrolanguage), S(pecial)
    - Type A(ncient), C(onstructed), E(xtinct), H(istorical), L(iving), S(pecial)
    - Reference language name
    
    Macrolanguages are names for collections (e.g. 'ara' "arabic 
    languages"). Specials are magic codes like 'mul' 
    (multiple languages) or 'und' (undetermined).
    
    Sorting opens a can of worms,
    https://stackoverflow.com/questions/1097908/how-do-i-sort-unicode-strings-alphabetically-in-python
    https://pypi.python.org/pypi/PyICU
    At present, if UCA is available 
    https://pypi.python.org/pypi/pyuca/1.2 (all Python solution), the 
    app uses it, otherwise it uses a locale sort.
    
    @param pk_in use these codes [code, ...]
    @param override override a provided language with a new common name [(code, common name)] 
    @param first data to go first in the list [codes]
    @param first_repeat repeat any items in 'first' in the main list
    @param reverse reverse the sort order
    @param sort_key sort by this key. Can be none (no sorting, iterate as data supplied)
    '''
    languages = []
    #pk_in=None
    #scope_in=None
    #type_in=None
    pk_in=['cym', 'glv']
    scope_in=[]
    type_in=[]
        
    override={}
    first=[]
    first_repeat=False
    reverse = False
    two_letter_code = False
        
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._first_cache = []
        self._body_cache = []

    def translate_pair(self, lang):
        return LangData(lang[0], force_text(lang[1]))
        
    #def to2lettercode(self, lang):
    #    return 
        
    #@property
    def cache_langmap(self):
        # Dynamically construct the query
        # then fill in the query action template
        pk_select = 'row[0] in self.pk_in' if self.pk_in else ''
        scope_select = 'row[2] in self.scope_in' if self.scope_in else ''
        type_select = 'row[3] in self.type_in' if self.type_in else ''
        select_tmpl = ' '.join((pk_select, scope_select, type_select))
        query_tmpl = _query_template.format(query=select_tmpl)
        
        # Execute the query in this namespace 
        b = []
        try:
            exec(query_tmpl) #in namespace
        except SyntaxError as e:
            raise SyntaxError(e.message + ':\n' + query_tmpl)

        ###
                # use the list from Django as default
                #from django.conf.global_settings import LANGUAGES as DJANGO_LANGDATA
                #languages = DJANGO_LANGDATA
        languages = b
                    
        # patch overrides
        if (self.override):
            b = []
            override_keys = self.override.keys()
            for l in languages:
                if (not(l[0] in override_keys)):
                    b.append(l)
                else:
                    key = l[0]
                    override_val = self.override[key]
                    if override_val:
                        b.append((key, override_val))
            languages = b
       

        #grab or extract first
        first = [0] * len(self.first)
        b = []
        if (self.first):
            for l in languages:
                if (not(l[0] in self.first)):
                    b.append(l)
                else:                
                    idx = self.first.index(l[0])   
                    if (not(self.first_repeat)):
                        first[idx] = l
                    else:
                        first[idx] = (l[0], l[1])
                        b.append(l)
            languages = b
            
        #if (self.two_letter_code):
        #   languages = [self.to2lettercode(l) for l in languages]
        print(str(first))
        self._first_cache = first
        self._body_cache = languages

                  
    def __iter__(self):
        self.cache_langmap()
        
        # Yield countries that should be displayed first.
        first = (
            self.translate_pair(lang)
            for lang in self._first_cache
        )

        for item in first:
            yield item
            
        body = (
            self.translate_pair(lang)
            for lang in self._body_cache
        )            
        
        for item in sorted(body, key=sort_key, reverse=self.reverse):
            yield item
            
    def __len__(self):
        size = len(self._first_cache)
        size += len(self._body_cache)
        return size
