# -*- coding: utf-8 -*-
# author: ethosa
from threading import Thread
from .utils import *
requests.packages.urllib3.disable_warnings()
from .vkaudio import *
from .smiles import *
import traceback
import datetime
import random
import time
import sys

class Vk:
    '''
    docstring for Vk

    Get vk access token here:
    https://vkhost.github.io/ (choose the Kate mobile.)

    used:
    vk = Vk(token=Access_Token) # if you want auth to user
    vk = Vk(token=Group_Access_Token) # if you want auth to group

    use param version_api for change verison api. Default value is 5.101
    use param debug=True for debugging!
    use param lang='en' for set debug language! # en, ru, de, fr, ja

    for handling new messages:
    In the official VK API documentation, the event of a new message is called "message_new", so use:

    @on_message_new
    def get_new_message(obj):
        print(obj)
        print('text message:', obj.text) # see https://vk.com/dev/objects/message for more info
        print(obj.obj)
        print(obj.peer_id)

    use any vk api method:
    vk.method(method='messages.send', message='message', peer_id=1234567890, random_id=0)

    use messages methods:
    vk.messages.send(message='message', peer_id=1234567890)

    methods, which working with token Kate Mobile:
    - audio.getUploadServer
    - audio.save
    '''

    def __init__(self, *args, **kwargs):
        self.token_vk = get_val(kwargs, "token") # Must be string
        self.debug = get_val(kwargs, "debug") # Must be boolean
        if self.debug: self.debug = 1.0
        self.version_api = get_val(kwargs, "version_api", "5.101") # Can be float / integer / string
        self.group_id = get_val(kwargs, "group_id") # can be string or integer
        self.lang = get_val(kwargs, "lang", "en") # must be string
        self.verison = "0.1.53"

        # Initialize methods
        self.longpoll = LongPoll(access_token=self.token_vk, group_id=self.group_id, version_api=self.version_api)
        self.method = Method(access_token=self.token_vk, version_api=self.version_api).use
        self.help = Help

        # Other variables:
        self.translate = Translator_debug().translate
        self.vk_api_url = "https://api.vk.com/method/"

        if self.token_vk:
            if self.debug: sys.stdout.write(self.translate('Токен установлен. Проверяем его валидность ...', self.lang))
            test = ''.join(requests.get('%smessages.getLongPollServer?access_token=%s&v=%s%s' % (self.vk_api_url, self.token_vk, self.version_api, "&group_id=%s" % (self.group_id) if self.group_id else "")).json().keys())
            if self.debug: sys.stdout.write(self.translate("Ошибка" if test == "error" else 'Успешно!', self.lang))
        else:
            if self.debug: sys.stdout.write(self.translate("Ошибка", self.lang))

        self.uploader = Uploader(vk=self)


    # Handlers:
    # use handlers:
    # @vk.*name function*
    # def function(obj):
    #     pass
    #
    # Example:
    # @vk.on_wall_post_new
    # def get_message(obj):
    #     print("post text is", obj.text)
    #
    # Hander longpolls errors:
    # return object with variables:
    # object.message, object.line, object.code
    def on_error(self, function):
        def parse_error():
            while True:
                for error in self.longpoll.errors:
                    function(error)
                    self.longpoll.errors.remove(error)
        Thread_VK(parse_error).start()

    def getUserHandlers(self):
        # return ALL user handlers
        return ["on_%s" % i for i in users_event]


    # Handler wrapper
    # Use it:
    # def a(func): vk.listen_wrapper('message_new', Obj, func)
    # @a
    # def get_mess(obj):
    #   print(obj.text)
    def listen_wrapper(self, type_value, class_wrapper, function, user=False, e="type"):
        def listen(e=e):
            if type(type_value) == int:
                e = 0
            for event in self.longpoll.listen():
                if event.update[e] == type_value:
                    try: function(class_wrapper(event.update))
                    except Exception as error_msg:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        line = traceback.extract_tb(exc_tb)[-1][1]
                        self.longpoll.errors.append(Error(line=line, message=str(error_msg), code=type(error_msg).__name__), file=__file__)
        Thread_VK(listen).start()

    def get_random_id(self):
        return random.randint(-2**37-1, 2**37-1) # random.randint(-2**10, 2**10)

    def __getattr__(self, method):
        if method.startswith("on_"):
            if method[3:] not in users_event.keys():
                return lambda function: self.listen_wrapper(method[3:], Obj, function)
            else:
                return lambda function: self.listen_wrapper(users_event[method[3:]], Obj, function)
        else: return Method(access_token=self.token_vk, version_api=self.version_api, method=method)

    def __str__(self):
        return '''**********
The Vk object with params:
token = %s
debug = %s
version_api = %s
group_id = %s
**********''' % ("%s**********%s" % (self.token_vk[:5], self.token_vk[-5:]), self.debug, self.version_api, self.group_id)


