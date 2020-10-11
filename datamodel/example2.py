from enum import Enum
from typing import List, Type

from dataclasses import dataclass
from datamodel import Datamodel


class UpdateTypeEnum(Enum):
    STYLE = "style"
    B = 2


@dataclass
class ItemStyle(Datamodel):
    # 是否可见
    visible: bool = None
    # 更换文本
    text: str = None
    child: List[Type['ItemStyle']] = None


@dataclass
class GraphicsItemUpdateData(Datamodel):
    # 页面id
    pageId: str = None
    # 图形itemId
    itemId: str = None
    # 类型
    type: UpdateTypeEnum = None
    # 样式
    style: List[ItemStyle] = None


@dataclass
class PageGraphicsData(Datamodel):
    # 是否显示
    visible: bool = None
    # 数据
    data: str = None
    # x 坐标
    x: float = None
    y: float = None
    # 图片/线条类型
    name: str = None
    # 图形的唯一id
    id: str = None
    # 类型0图片,1线条
    type: int = None

    ##########以下为线条属性############
    strokeStyle: str = None
    # 点的坐标数组 [[x,y],[x1,y1]]
    linePointList: list = None
    # 线条粗细
    lineWidth: float = None


if __name__ == '__main__':
    a = GraphicsItemUpdateData.decoder([{"pageId": "ddd", "itemId": 5, "type": "style",
                                         "style": [{"visible": True, "text": "ddd",
                                                    "child": [{
                                                        "visible": True, "text": "ddd",
                                                    }]
                                                    }
                                                   ]}])
    print(a)

    data = """[
	{
		"visible": true,
		"data": "",
		"x": 50,
		"name": "capacitance",
		"y": 37,
		"id": "d855957",
		"type": 0
	},
	{
		"visible": true,
		"data": "",
		"x": 207,
		"name": "circuitBreakerUpRightImg",
		"y": 119,
		"id": "3a36ca",
		"type": 0
	},
	{
		"visible": true,
		"data": "",
		"x": 207,
		"name": "circuitBreakerUpRightGreenImg",
		"y": 119,
		"id": "78b29ff",
		"type": 0
	},
	{
		"strokeStyle": "red",
		"visible": true,
		"data": "",
		"name": "polyline",
		"linePointList": [
			[
				75,
				37
			],
			[
				75,
				-13
			],
			[
				141,
				-13
			],
			[
				141,
				126
			],
			[
				207,
				126
			]
		],
		"id": "ae79f82",
		"type": 1,
		"lineWidth": 1
	},
	{
		"visible": true,
		"data": "",
		"x": 376,
		"name": "fuseUpRightImg",
		"y": 91,
		"id": "e7d048a",
		"type": 0
	},
	{
		"strokeStyle": "#222",
		"visible": true,
		"data": "",
		"name": "polyline",
		"linePointList": [
			[
				257,
				126
			],
			[
				320,
				126
			],
			[
				320,
				41
			],
			[
				384,
				41
			],
			[
				384,
				91
			]
		],
		"id": "2efe0b61",
		"type": 1,
		"lineWidth": 1
	}
]"""

    dataList = PageGraphicsData.decoder(data)
    print(dataList)
