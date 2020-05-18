# datamodel

datamodel 是一个可以从 JSON 映射到 Python 类的模块。

**支持：**

- 字典转对象 ( `dict` → `object` )
- 列表转对象数组 ( `list` → `List[object]` )
- 对象转字典 ( `object` → `dict` )

目前网上并没有一个比较好的 JSON to Model 库，就算有，其写法也大多繁琐。由于做项目需要经常把从服务器上请求到的 JSON  转换到对应类的实例，于是决定自己写一个。

## 使用

**JSON 转类对象**

```python
"""
包括需要继承的 DataModel 类，dataclasses 模块中的 dataclass 装饰器；
以及 typing 模块中常用的 List 和 Dict 类型。
"""
from datamodel import *

@dataclass
class Person(Datamodel):
    name: str = ''
    age: int = 0
    height: int = 0

p = Person.decoder({"name": "HjzCy",
                    "age": 18,
                    "height": 170
                    })

# Person(name='HjzCy', age=18, height=170)
print(p)
```

**类对象转 JSON**

```python
# {'name': 'HjzCy', 'age': 18, 'height': 170}
print(p.asdict())
```

**JSON 转类型实例列表**

```python
data = """[{
    "name": "HjzCy",
    "age": "18",
    "height": "170"
},
{
    "name": "YDMS",
    "age": "15",
    "height": "176"
}]"""
    
p_list = Person.decoder(data)
# [Person(name='HjzCy', age=18, height=170), Person(name='YDMS', age=15, height=176)]
print(p_list)
```

## Api

- **`decoder(cls, data: object)`**

  接收一个 `dict` 、`list` 或 `str` 类型的值作为参数，返回**对应类型的实例**或**对应类型的实例列表**。并且支持自动类型转换。例如：

  ```python
  @dataclass
  class Ip(Datamodel):
      ip: str = ""
      port: int = 0
  
  # 注意: 被解析的 port 字段值是 str 型
  # Ip(ip='192.136.1.95', port=8080)
  print(Ip.decoder({"ip": "192.136.1.95", "port": "8080"}))
  ```

  **注意**：如果某些值不能自动转换到对应的类型，则保留默认值。例如：

  ```python
  # Ip(ip='192.136.1.95', port=0)
  print(Ip.decoder({"ip": "192.136.1.95", "port": "a1234"}))

- **`asdict()`**

  将类实例对象转换为对应字段的字典。

## 使用说明

1. **类必须经过 `@dataclass` 修饰**

    python 3.7 的新特性，为简单起见，约束所有类型必须使用。参阅 [理解 Python 的 Dataclasses](https://zhuanlan.zhihu.com/p/59657729)。
    
2. **必须为所有属性提供默认值 ( 可为 `None` )**

    暂时强制遵守。原因我要在 `decoder` 方法中实例化传进来的类，如果该类中包含只是定义而不初始化的字段时，就会报错。例如：
    ```python
    @dataclass
    class Person:
        name: str
        age: int
    ```
    该 `Person` 传到 `decoder` 方法中会报错！

3. **不会检测 `__init__` 中定义的属性**

    如果你已经使用了 `@dataclass` 修饰类，也许就没必要在定义一个 `__init__` 方法了。如果需要，请在 `__post_init_` 方法中执行初始化后要执行的额外操作。
