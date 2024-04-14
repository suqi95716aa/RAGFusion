

"""

是按标题？还是按父子关系？
所以它们两个应该是不一样的，但是可以互相增强。

parent-child document splitter

1. 父节点有parent_id，子节点同时有parent_id、child_id
2. 可以选择切分模式
2.1 重组后切分（默认），条件：传入parentSplitter、childSplitter、原始文档（接受文本/Document对象）
2.2 不重组切分 条件：传入childSplitter、Document对象

做法：
1. 先寻找它们的header关系，成数组然后去重；
2. 开始找，然后切片
3.

"""

import re

# 定义正则表达式
pattern = r"^(\d+(\.\d+)*)[^,.。|;:'\"?!]*$"

# 示例字符串
test_string = "1.2.3 表达式?"

# 检查字符串是否符合正则表达式的条件
if re.match(pattern, test_string):
    print("匹配成功")
else:
    print("匹配失败")