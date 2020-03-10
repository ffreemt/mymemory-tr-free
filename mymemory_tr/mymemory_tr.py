#!/usr/bin/env python
'''
based on mypython mymemory.py

mymemory MAX ALLOWED QUERY : 500 CHARS
'''
import json
from textwrap import wrap

from urllib.parse import quote

from random import choice, randint, seed
from string import ascii_lowercase
import httpx

import logzero
from logzero import logger

# pip install freemt-utils
from freemt_utils import make_url

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
    (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'
}


class QuotaError(Exception):
    '''QuotaError'''


class MymemoryTr:  # pylint: disable=too-few-public-methods
    '''
    to='zh', from_lang='en'
    >>> mymemory = MymemoryTr()
    >>> mymemory.translate('you.')
    '您。 '
    >>> translate = mymemory.translate
    >>> translate('you and me.')
    '你和我。 '
    >>> translate('you and me. China.')
    '你和我。中国。 '
    >>> translate('China')
    '中国'
    '''
    # pylint: disable=too-many-arguments
    def __init__(self, to_lang='zh', from_lang='en', debug=False, proxy=None, testurl=''):
        '''
        testurl: if not empty, is used as dest url (substitute api_url)
        '''
        self.from_lang = from_lang
        self.to_lang = to_lang
        # self.source_list = ['']
        self.proxy = proxy
        self.testurl = testurl

        _ = make_url(proxy)
        proxies = {
            'http': _,
            'https': _,
        }
        self.client = httpx.Client(proxies=proxies)

        if debug:
            logzero.loglevel(10)
        else:
            logzero.loglevel(20)

    # def mymemory(self, source):
    def translate(self, source, from_lang=None, to_lang=None, proxy=None):
        '''
        if from_lang to_lang: None, use instance's

        if proxy != self.proxy: use new client
        '''

        if from_lang is None:
            from_lang = self.from_lang
        if to_lang is None:
            to_lang = self.to_lang

        if from_lang == to_lang:
            return source

        # self.source_list = wrap(source, 1000, replace_whitespace=False)

        # last "." not converted to "。" in dest chinese, attache ' _xx', remove 'XXX' [:-4]
        if to_lang == 'zh':
            # source_list = wrap(source + ' . _xx', 500, replace_whitespace=False)
            # a chinese char about 3 bytes
            source_list = wrap(source + ' . _xx', 160, replace_whitespace=False)
        else:
            source_list = wrap(source, 500, replace_whitespace=False)
        # self.source_list = wrap(source, 1695, replace_whitespace=False)
        #  MAX ALLOWED QUERY : 500 bytes/CHARS

        try:
            _ = (self._get_translation(elm, proxy=proxy) for elm in source_list)
            seq = ' '.join(_)
        except Exception as exc:
            logger.warning(" seq = ' '.join, exc %s ", exc)
            # return None
            raise

        # if seq[:17] == 'MYMEMORY WARNING:':
        if seq.startswith(('MYMEMORY WARNING:',)):
            logger.critical("MYMEMORY WARNING: %s", seq)
            raise QuotaError(seq)

        # last "." not converted to "。" in dest chinese, attache ' _xx', remove 'XXX' [:-4]
        if self.to_lang == 'zh':
            return seq[:-5]

        return seq

    def _get_translation(self, source, proxy=None):
        json5 = self._get_json5(source, proxy=proxy)
        try:
            # data = res.json()  # httpx.get(url)
            data = json.loads(json5)
        except Exception as exc:
            logger.warning(" Probably not connected to mymemory.transalted.net,  data = json.loads(json5), exc: %s ", exc)

            # data = {'error': str(json5)}
            logger.error('returned: %s', json5)
            raise
            # return None

        translation = data['responseData']['translatedText']
        if not isinstance(translation, bool):
            return translation

        matches = data['matches']
        for match in matches:
            if not isinstance(match['translation'], bool):
                next_best_match = match['translation']
                break
        else:
            logger.warning('for ... else...raise')
            raise Exception('Unable to find a match')

        return next_best_match

    def _get_json5(self, source, proxy=None):
        escaped_source = quote(source, '')

        # http://api.mymemory.translated.net/get?q=Hello%20World!&langpair=en|zh

        # api_url = "http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s"
        # req = request.Request(url=api_url % (escaped_source, self.from_lang, self.to_lang),

        # api_url = "http://api.mymemory.translated.net/get?q={0}&langpair={1}|{2}"
        api_url = "http://api.mymemory.translated.net/get?q={0}&langpair={1}|{2}&de={3}"
        #
        # generates key (for using private TMX: http://api.mymemory.translated.net/keygen?user=username&pass=password

        # ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(7,10)))+random.choice(['@gmail.com', '@yahoo.com', '@outlook.com', '@126.com', '@qq.com', '@hotmail.com', '@yahoo.com.hk'])
        #

        # fixed email address for fixed machine name (os.name)
        # random.seed(sum(list(map(ord, os.name)))+1)  # 'nt' => vlcohxnnby@gmail.com

        # random.seed(1 + sum(list(map(ord, ''.join(platform.uname())))))
        # 'kseeiajxtt@hotmail.com'

        seed(-11)
        random_domain = choice([
            '@gmail.com',
            '@yahoo.com',
            '@outlook.com',
            '@126.com',
            '@qq.com',
            '@hotmail.com',
            '@yahoo.com.hk'
        ])  # de=emailaddy how to know it has any effect???
        emailaddy = ''.join(choice(ascii_lowercase) for i in range(randint(7, 10))) + random_domain

        # url="http://translate.google.com/translate_a/t?clien#t=p&ie=UTF-8&oe=UTF-8"
        # +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
        # , headers = headers)

        url = api_url.format(escaped_source, self.from_lang, self.to_lang, emailaddy)

        if self.testurl:
            url = self.testurl
            logger.debug('url: %s', url)

        # req = request.Request(url=url, headers=headers)
        # r = request.urlopen(req)
        # return r.read().decode('utf-8')

        proxy = make_url(proxy)

        # create a new client if proxy not equalt to self.proxy
        if proxy == self.proxy:
            client = self.client
            use_local = False
        else:
            proxies = {
                'http': proxy,
                'https': proxy,
            }
            client = httpx.Client(proxies=proxies)
            use_local = True

            logger.debug('proxies: %s', proxies)

        try:
            # with httpx.Client(proxies=proxies, trust_env=False) as client:
            # res = httpx.get(url)
            res = client.get(url)
            out = res.text

            logger.debug('out: %s', out)
            logger.debug('headers: %s', res.headers)

        except Exception as exc:
            logger.error('%s', exc)
            out = str(exc)
        finally:
            # close the local client if created
            if use_local:
                client.close()

        return out


