
from django.conf import settings

import requests
import json
import transliterate
from transliterate_pack import RussianLanguagePack2

from transliterate.base import TranslitLanguagePack, registry
registry.register(RussianLanguagePack2)

def debug(context):
  ip = context.META.get("REMOTE_ADDR")
  data = requests.get('http://ipinfo.io/%s/' % ip)
  c = {}
  if data:
    try:
      if data.content:
        geo_info = json.loads(data.content)
        c['CITY'] = transliterate.translit(geo_info.get('city'), 'ru2')
    except:
      pass
  c['DEBUG'] = settings.DEBUG
  c['ip'] = ip
  return c