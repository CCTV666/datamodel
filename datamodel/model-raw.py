import json
from dataclasses import dataclass, field, fields, is_dataclass, asdict
from typing import List, Dict

__all__ = ['Datamodel', 'dataclass', 'field', 'List', 'Dict']


class Datamodel:
    @classmethod
    def decoder(cls, data: object):
        """ 解码，JSON 转对象
        data:       要解码的 JSON 对象 (str, dict, list, tuple, set)
        return:     经过解码后的 cls 实例对象
        """
        def parse(T, data) -> object:
            if T.__module__ == 'typing' and not T._special and (args := T.__args__):
                if T._name == 'List':
                    if args[0].__module__ == 'typing':
                        return parse(args[0].__args__[0], data)
                    else:
                        return parse(args[0], data)
                if T._name == 'Dict':
                    return dict((x[0], parse(T.__args__[1], x[1])) for x in data.items())
            if is_dataclass(T):
                if isinstance(data, list):
                    return [T.decoder(x) for x in data]
                else:
                    return T.decoder(data)
            return data

        if (obj := cls()) and isinstance(data, dict):
            for name, T in [(f.name, f.type) for f in fields(cls) if f.name in data]:
                if T.__module__ == 'typing':
                    setattr(obj, name, parse(T, data[name]))
                    continue
                if is_dataclass(T):  # dataclass 类
                    setattr(obj, name, T.decoder(data[name]))
                    continue
                try:  # 基本类型
                    setattr(obj, name, T(data[name]))
                except (TypeError, ValueError, AttributeError) as err:
                    if not (T in [int, float] and data[name] == ''):
                        print(f'{cls.__name__} {name} decoder error: {err}')
            return obj
        if isinstance(data, str):
            try:
                return cls.decoder(json.loads(data))
            except json.decoder.JSONDecodeError as err:
                print(err)
        if isinstance(data, (list, tuple, set)):
            return [cls.decoder(x) for x in data if isinstance(x, dict)]  # 过滤掉非字典元素

    def asdict(self) -> dict:
        return asdict(self)