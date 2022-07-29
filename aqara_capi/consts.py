
from enum import Enum


class Locality(Enum):
    CN = 'CN'
    USA = 'USA'
    KR = 'KR'
    RU = 'RU'
    GER = 'GER'


API_DOMAIN = {
    Locality.CN: 'open-cn.aqara.com',
    Locality.USA: 'open-usa.aqara.com',
    Locality.KR: 'open-kr.aqara.com',
    Locality.RU: 'open-ru.aqara.com',
    Locality.GER: 'open-ger.aqara.com',
}  # type: dict[Locality, str]
