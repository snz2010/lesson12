from os.path import isfile
import json

SETTINGS_FILE_PATH = 'settings.json'
ANC_FILE = "candidates.json"  # словарь


# Установили значение по умолчанию, если файла не оказалось.
CONFIG = {
    'DEBUG': True,
    'SOME_VARIABLE': 'Значение по умолчанию',
}

ANC_LIST = []


# Если файл есть - перезаписали настройки.
if isfile(SETTINGS_FILE_PATH):
    with open(SETTINGS_FILE_PATH) as f:
        CONFIG = json.load(f)

if isfile(ANC_FILE):
    with open(ANC_FILE, encoding='utf-8') as f:
        ANC_LIST = json.load(f)