def main(defvals=None):
    ''' main '''
    import argparse
    import sys
    import locale

    if defvals is None:
        defvals = {'f': 'en', 't': 'zh', 'd': False, 'p': None, 'u': ''}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('texts', metavar='text', nargs='+', help='a string to translate(use "" when it\'s a sentence)')
    parser.add_argument('-t', '--to', dest='to_lang', type=str, default=defvals['t'], help='To language (e.g. zh, zh-TW, en, ja, ko). Default is ' + defvals['t'] + '.')
    parser.add_argument(
        '-f', '--from',
        dest='from_lang', type=str,
        default=defvals['f'],
        help='From language (e.g. zh, zh-TW, en, ja, ko). Default is ' + defvals['f'] + '.'
    )
    parser.add_argument(
        '-d', '--debug',
        dest='debug', type=bool,
        default=defvals['d'],
        help=f'Debug: boolean. Default is {defvals["d"]}.'
    )
    parser.add_argument(
        '-p', '--proxy',
        dest='proxy', type=str,
        default=defvals['p'],
        help=f'Proxy (http://....:8888). Default is {defvals["p"]}.'
    )
    parser.add_argument(
        '-u', '--testurl',
        dest='testurl', type=str,
        default=defvals['u'],
        help=f' testurl used to test proxy. Default is "".'
    )

    args = parser.parse_args()

    # translator = Translator(from_lang=args.from_lang, to_lang=args.to_lang)

    if args.debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    logger.debug('args: %s', args)
    logger.debug('args.texts: %s', args.texts)

    _ = MymemoryTr(
        from_lang=args.from_lang,
        to_lang=args.to_lang,
        debug=args.debug,
        testurl=args.testurl,
    )
    translate = _.translate

    try:
        translation = translate(' '.join(args.texts), proxy=args.proxy)
    except Exception as exc:
        logger.exception(exc)
        # logger.error(exc)
        raise SystemExit(1)

    # sys.stdout.write(translation)
    logger.info('%s', translation)

    for text in args.texts:
        translation = translate(text, args.proxy)
        if sys.version_info.major == 2:
            translation = translation.encode(locale.getpreferredencoding())
        sys.stdout.write(str(translation))
        sys.stdout.write("\n")


# get_ipython is defined in ipython session
# cut and paste wont run main()
if __name__ == "__main__" and not globals().get('get_ipython'):
    # python mymemory.py 生成最新的神经机器翻译（NMT）系统。 -f zh -t en -d 1

    # python mymemory.py abc -u http://173.82.240.230:5000 -d=1 -p http://127.0.0.1:8889

    main()
