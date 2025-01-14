import json
import time
from hashlib import md5

import execjs
import requests


class Translate:
    def __init__(self, show_print=False):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Origin": "https://fanyi.youdao.com",
            "Referer": "https://fanyi.youdao.com/",
        }
        self.show_print = show_print
        self.iv = None
        self.key = None
        self.session = requests.session()
        self.session.cookies.update({"DICT_DOCTRANS_SESSION_ID": "ODM3NDE4MWItNzNmNi00N2I5LWEzODQtMmRmNjMwOGFlOGRm"})
        self.session.headers = headers
        self.session.get('https://fanyi.youdao.com')
        self.start_url = 'https://dict.youdao.com/webtranslate/key'
        self.translate_url = 'https://dict.youdao.com/webtranslate'

    def get_sign(self, timeStr, key):
        sign_str = f"client=fanyideskweb&mysticTime={timeStr}&product=webfanyi&key={key}"
        return md5(sign_str.encode()).hexdigest()

    def run(self, i=None):
        """
        :param i: 需要翻译的内容
        :return:
        """
        t = str(int(time.time() * 1000))
        params = {
            "keyid": "webfanyi-key-getter",
            "sign": self.get_sign(t, "asdjnjfenknafdfsdfsd"),
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": t,
            "keyfrom": "fanyi.web",
            "mid": "1",
            "screen": "1",
            "model": "1",
            "network": "wifi",
            "abtest": "0",
            "yduuid": "abcdefg"
        }
        response = self.session.get(self.start_url, params=params)
        try:
            jsonData = response.json()
            if not jsonData or 'code' not in jsonData or 0 != jsonData['code']:
                if self.show_print:
                    print(f'获取 aes 密钥失败：{jsonData}')
                return ''
        except Exception as e:
            if self.show_print:
                print(f'获取 aes 密钥错误：{e}')
            return ''

        self.key = jsonData['data']['aesKey']
        self.iv = jsonData['data']['aesIv']

        aesStr = self.parse_translate_data(jsonData['data']['secretKey'], i)
        if not aesStr:
            if self.show_print:
                print('翻译失败：获取 aes 加密数据为空！')
            return ''

        return self.parse_aes_data(aesStr)

    def parse_translate_data(self, secretKey, i):
        """
        请求翻译接口
        :param secretKey:
        :param i:
        :return:
        """
        t = int(time.time() * 1000)
        data = {
            "i": i,
            "from": "auto",
            "to": "",
            "useTerm": "false",
            "domain": "0",
            "dictResult": "true",
            "keyid": "webfanyi",
            "sign": self.get_sign(t, secretKey),
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": t,
            "keyfrom": "fanyi.web",
            "mid": "1",
            "screen": "1",
            "model": "1",
            "network": "wifi",
            "abtest": "0",
            "yduuid": "abcdefg"
        }
        return self.session.post(self.translate_url, data=data).text

    def parse_aes_data(self, aesStr):
        """
        解析 aes 加密数据
        :param aesStr:
        :return:
        """
        try:
            jsonData = execjs.compile(open('aes.js', 'r', encoding='utf-8').read()).call('dec', aesStr, self.key,
                                                                                         self.iv)
            jsonData = json.loads(jsonData)
            if not jsonData or 'code' not in jsonData or 0 != jsonData['code']:
                if self.show_print:
                    print(f'aes 解密失败：{jsonData}')
                return ''

            return jsonData['translateResult'][0][0]['tgt']
        except Exception as e:
            if self.show_print:
                print(f'aes 解密失败xx：{e}')
            return ''
