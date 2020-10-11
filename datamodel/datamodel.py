import json
from dataclasses import dataclass, field, fields, is_dataclass, asdict, _MISSING_TYPE
from typing import List, Dict, _ForwardRef

__all__ = ['Datamodel', 'dataclass', 'field', 'List', 'Dict']


@dataclass
class Datamodel:
    @classmethod
    def decoder(cls, data: object):
        """
        方法接收一个 dict 、list、tuple、set 或 str 类型的值作为参数，
        返回 **对应类型的实例** 或 **对应类型的实例列表**。并且支持自动类型转换。
        """

        def parse(T, data) -> object:
            # if T.__module__ == 'typing' and not T._special and (args := T.__args__):
            # 使用hasattr判断类型
            if T.__module__ == 'typing' and not hasattr(T, "_special"):
                # args = T.__args__
                args = T.__args__ if hasattr(T, "__args__") else None
                if args:
                    # if T._name == 'List':
                    # 用内置方法判断T的类型
                    if issubclass(T, List):
                        if args[0].__module__ == 'typing':
                            if isinstance(T, _ForwardRef):
                                return parse(args[0], data)
                            return parse(args[0].__args__[0], data)
                        return parse(args[0], data)
                    elif issubclass(T, Dict):
                        return {x: parse(T.__args__[1], y) for x, y in data.items()}

            if is_dataclass(T):
                if isinstance(data, list):
                    return [T.decoder(x) for x in data]
                return T.decoder(data)
            return data

        obj = cls()
        if isinstance(data, dict):
            for f in fields(cls):
                if f.name not in data:  # 该字段不在数据键中
                    setattr(obj, f.name, cls.__dict__[f.name])
                elif f.type.__module__ == 'typing':  # 处理来自 typing 模块的类型
                    setattr(obj, f.name, parse(f.type, data[f.name]))
                elif is_dataclass(f.type):  # dataclass 类
                    setattr(obj, f.name, f.type.decoder(data[f.name]))
                else:
                    try:  # 数据和实例中的基本数据类型转换
                        if data[f.name] is None:  # 若为None，则等于该字段类型的初始默认值。
                            setattr(obj, f.name,
                                    f.default_factory if isinstance(f.default, _MISSING_TYPE) else f.default)
                        else:
                            setattr(obj, f.name, f.type(data[f.name]))
                    except Exception as err:
                        # 如果碰到实例类型为 int 或 float，数据值为 空串('') 时，则不打印异常信息。
                        # 换句话说：碰到 obj.int/float('') 时不提示异常。
                        if not (f.type in [int, float] and data[f.name] == ''):
                            print(f'{cls.__name__} {f.name} decoder error: {err}')
            return obj
        elif isinstance(data, str):
            try:
                return cls.decoder(json.loads(data))
            except json.decoder.JSONDecodeError:
                raise
        elif isinstance(data, (list, tuple, set)):  # 过滤掉非字典元素
            return [cls.decoder(x) for x in data if isinstance(x, dict)]
        else:
            raise ValueError("不支持的类型！")

    def asdict(self) -> dict:
        return asdict(self)