class LongPoll:
    '''
    docstring for LongPoll

    use it for longpolling

    example use:
    longpoll = LongPoll(access_token='your_access_token123')
    for event in longpoll.listen():
        print(event)
    '''
    def __init__(self, *args, **kwargs):
        self.group_id = get_val(kwargs, "group_id")
        self.access_token = kwargs["access_token"]
        self.vk_api_url = 'https://api.vk.com/method/'
        self.version_api = get_val(kwargs, "version_api", "5.101")
        self.ts = "0"
        self.errors = []

    def listen(self):
        if self.group_id:
            response = requests.get("%sgroups.getLongPollServer?access_token=%s&v=%s&group_id=%s" %
                                    (self.vk_api_url, self.access_token, self.version_api, self.group_id)).json()['response']
            self.ts = response['ts']
            self.key = response['key']
            self.server = response['server']

            while 1.0:
                response = requests.get('%s?act=a_check&key=%s&ts=%s&wait=25' % (self.server, self.key, self.ts)).json()
                self.ts = get_val(response, 'ts', self.ts)
                updates = get_val(response, 'updates')

                if updates:
                    for update in updates: yield Event(update)
        else:
            response = requests.get("%smessages.getLongPollServer?access_token=%s&v=%s" %
                                    (self.vk_api_url, self.access_token, self.version_api)).json()['response']
            self.ts = response["ts"]
            self.key = response["key"]
            self.server = response["server"]

            while 1.0:
                response = requests.get('https://%s?act=a_check&key=%s&ts=%s&wait=25&mode=202&version=3' % (self.server, self.key, self.ts)).json()
                self.ts = get_val(response, 'ts', self.ts)
                updates = get_val(response, 'updates')

                if updates:
                    for update in updates: yield Event(update)


# Class for use anything vk api method
# You can use it:
# response = vk.method(method='wall.post', message='Hello, world!')
class Method:
    def __init__(self, *args, **kwargs):
        self.access_token = kwargs['access_token']
        self.vk_api_url = 'https://api.vk.com/method/'
        self.version_api = get_val(kwargs, 'version_api', '5.101')
        self.method = get_val(kwargs, 'method', '')

    def use(self, method, *args, **kwargs):
        url = '%s%s' % (self.vk_api_url, method)
        kwargs['access_token'] = self.access_token
        kwargs['v'] = self.version_api
        response = requests.post(url, data=kwargs).json()
        return response

    def __getattr__(self, method):
        return lambda **kwargs: self.use(method="%s.%s" % (self.method, method), **kwargs)

from .uploader import *

class Keyboard:

    """
    docstring for Keyboard

    use it for add keyboard in message

    keyboard = Keyboard()
    keyboard.add_button(Button(type='text', label='lol'))
    keyboard.add_line()
    keyboard.add_button(Button(type='text', label='hello', color=ButtonColor.POSITIVE))
    keyboard.add_button(Button(type='text', label='world', color=ButtonColor.NEGATIVE))
    # types "location", "vkpay", "vkapps" can't got colors. also this types places on all width line.
    keyboard.add_button(Button(type='location''))
    keyboard.add_button(Button(type='vkapps'', label='hello, world!'))
    keyboard.add_button(Button(type='vkpay''))
    """

    def __init__(self, *args, **kwargs):
        self.keyboard = {
            "one_time" : get_val(kwargs, "one_time", 1.0),
            "buttons" : get_val(kwargs, "buttons", [[]])
        }

    def add_line(self):
        if len(self.keyboard['buttons']) < 10:
            self.keyboard['buttons'].append([])

    def add_button(self, button):
        if len(self.keyboard['buttons'][::-1][0]) <= 4:
            if button['action']['type'] != 'text' and len(self.keyboard['buttons'][-1]) >= 1:
                self.add_line()
            if len(self.keyboard['buttons']) < 10:
                self.keyboard['buttons'][::-1][0].append(button)
        else:
            self.add_line()
            if len(self.keyboard['buttons']) < 10:
                self.add_button(button)

    def compile(self):
        return json.dumps(self.keyboard)


