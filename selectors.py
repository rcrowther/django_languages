

UNITED_NATIONS = [
    "ara", # Arabic
    "zho", # Chinese
    "eng", # English
    "fra", # French
    "rus", # Russian
    "spa", # Spanish
]

#  https://en.wikipedia.org/wiki/Languages_used_on_the_Internet
#  W3Techs estimate 2017
INTERNET_MOST_CONTENT = [
    "eng", # English
    "rus", # Russian
    "jpn", # Japanese
    "deu", # German
    "spa", # Spanish
    "fra", # French
    "por", # Portuguese
    "ita", # Italian
    "zho", # Chinese
    "pol", # Polish
    "tur", # Turkish
    "fas", # Persian
    "nld", # Dutch
    "kor", # Korean
    "ces", # Czech
    "ara", # Arabic
    "vie", # Vietnamese
    "ind", # Indonesian
    "ell", # Greek
    "swe", # Swedish
    "ron", # Romanian
    "hun", # Hungarian
    "dan", # Danish
    "tha", # Thai
    "slk", # Slovak
    "fin", # Finnish
    "bul", # Bulgarian
    "heb", # Hebrew
    "lit", # Lithuanian
    "nor", # Norwegian
    "ukr", # Ukrainian
    "hrv", # Croatian
    "nob", # Norwegian Bokmål
    "srp", # Serbian
    "cat", # Catalan
    "slv", # Slovenian
    "lav", # Latvian
    "est", # Estonian
    "tam", # Tamil
]

#  Funredes/MAAYA Observatory
#  http://funredes.org/lc2017/
INTERNET_MOST_TRAFFIC = [
    "eng", # English
    "zho", # Chinese
    "spa", # Spanish
    "fra", # French
    "rus", # Russian
    "deu", # German
    "por", # Portugese
    "jpn", # Japanese
    "ara", # Arabic
    "hin", # Hindi
    "msa", # Malay
    "ita", # Italian
    "kor", # Korean
    "pol", # Polish
    "urd", # Urdu
]

#  django.conf.global_settings, 2017
#  
DJANGO_TRANSLATED = [
    'afr', # Afrikaans
    'ara', # Arabic
    'ast', # Asturian
    'aze', # Azerbaijani
    'bul', # Bulgarian
    'bel', # Belarusian
    'ben', # Bengali
    'bre', # Breton
    'bos', # Bosnian
    'cat', # Catalan
    'ces', # Czech
    'cym', # Welsh
    'dan', # Danish
    'deu', # German
    'dsb', # Lower Sorbian
    'ell', # Greek
    'eng', # English
    #'en-au', # Australian English
    #'en-gb', # British English
    'epo', # Esperanto
    'spa', # Spanish
    #'es-ar', # Argentinian Spanish
    #'es-co', # Colombian Spanish
    #'es-mx', # Mexican Spanish
    #'es-ni', # Nicaraguan Spanish
    #'es-ve', # Venezuelan Spanish
    'est', # Estonian
    'eus', # Basque
    'fas', # Persian
    'fin', # Finnish
    'fra', # French
    'fry', # Frisian
    'gle', # Irish
    'gla', # Scottish Gaelic
    'glg', # Galician
    'heb', # Hebrew
    'hin', # Hindi
    'hrv', # Croatian
    'hsb', # Upper Sorbian
    'hun', # Hungarian
    'ina', # Interlingua
    'ind', # Indonesian
    'ido', # Ido
    'isl', # Icelandic
    'ita', # Italian
    'jpn', # Japanese
    'kat', # Georgian
    'kaz', # Kazakh
    'khm', # Khmer
    'kan', # Kannada
    'kor', # Korean
    'ltz', # Luxembourgish
    'lit', # Lithuanian
    'lav', # Latvian
    'mkd', # Macedonian
    'mal', # Malayalam
    'mon', # Mongolian
    'mar', # Marathi
    'mya', # Burmese
    'nob', # Norwegian Bokmål
    'nep', # Nepali
    'nld', # Dutch
    'nno', # Norwegian Nynorsk
    'oss', # Ossetic
    'pan', # Punjabi
    'pol', # Polish
    'por', # Portuguese
    #'pt-br', # Brazilian Portuguese
    'ron', # Romanian
    'rus', # Russian
    'slk', # Slovak
    'slv', # Slovenian
    'sqi', # Albanian
    'srp', # Serbian
    #'sr-latn', # Serbian Latin
    'sve', # Swedish
    'swa', # Swahili
    'tam', # Tamil
    'tel', # Telugu
    'tha', # Thai
    'tur', # Turkish
    'tat', # Tatar
    'udm', # Udmurt
    'ukr', # Ukrainian
    'urd', # Urdu
    'vie', # Vietnamese
    'zoo', # Chinese
    #'zh-hans', # Simplified Chinese
    #'zh-hant', # Traditional Chinese
]

