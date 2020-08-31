import datetime
import os
from colorama import init, Fore
import json
from config import config
init()


def parse_msg(msg):
    if isinstance(msg, str):
        return msg

    if isinstance(msg, int):
        return str(msg)

    if isinstance(msg, float):
        return str(msg)

    if isinstance(msg, bool):
        if msg:
            return 'True'
        else:
            return 'False'

    elif isinstance(msg, (list, dict)):
        return json.dumps(msg, indent=4, default=lambda x: str(x))

    else:
        return str(msg)


class Logger:
    def __init__(self, path, error_path, name, level, max_size):
        self.colors = {
            'verde': Fore.GREEN,
            'azul': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'blanco': Fore.WHITE,
            'amarillo': Fore.YELLOW,
            'rojo': Fore.RED,
            'reset': Fore.RESET
        }
        if not os.path.isdir(path):
            os.mkdir(path)
        self.path = path
        self.error_path = error_path
        self.format = '%Y-%m-%d_%H:%M:%S.%f'
        self.level = level
        self.name = name
        self.logger_name = f'{datetime.datetime.now().strftime(self.format)}_{self.name}.log'
        self.max_size = max_size

    def flush(self):
        self.logger_name = datetime.datetime.now().strftime(self.format) + '_' + self.name + '.log'

    def check_if_flush(self):
        if os.path.getsize(os.path.join(self.path, self.logger_name)) > self.max_size:
            self.flush()

    def debug(self, *msgs, color='blanco'):
        color = self.colors[color]
        msg = ''.join([parse_msg(m) for m in msgs])
        to_write = datetime.datetime.now().strftime(self.format) + '; DEBUG; ' + msg
        if self.level > 3:
            print(color + to_write + Fore.RESET)
        with open(os.path.join(self.path, self.logger_name), 'a', encoding='utf-8') as f:
            f.write(to_write + '\n')
        self.check_if_flush()

    def info(self, *msgs, color='blanco'):
        color = self.colors[color]
        msg = ''.join([parse_msg(m) for m in msgs])
        to_write = datetime.datetime.now().strftime(self.format) + '; INFO; ' + msg
        if self.level > 2:
            print(color + to_write + Fore.RESET)
        with open(os.path.join(self.path, self.logger_name), 'a', encoding='utf-8') as f:
            f.write(to_write + '\n')
        self.check_if_flush()

    def warning(self, *msgs, color='amarillo'):
        color = self.colors[color]
        msg = ''.join([parse_msg(m) for m in msgs])
        to_write = datetime.datetime.now().strftime(self.format) + '; WARNING; ' + msg
        if self.level > 1:
            print(color + to_write + Fore.RESET)
        with open(os.path.join(self.path, self.logger_name), 'a', encoding='utf-8') as f:
            f.write(to_write + '\n')
        self.check_if_flush()

    def error(self, *msgs):
        msg = ''.join([parse_msg(m) for m in msgs])
        to_write = datetime.datetime.now().strftime(self.format) + '; ERROR; ' + msg
        if self.level > 0:
            print(Fore.RED + to_write + Fore.RESET)
        with open(os.path.join(self.path, self.logger_name), 'a', encoding='utf-8') as f:
            f.write(to_write + '\n')
        self.check_if_flush()
        with open(os.path.join(self.error_path, 'error_' + self.logger_name), 'a', encoding='utf-8') as f:
            f.write(to_write + '\n')


logger = Logger(
    config['logger']['path'],
    config['logger']['error_path'],
    'server',
    5,
    10000000
)