class Button:

    """
    docstring for Button

    Button use for Keyboard.
    Usage:
    red_button = Button(label='hello!', color=ButtonColor.NEGATIVE)

    and use red button:
    keyboard.add_button(red_button) # easy and helpfull!
    """

    def __init__(self, *args, **kwargs):
        self.type = get_val(kwargs, "type", "text")

        actions = {
            "text" : {
                "type" : "text",
                "label" :get_val(kwargs, "label","бан"),
                "payload" : get_val(kwargs, "payload", '')
            },
            "location" : {
                "type" : "location",
                "payload" : get_val(kwargs, "payload", '')
            },
            "vkpay" : {
                "type" : "vkpay",
                "payload" : get_val(kwargs, "payload", ''),
                "hash" : get_val(kwargs, "hash", 'action=transfer-to-group&group_id=1&aid=10')
            },
            "vkapps" : {
                "type" : "open_app",
                "payload" : get_val(kwargs, "payload", ''),
                "hash" : get_val(kwargs, "hash", "ethosa_lib"),
                "label" : get_val(kwargs, "label", ''),
                "owner_id" : get_val(kwargs, "owner_id", "-181108510"),
                "app_id" : get_val(kwargs, "app_id", "6979558")
            }
        }

        self.action = get_val(actions, kwargs['type'], actions['text'])
        self.color = get_val(kwargs, 'color', ButtonColor.PRIMARY)

    def __new__(self, *args, **kwargs):
        self.__init__(self, *args, **kwargs)
        kb = { 'action' : self.action, 'color' : self.color }
        if kb['action']['type'] != 'text':
            del kb['color']
        return kb


# Enums start here:
class Event:
    '''docstring for Event'''
    def __init__(self, update, *args, **kwargs):
        self.update = update
    def __str__(self):
        return "%s" % self.update


class Thread_VK(Thread):
    def __init__(self, function):
        Thread.__init__(self)
        self.function = function
    def run(self):
        self.function()


class ButtonColor:
    PRIMARY = "primary"
    SECONDARY = "secondary"
    NEGATIVE = "negative"
    POSITIVE = "positive"


class Error:
    def __init__(self, *args, **kwargs):
        self.code = kwargs["code"]
        self.message = kwargs["message"]
        self.line = kwargs["line"]
        self.file = kwargs['file']
    def __str__(self):
        return "%s, Line %s:\n%s\nFile: %s" % (self.code, self.message, self.line, self.file)


class Obj:
    def __init__(self, obj):
        self.obj = obj
        if type(self.obj) == dict:
            self.strdate = datetime.datetime.utcfromtimestamp(self.obj['date']).strftime('%d.%m.%Y %H:%M:%S') if 'date' in self.obj else None
    def has(self, key):
        return key in self.obj
    def __getattr__(self, attribute):
        val = get_val(self.obj, attribute)
        return val if val else get_val(self.obj['object'] if type(self.obj) == dict else self.obj[6] if attribute in self.obj[6] else self.obj[7], attribute)

class Help:

    """
    docstring for Help

    usage:
    vk.help() - return list of all methods

    vk.help('messages') - return list of all messages methods

    vk.help('messages.send') - return list of all params method
    """

    def __new__(self, *args, **kwargs):
        if not args:
            resp = requests.get('https://vk.com/dev/methods').text
            response = resp.split('<div id="dev_mlist_submenu_methods" style="">')[1].split('</div>')[0].split('<a')
            return [i.split('>')[1].split('</a')[0].lower() for i in response if len(i.split('>')) > 1 and i.split('>')[1].split('</a')[0] != '']
        else:
            return self.__getattr__(self, args[0])
    def __getattr__(self, method):
        if '.' not in method:
            resp = requests.get(f'https://vk.com/dev/{method}').text
            response = resp.split('<span class="dev_methods_list_span">')
            response = [i.split('</span>', 1)[0] for i in response if len(i.split('</span>', 1)[0]) <= 35]
            return response
        else:
            response = requests.get(f'https://vk.com/dev/{method}').text.split('<table class="dev_params_table">')[1].split('</table>')[0]

            params = { i.split('<td')[1].split('>')[1].split('</td')[0] : i.split('<td')[2].split('>', 1)[1].split('</td')[0] for i in response.split('<tr') if len(i) > 2 }

            for i in params.keys():
                params[i] = params[i].replace('\n', ' ').replace('&lt;', '{').replace('&gt;', '}')
                while '<' in params[i]:
                    pos = [params[i].find('<'), params[i].find('>')]
                    params[i] = f'{params[i][:pos[0]]}{params[i][pos[1]+1:]}'
            return params