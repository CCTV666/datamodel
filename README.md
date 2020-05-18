# datamodel

**datamodel** 是专门为 Python 写的一个 JSON to Model 模块。

支持：

- 字典转对象 ( `dict` to `object` )
- 列表转对象数组 ( `list` to `List[object]` )
- 对象转字典 ( `object` to `dict` )

## 使用案例

```python
"""
包含需要继承的 DataModel 类；
dataclasses 模块中的 dataclass 装饰器；
以及 typing 模块中常用的 List 和 Dict 类型。
"""
from datamodel import *

@dataclass
class Phone(DataModel):
    name: str = ''
    number: str = ''

@dataclass
class Dog(DataModel):
    name: str = ''
    color: str = ''
    
@dataclass
class Person(DataModel):
    name: str = 'one'
    age: int = 0
    phone: Phone = None
    dogs: List[Dog] = field(default_factory=list)

if __name__ == "__main__"
    import json

    data = {
        "name": 'HjzCy',
        "age": 19,
        "phone": {
            "name": "iPhone XS",
            "number": "13689772671"
        },
        "dogs": [
            {
                "name": "小黑狗",
                "color": "黑色"
            },
            {
                "name": "妞妞",
                "color": "金色"
            },
            {
                "name": "大黄狗",
                "color": "黄色"
            }
        ]
    }
    
    # decoder 接收一个 dict、list 或 str ( 将解析为 dict 或 list ) 等类型的值作为参数。
    # 如果传递的是 dict，则返回调用它的类实例对象，否则返回该实例对象的数组。
    p = Person.decoder(data)  # 解码字典
    print(p)
    '''\
    Person(name='HjzCy',
           age=19, 
           phone=Phone(name='iPhone XS', number='13689772671'), 
           dogs=[Dog(name='小黑狗', color='黑色'), Dog(name='妞妞', color='金色'), Dog(name='大黄狗', color='黄色')])
    '''
    
    p = Person.decoder(json.dumps(data))  # 解码 JSON 字符串
    print(p)  # 输出同上
    
    dogs = Dog.decoder(data['dogs'])  # 解码列表
    print(dogs)
    # [Dog(name='小黑狗', color='黑色'), Dog(name='妞妞', color='金色'), Dog(name='大黄狗', color='黄色')]
```

## 使用说明

1. **类必须经过 `@dataclass` 修饰**

    python 3.7 的新特性，为简单起见，约束所有类型必须使用。
    如果你还不知道什么是 `@dataclass` ，请参阅 [理解 Python 的 Dataclasses](https://zhuanlan.zhihu.com/p/59657729)。

2. **必须为所有属性提供默认值 ( 可为 `None` )**

    暂时强制遵守。原因我要在 `decoder` 方法中实例化传进来的类，如果该类中包含只是定义而不初始化的字段时，就会报错。例如：
    ```python
    @dataclass
    class Person:
        name: str
        age: int
    ```
    该 `Person` 类传到 `decoder` 方法中会报错！

3. **不会检测 `__init__` 中定义的属性**

    如果你已经使用了 `@dataclass` 修饰类，也许就没必要在定义一个 __init__ 方法了。要在初始化后执行额外的操作，请在 `__post_init__` 方法中完成。

4. **被解析的容器类 ( 例如 `dict` 和 `list` 等 ) 的值不能包含自定义类型**

    例如，某个 `dict` 不能是 `{"p": Person(name="HjzCy", "age": 19)}` 。

    算是一个缺陷？或许以后会处理。

5. **自动类型转换**

    `decoder()` 方法能够将数据转换为符合对象预期的类型。例如：
    
    ```python
    @dataclass
    class Ip(DataModel):
        ip: str = ""
        port: str = 0

    print(Ip.decoder({"ip": "192.136.1.95", "port": 8080}))  # 注意：字典中的 port 键值是 int 类型
    # Ip(ip='192.136.1.95', port='8080')
    ```
    
    如果某些数据不能够自动转换时，则保留在定义该类时设置的初始值。例如：
    
    ```python
    @dataclass
    class Child(DataModel):
        name: str = ''
        age: int = 0
    
    # 在输出之前，如果 decoder 解码出现错误，则将其抛出，以便用于调试：
    # Child DecoderError: invalid literal for int() with base 10: '19.a'
    # Child(name='Hjz', age=0)
    print(Child.decoder({"name": "Hjz", "age": "19.a"}))
    ```
