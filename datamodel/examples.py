from enum import Enum
from typing import List, Type

from dataclasses import dataclass

from datamodel import Datamodel


class TypeEnum(Enum):
    ROOT = 1
    CHILDREN = 2


@dataclass
class TypeExample(Datamodel):
    id: str = None
    type: TypeEnum = None


@dataclass
class Node(Datamodel):
    id: str = None
    name: str = None
    # childList是一个List
    # Type['className'] 是自引用 , 3.7及其以后可用 from __future__ import annotations ,直接使用自己类名
    childList: List[Type['Node']] = None


if __name__ == '__main__':
    #
    typeExample = TypeExample.decoder({"id": "2222", "type": 1})

    print(typeExample)

    # 自我嵌套
    dictObj = {"id": "1", "name": "n1", "childList": [
        {"id": "2", "name": "n2",
         "childList": [
             {"id": "2-1", "name": "n2-1",
              "childList": []}
         ]},
        {"id": "3", "name": "n3",
         "childList": []}
    ]}

    root1 = Node.decoder(dictObj)
    print(root1)

    import json

    jsonStr = json.dumps(dictObj)
    root2 = Node.decoder(jsonStr)
    print(root2)
