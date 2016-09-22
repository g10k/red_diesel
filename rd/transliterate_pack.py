# encoding: utf-8
from transliterate.base import TranslitLanguagePack, registry
from transliterate.contrib.languages.ru import data
import transliterate

# new_data = data.reversed_specific_mapping

correct_pre_processor_mapping = data.pre_processor_mapping
correct_pre_processor_mapping[u'kh'] = u'х'
correct_pre_processor_mapping[u'Kh'] = u'Х'

class RussianLanguagePack2(TranslitLanguagePack):
    """
    Language pack for Russian language. See http://en.wikipedia.org/wiki/Russian_alphabet for details.
    """
    language_code = "ru2"
    language_name = "Russian"
    character_ranges = ((0x0400, 0x04FF), (0x0500, 0x052F))
    mapping = data.mapping
    reversed_specific_mapping = data.reversed_specific_mapping
    pre_processor_mapping = correct_pre_processor_mapping
    detectable = True
registry.register(RussianLanguagePack2)
