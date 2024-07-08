import re
from text.japanese import japanese_to_romaji_with_accent, japanese_to_ipa, japanese_to_ipa2, japanese_to_ipa3
from text.korean import latin_to_hangul, number_to_hangul, divide_hangul, korean_to_lazy_ipa, korean_to_ipa, fix_g2pk2_error
from g2pk2 import G2p
from text.mandarin import number_to_chinese, chinese_to_bopomofo, latin_to_bopomofo, chinese_to_romaji, chinese_to_lazy_ipa, chinese_to_ipa, chinese_to_ipa2
#from text.sanskrit import devanagari_to_ipa
from text.english import english_to_ipa, english_to_lazy_ipa, english_to_ipa2, english_to_lazy_ipa2
from text.thai import num_to_thai, latin_to_thai
#from viphoneme import vi2IPA
#from text.shanghainese import shanghainese_to_ipa
#from text.cantonese import cantonese_to_ipa
#from text.ngu_dialect import ngu_dialect_to_ipa
from unidecode import unidecode
from phonemizer import phonemize

from num2words import num2words
import epitran
import cn2an
import pykakasi
import re

g2p = G2p()
kks = pykakasi.kakasi()

ipa_en = epitran.Epitran('eng-Latn')
ipa_ko = epitran.Epitran('kor-Hang')
ipa_cn = epitran.Epitran('cmn-Hans', cedict_file='./cedict_1_0_ts_utf-8_mdbg.txt')
ipa_ja = epitran.Epitran('jpn-Hrgn')

ipa_vi = epitran.Epitran('vie-Latn')
ipa_id = epitran.Epitran('ind-Latn')
ipa_th = epitran.Epitran('tha-Thai')
ipa_ru = epitran.Epitran('rus-Cyrl')

_whitespace_re = re.compile(r'\s+')

# Regular expression matching Japanese without punctuation marks:
#_japanese_characters = re.compile(r'[A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# Regular expression matching non-Japanese characters or punctuation marks:
#_japanese_marks = re.compile(r'[^A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9fff\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text

def collapse_whitespace(text):
    return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
    return unidecode(text)


def basic_cleaners(text):
    # - For replication of https://github.com/FENRlR/MB-iSTFT-VITS2/issues/2
    # you may need to replace the symbol to Russian one
    '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
    text = text.lower()
    text = collapse_whitespace(text)
    return text

'''
def fix_g2pk2_error(text):
    new_text = ""
    i = 0
    while i < len(text) - 4:
        if (text[i:i+3] == 'ㅇㅡㄹ' or text[i:i+3] == 'ㄹㅡㄹ') and text[i+3] == ' ' and text[i+4] == 'ㄹ':
            new_text += text[i:i+3] + ' ' + 'ㄴ'
            i += 5
        else:
            new_text += text[i]
            i += 1

    new_text += text[i:]
    return new_text
'''

def english_cleaners(text):
  return english_to_ipa(text)

def english_cleaners2(text):
  return english_to_ipa2(text)

