import collections

Language = collections.namedtuple('Language', 'code3 code2 scope type name')

EmptyLanguage = Language(code3='', code2='', scope='', type='', name='empty language')

LangData = collections.namedtuple('LangData', 'code name')
