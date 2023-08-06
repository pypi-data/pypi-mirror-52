from enum import Enum
import requests
from .model import *

API_VERSION = "0.2"
TIMEOUT = 30000
SUCCESS_CODE = 200


class Language(Enum):
    EN = "en"
    ZH = "zh"


class AtmanParser(object):
    def __init__(self, endpoint, language, is_constituency_parsing):
        self.endpoint = endpoint
        self.language = language
        self.is_constituency_parsing = is_constituency_parsing

    def parse(self, text):
        """Post text to the Preprocess Server

        :param (str|OrderedDict) text : raw text for the server to parse
        :return: tokenization and constituency parsing
        """
        content = {
            "apiVersion": API_VERSION,
            "data": {
                "text": str(text),
                "language": self.language.value,
                "isConstituencyParsing": self.is_constituency_parsing
            }
        }

        r = requests.post(url=self.endpoint, json=content, timeout=TIMEOUT)
        if r.status_code == SUCCESS_CODE:
            r = json.loads(r.text)
            result = Document(jstr=r['data']['constituencyText'])
            return result

        return r.text