def espeak_en_cleaners(text): # needs espeak - apt-get install espeak
    text = convert_to_ascii(text)
    text = expand_abbreviations(text.lower())
    phonemes = phonemize(text, language='en-us', backend='espeak', strip=True, preserve_punctuation=True,with_stress=True)
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def espeak_ru_cleaners(text):
    text = convert_to_ascii(text)
    text = expand_abbreviations(text.lower())
    phonemes = phonemize(text, language='ru', backend='espeak', strip=True, preserve_punctuation=True,with_stress=True, language_switch='remove-flags',njobs=4)
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def espeak_vi_cleaners(text):
    text = convert_to_ascii(text)
    text = expand_abbreviations(text.lower())
    phonemes = phonemize(text, language='vi', backend='espeak', strip=True, preserve_punctuation=True,with_stress=True, language_switch='remove-flags',njobs=4)
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def espeak_th_cleaners(text): # needs espeak - apt-get install espeak
    text = convert_to_ascii(text)
    text = expand_abbreviations(text.lower())
    phonemes = phonemize(text, language='th', backend='espeak', strip=True, preserve_punctuation=True,with_stress=True, language_switch='remove-flags',njobs=4)
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def espeak_id_cleaners(text): # needs espeak - apt-get install espeak
    text = convert_to_ascii(text)
    text = expand_abbreviations(text.lower())
    phonemes = phonemize(text, language='id', backend='espeak', strip=True, preserve_punctuation=True,with_stress=True, language_switch='remove-flags',njobs=4)
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def espeak_ja_cleaners(text): # needs espeak - apt-get install espeak
    text = convert_to_ascii(text)
    text = expand_abbreviations(text.lower())
    phonemes = phonemize(text, language='ja', backend='espeak', strip=True, preserve_punctuation=True,with_stress=True, language_switch='remove-flags',njobs=4)
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def japanese_cleaners(text):
    text = japanese_to_romaji_with_accent(text)
    text = re.sub(r'([A-Za-z])$', r'\1.', text)
    return text

def japanese_cleaners2(text):
    return japanese_cleaners(text).replace('ts', 'ʦ').replace('...', '…')

def korean_cleaners(text):
    '''Pipeline for Korean text'''
    text = latin_to_hangul(text)
    text = g2p(text)
    text = divide_hangul(text)
    text = fix_g2pk2_error(text)
    text = re.sub(r'([\u3131-\u3163])$', r'\1.', text)
    return text


def korean_cleaners2(text): # KO part from cjke
    '''Pipeline for Korean text'''
    korean_to_ipa(text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def chinese_cleaners(text):
    '''Pipeline for Chinese text'''
    text = number_to_chinese(text)
    text = chinese_to_bopomofo(text)
    text = latin_to_bopomofo(text)
    text = re.sub(r'([ˉˊˇˋ˙])$', r'\1。', text)
    return text


def sanskrit_cleaners(text):
    text = text.replace('॥', '।').replace('ॐ', 'ओम्')
    text = re.sub(r'([^।])$', r'\1।', text)
    return text



# ------------------------------
''' cjke type cleaners below '''
#- text for these cleaners must be labeled first
# ex1 (single) : some.wav|[EN]put some text here[EN]
# ex2 (multi) : some.wav|0|[EN]put some text here[EN]
# ------------------------------

def zh_ja_mixture_cleaners(text):
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_romaji(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]', lambda x: japanese_to_romaji_with_accent(
        x.group(1)).replace('ts', 'ʦ').replace('u', 'ɯ').replace('...', '…')+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def kej_cleaners(text):
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_ipa2(x.group(1)) + ' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa2(x.group(1)) + ' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def cjks_cleaners(text):
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_lazy_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_lazy_ipa(x.group(1))+' ', text)
    #text = re.sub(r'\[SA\](.*?)\[SA\]',
    #              lambda x: devanagari_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_lazy_ipa(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def cjke_cleaners(text):
    text = re.sub(r'\[ZH\](.*?)\[ZH\]', lambda x: chinese_to_lazy_ipa(x.group(1)).replace(
        'ʧ', 'tʃ').replace('ʦ', 'ts').replace('ɥan', 'ɥæn')+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]', lambda x: japanese_to_ipa(x.group(1)).replace('ʧ', 'tʃ').replace(
        'ʦ', 'ts').replace('ɥan', 'ɥæn').replace('ʥ', 'dz')+' ', text)
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]', lambda x: english_to_ipa2(x.group(1)).replace('ɑ', 'a').replace(
        'ɔ', 'o').replace('ɛ', 'e').replace('ɪ', 'i').replace('ʊ', 'u')+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def cjke_cleaners2(text):
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[KO\](.*?)\[KO\]',
                  lambda x: korean_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text

def thai_cleaners(text):
    text = num_to_thai(text)
    text = latin_to_thai(text)
    return text