#  Nationalencyklopedin 2007
#  from https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers
MOST_SPEAKERS = [
    #  1 Mandarin Chinese 935
    "cmn", # Mandarin Chinese
    #  2 Spanish language 390
    "spa", # Spanish
    #  3 English language 365
    "eng", # English
    #  4 Hindi language 422
    'hin', # Hindi
    #  5 Arabic  280
    'ara', # Arabic
    #  6 Portuguese language 205
    'por', # Portuguese
    #  7 Bengali language 200
    'ben', # Bengali
    #  8 Russian language 160
    'rus', # Russian
    #  9 Japanese language 125
    'jpn', # Japanese
    #  10 Punjabi language 95
    'pan', # Punjabi
    #  11 German language 92
    'deu', # German
    #  12 Javanese language 82
    'jav', # Javanese
    #  13 Wu Chinese 80
    'wuu', # Wu Chinese
    #  14 Malay language 77
    'msa', # Malay (macrolanguage
    #  15 Telugu language 76
    'tel', # Telugu
    #  16 Vietnamese language 76
    'vie', # Vietnamese
    #  17 Korean language 76
    'kor', # Korean
    #  18 French language 75
    'fra', # French
    #  19 Marathi language 73
    'mar', # Marathi
    #  20 Tamil language 70
    'tam', # Tamil
    #  21 Urdu 66
    'urd', # Urdu
    #  22 Turkish language 63
    'tur', # Turkish
    #  23 Italian language 59
    'ita', # Italian
    #  24 Yue Chinese 59
    'yue', # Yue Chinese
    #  25 Thai language 56
    'tha', # Thai
    #  26 Gujarati language 49
    'gju', # Gujari
    #  27 Jin Chinese 48
    'cjy', # Jinyu Chinese
    #  28 Southern Min 47
    'nan', # Min Nan Chinese
    #  29 Persian language 45
    'fas', # Persian
    #  30 Polish language 40
    'pol', # Polish
    #  31 Pashto language 39
    'pst', # Central Pashto
    #  32 Kannada language 38
    'kan', # Kannada
    #  33 Xiang Chinese 38
    'hsn', # Xiang Chinese
    #  34 Malayalam language 38
    'mal', # Malayalam
    #  35 Sundanese language 38
    'sun', # Sundanese
    #  36 Hausa language 34
    'hau', # Hausa
    #  37 Odia language 33
    'ory', # Odia
    #  38 Burmese language 33
    'mya', # Burmese
    #  39 Hakka Chinese 31
    'hak', # Hakka Chinese
    #  40 Ukrainian language 30
    'ukr', # Ukrainian
    #  41 Bhojpuri language 29
    'bho', # Bhojpuri
    #  42 Tagalog language 28
    'tgl', # Tagalog
    #  43 Yoruba language 28
    'yor', # Yoruba
    #  44 Maithili language 27
    'mai', # Maithili
    #  45 Uzbek language 26
    'uzb', # Uzbek
    #  46 Sindhi language 26
    'snd', # Sindhi
    #  47 Amharic language 25
    'amh', # Amharic
    #  48 Fula language 24
    'ful', # Fulah
    #  49 Romanian language 24
    'ron', # Romanian
    #  50 Oromo language 24
    'orm', # Oromo
    #  51 Igbo language 24
    'ibo', # Igbo
    #  52 Azerbaijani language 23
    'aze', # Azerbaijani
    #  53 Awadhi 22
    'awa', # Awadhi
    #  54 Gan Chinese 22
    'gan', # Gan Chinese
    #  55 Cebuano language 21
    'ceb', # Cebuano
    #  56 Dutch language 21
    'nld', # Dutch
    #  57 Kurdish language 21
    'kur', # Kurdish
    #  58 Serbo-Croatian 19
    'hbs', # Serbo-Croatian
    #  59 Malagasy language 18
    'mlg', # Malagasy
    #  60 Saraiki language 17
    'skr', # Saraiki
    #  61 Nepali language 17
    'nep', # Nepali 
    #  62 Sinhalese language 16
    'sin', # Sinhala
    #  63 Chittagonian language 16
    'ctg', # Chittagonian
    #  64 Zhuang languages 16
    'zha', # Zhuang
    #  65 Khmer language 16
    'khm', # Central Khmer
    #  66 Turkmen language 16
    'tuk', # Turkmen
    #  67 Assamese language 15
    'asm', # Assamese
    #  68 Madurese language 15
    'mad', # Madurese
    #  69 Somali language 15
    'som', # Somali
    #  70 Marwari language 14
    'mwr', # Marwari
    #  71 Magahi language 14
    'mag', # Magahi
    #  72 Haryanvi language 14
    'bgc', # Haryanvi
    #  73 Hungarian language 13
    'hun', # Hungarian
    #  74 Chhattisgarhi language 12
    'hne', # Chhattisgarhi
    #  75 Greek language 12
    'ell', # Modern Greek 
    #  76 Chewa language 12
    'nya', # Nyanja
    #  77 Deccan language 11
    'dcc', # Deccan
    #  78 Akan language 11
    'aka', # Akan
    #  79 Kazakh language 11
    'kaz', # Kazakh
    #  80 Northern Min 14
    'mnp', # Min Bei Chinese
    #  81 Sylheti language 10.7
    'syl', # Sylheti
    #  82 Zulu language 10.4
    'zul', # Zulu
    #  83 Czech language 10.0
    'ces', # Czech
    #  84 Kinyarwanda 9.8
    'kin', # Kinyarwanda
    #  85 Dhundari language 9.6
    'dhd', # Dhundari
    #  86 Haitian Creole 9.6
    'hat', # Haitian
    #  87 Eastern Min 9.5
    'cdo', # Min Dong Chinese
    #  88 Ilocano language 9.1
    'ilo', # Iloko
    #  89 Quechua languages 8.9
    'que', # Quechua
    #  90 Kirundi 8.8
    'run', # Rundi
    #  91 Swedish language 8.7
    'swe', # Swedish
    #  92 Hmong language 8.4
    'hmn', # Hmong
    #  93 Shona language 8.3
    'sna', # Shona
    #  94 Uyghur language 8.2
    'uig', # Uighur
    #  95 Hiligaynon language 8.2
    'hil', # Hiligaynon
    #  96 Mossi language 7.6
    'mos', # Mossi
    #  97 Xhosa language 7.6
    'xho', # Xhosa
    #  98 Belarusian language 7.6
    'bel', # Belarusian
    #  99 Balochi language 7.6
    'bcc', # Southern Balochi
    #  100 Konkani language 7.4
    'kok', # Konkani 
]

