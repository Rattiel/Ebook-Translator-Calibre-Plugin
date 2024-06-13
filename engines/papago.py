import json
import re

from .base import Base
from .languages import papago

load_translations()

zero_space = ''
white_space = ' '
japanese_mark = {
    '。': '.',
    '（': "(",
    '）': ")",
    '！': '!',
    '？': '?',
    '～': '~'
}

divide_patterns = ['"', "'", '「', '」', '『', '』', '\[', '\]', '\{', '\}', '(', '（', ')', '）']
divide_marks = ['"', "'", '「', '」', '『', '』', '[', ']', '{', '}', '(', '（', ')', '）']

punctuation_patterns = ['…', '\n', '.', '。', '!', '！', '?', '？', '~', '～', '\-', '─']
punctuation_marks = ['…', '\n', '.', '。', '!', '！', '?', '？', '~', '～', '-', '─']

punctuation_pattern = r'([' + "".join(divide_patterns + punctuation_patterns) + r'])\s*'
translate_ignore_mark = divide_marks + punctuation_marks + [white_space, zero_space]


class PapagoTranslate(Base):
    name = 'papago'
    alias = 'Papago'
    lang_codes = Base.load_lang_codes(papago)
    endpoint = {
        'translate': 'https://naveropenapi.apigw.ntruss.com/nmt/v1/translation',
    }
    need_api_key = False

    client_id = ''
    client_secret = ''
    glossary_key = ''
    is_novel_translate = False

    def __init__(self):
        Base.__init__(self)

        self.client_id = self.config.get('client_id', self.client_id)
        self.client_secret = self.config.get('client_secret', self.client_secret)
        self.glossary_key = self.config.get('glossary_key', self.glossary_key)
        self.is_novel_translate = self.config.get('is_novel_translate', self.is_novel_translate)

    def translate_request(self, text):
        headers = {
            'Content-Type': 'application/json',
            'X-NCP-APIGW-API-KEY-ID': self.client_id,
            'X-NCP-APIGW-API-KEY': self.client_secret
        }

        data = json.dumps({
            'text': text,
            'source': self._get_source_code(),
            'target': self._get_target_code(),
            'glossaryKey': self.glossary_key
        })

        return self.get_result(
            self.endpoint.get('translate'), data, headers, method='POST',
            callback=lambda r: json.loads(r)['message']['result']['translatedText'])

    def translate(self, text):
        if not self.is_novel_translate:
            return self.translate_request(text)

        split_text = re.split(punctuation_pattern, text)

        result = ""
        split_text_len = len(split_text)
        for index, target_text in enumerate(split_text):
            if target_text not in translate_ignore_mark:
                if index > 1 and split_text[index - 1] in punctuation_marks:
                    result += white_space
                result += self.translate_request(target_text)
            else:
                if target_text in japanese_mark:
                    result += japanese_mark[target_text]
                else:
                    result += target_text

                #if index < split_text_len - 1:
                #    if split_text[index + 1] not in white_space_not_need_marks:
                #        result += white_space

        return result