"""
def vietnamese_cleaners(text):
    text = vi2IPA(text)
    return text
"""




'''
#- reserves

def thai_cleaners(text):
    text = num_to_thai(text)
    text = latin_to_thai(text)
    return text


def shanghainese_cleaners(text):
    text = shanghainese_to_ipa(text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text


def chinese_dialect_cleaners(text):
    text = re.sub(r'\[ZH\](.*?)\[ZH\]',
                  lambda x: chinese_to_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[JA\](.*?)\[JA\]',
                  lambda x: japanese_to_ipa3(x.group(1)).replace('Q', 'ʔ')+' ', text)
    text = re.sub(r'\[SH\](.*?)\[SH\]', lambda x: shanghainese_to_ipa(x.group(1)).replace('1', '˥˧').replace('5',
                  '˧˧˦').replace('6', '˩˩˧').replace('7', '˥').replace('8', '˩˨').replace('ᴀ', 'ɐ').replace('ᴇ', 'e')+' ', text)
    text = re.sub(r'\[GD\](.*?)\[GD\]',
                  lambda x: cantonese_to_ipa(x.group(1))+' ', text)
    text = re.sub(r'\[EN\](.*?)\[EN\]',
                  lambda x: english_to_lazy_ipa2(x.group(1))+' ', text)
    text = re.sub(r'\[([A-Z]{2})\](.*?)\[\1\]', lambda x: ngu_dialect_to_ipa(x.group(2), x.group(
        1)).replace('ʣ', 'dz').replace('ʥ', 'dʑ').replace('ʦ', 'ts').replace('ʨ', 'tɕ')+' ', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text
'''

"""
ipa_ar = epitran.Epitran('ara-Arab')
ipa_fa = epitran.Epitran('fas-Arab')
ipa_tr = epitran.Epitran('tur-Latn')
ipa_ml = epitran.Epitran('mal-Mlym')

ipa_fr = epitran.Epitran('fra-Latn')
ipa_it = epitran.Epitran('ita-Latn')
ipa_de = epitran.Epitran('deu-Latn')
ipa_es = epitran.Epitran('spa-Latn')

ipa_pt = epitran.Epitran('por-Latn')
ipa_pl = epitran.Epitran('pol-Latn')
ipa_sw = epitran.Epitran('swe-Latn')


ipa_mn = epitran.Epitran('mon-Cyrl-bab')
"""

# Function to extract all the numbers from the given string
def numCleaner(str, lang):
	nums = re.findall(r'[-+]?[0-9]+[.]?[0-9]*', str)
	for num in nums:
		if "." in num:
			val = float(num)
		else:
			val = int(num)
		if lang != 'cn':
			str = str.replace(num, num2words(val, lang=lang))
		else:
			str = str.replace(num, cn2an.an2cn(num))
	return str

def canvers_en_cleaners(text):
    text = numCleaner(text,'en')
    return ipa_en.transliterate(text)

def canvers_ja_cleaners(text):
    result = kks.convert(numCleaner(text,'ja'))
    text = ""
    for item in result:
        text = text + item['hira']
    return ipa_ja.transliterate(text)
 
def canvers_cn_cleaners(text):
    text = numCleaner(text,'cn')
    return ipa_cn.transliterate(text)

def canvers_ko_cleaners(text):
    text = numCleaner(text,'ko')
    return ipa_ko.transliterate(text)
  
def canvers_vi_cleaners(text):
    text = numCleaner(text,'vi')
    return ipa_vi.transliterate(text)

def canvers_id_cleaners(text):
    text = numCleaner(text,'id')
    return ipa_id.transliterate(text)

def canvers_th_cleaners(text):
    text = numCleaner(text,'th')
    return ipa_th.transliterate(text)
 
def canvers_ru_cleaners(text):
    text = numCleaner(text,'ru')
    return ipa_ru.transliterate(text)
