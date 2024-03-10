import asyncio
import re
import asyncio
# 引入metagpt库的模块
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from metagpt.actions import Action


# 定义一个SimpleWriteCode的类，它继承了Action类
class SimpleWriteCode(Action):
    # 定义一个类属性PROMPT_TEMPLATE，它是一个字符串模板
    PROMPT_TEMPLATE: str = """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """

    # 定义一个类属性name，其值为'SimpleWriteCode'
    name: str = "SimpleWriteCode"
    # 重新run方法，接受一个参数instruction
    async def run(self, instruction: str):
        # 使用传入的instruction参数进行字符串格式化
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        # 使用_aask方法执行并得到结果，我们假设这个方法会基于prompt生成代码并返回
        rsp = await self._aask(prompt)
        # 使用静态方法parse_code解析出代码部分
        code_text = SimpleWriteCode.parse_code(rsp)
        # 返回解析出的代码文本
        return code_text

    # 定义一个静态方法parse_code，它接受一个参数rsp
    @staticmethod
    def parse_code(rsp):
        # 定义一个正则表达式，用于查找python代码部分
        pattern = r"```python(.*)```"
        # 使用正则表达式模块re，按照上面定义的pattern在rsp中进行搜索
        match = re.search(pattern, rsp, re.DOTALL)
        # 如果找到了匹配项，则返回匹配项中的第一个组，也就是python代码部分；如果没有找到则返回整个rsp
        code_text = match.group(1) if match else rsp
        return code_text
    

# 定义一个SimpleCoder的类，继承了Role类
class SimpleCoder(Role):
    # 定义一个类属性
    name: str = "dev-itdabai"
    # 定义一个类属性profile，描述该角色的信息
    profile: str = "code developer,write perfect code without debug"
    # 定义构造函数，接受任意数量的关键字参数
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 执行父类Role的构造函数
        self.set_actions([SimpleWriteCode])  # 为该角色配置拥有的动作/技能

    # 定义一个异步方法_act，它返回一个Message对象
    async def _act(self) -> Message:
        # 使用logger.info记录当前要执行的行为
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        # 获取当前要执行的行为
        todo = self.rc.todo  # todo将是一个SimpleWriteCode的实例对象
        # 获取最近的一条消息
        msg = self.get_memories(k=1)[0]
        # 运行todo实例的run方法，传入最近的一条消息的内容，并获取代码文本
        code_text = await todo.run(msg.content)
        # 创建并返回一个新的Message对象，内容为代码文本，角色为自身的profile，由todo类型引发
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        return msg

async def main():
    msg = "write a python function that read and return excel content with a testcase"
    role = SimpleCoder()
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)

asyncio.run(main())