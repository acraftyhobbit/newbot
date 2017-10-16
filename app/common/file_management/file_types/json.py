def open_json_file(key):
    from common.file_management.manager import read_file
    text = read_file(key=key, open_type='rb')
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    js = dict()
    if text:
        js = clean_json(text)
    return js


def store_json_file(obj, key, large=False, overwrite=True):
    from common.file_management.manager import store_file
    import json
    store_file(obj=json.dumps(obj), key=key, large=large, overwrite=overwrite)
    return key


def clean_json(json_string):
    import json
    import re
    from json.decoder import JSONDecodeError
    result = dict()
    try:
        result = json.loads(json_string)  # try to parse...
    except JSONDecodeError as e:
        # "Expecting , delimiter: line 34 column 54 (char 1158)"
        # position of unexpected character after '"'
        unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
        # position of unescaped '"' before that
        unesc = json_string.rfind(r'"', 0, unexp)
        json_string = json_string[:unesc] + r'\"' + json_string[unesc + 1:]
        # position of corresponding closing '"' (+2 for inserted '\')
        closg = json_string.find(r'"', unesc + 2)
        json_string = json_string[:closg] + r'\"' + json_string[closg + 1:]
        try:
            result = clean_json(json_string=json_string)
        except RuntimeError:
            pass
    return result
