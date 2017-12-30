import collections

#Language = collections.namedtuple('Language', 'code3 code2 scope tpe name')



class Language(object):
    __slots__ = ['code3', 'code2', 'scope', 'tpe', 'name']

    def __init__(self, code3, code2, scope, tpe, name):
        self.code3=code3 
        self.code2=code2 
        self.scope=scope 
        self.tpe=tpe 
        self.name=name
    
    def __hash__(self):
        return hash(code3)
    
    def __str__(self):
        # Consider carefully before changing this, even if the return
        # breaks the usual convention of __str__ (it *should* be nicely
        # printable and non-eval).
        # Django code (verification, etc.) stringifies the field value 
        # before reaching the model and rendering the 'choices' 
        # attribute. In the current code, this method must return a 
        # value to compare to the 'choices' tuple structure. That is, a 
        # string with the three-letter code. Otherwise, the comparision
        # will fail and the field results will not show the language
        # currently selected.
        return self.code3
        
    def __repr__(self):
        return '<Language "{0}", "{1}", "{2}", "{3}", "{4}">'.format(
            self.code3,
            self.code2, 
            self.scope, 
            self.tpe, 
            self.name
        )

EmptyLanguage = Language(code3='', code2='', scope='', tpe='', name='empty language')

'''
Small model representing a chosen code and common name.
Can be used to shape a Django choices structure.
'''
LangData = collections.namedtuple('LangData', 'code name')
