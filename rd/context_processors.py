
from django.conf import settings

import requests
import json
import transliterate
from transliterate_pack import RussianLanguagePack2

from transliterate.base import TranslitLanguagePack, registry
registry.register(RussianLanguagePack2)
import rd.models
def debug(context):
  ip = context.META.get("REMOTE_ADDR")
  data = requests.get('http://ipinfo.io/%s/' % ip)
  c = {}
  if data:
    try:
      if data.content:
        geo_info = json.loads(data.content)
        en_name_city = geo_info.get('city')
        city_instance = rd.models.City.objects.filter(en_name=en_name_city).first()
        if city_instance:
          ru_name_city = city_instance.ru_name
        else:
          ru_name_city = transliterate.translit(geo_info.get('city'), 'ru2')
        c['CITY'] = ru_name_city
    except:
      pass
  c['DEBUG'] = settings.DEBUG
  c['ip'] = ip
  return c