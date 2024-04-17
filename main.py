import tenacity

max_reties = 0


class MyRetryableClass:
    def __init__(self, max_retries):
        self.max_retries = max_retries
        global max_reties
        max_reties = self.max_retries

    def my_method(self):
        # 这里是可能会失败的方法
        # 如果失败，将根据配置重试
        print("尝试执行方法...")
        # 模拟失败
        raise Exception("出了一些问题")

# 使用示例
my_instance = MyRetryableClass(max_retries=3)
print(max_reties)

# try:
#     my_instance.my_method()
# except Exception as e:
#     print(f"方法执行失败，最后的异常信息是: {e}")


# # 假设这些全局变量已经在类定义之前定义
# GLOBAL_VARIABLE = 6
# BGE_URL = "http://example.com"
#
# def test():
#     print(GLOBAL_VARIABLE)
#
# class MyClass:
#     def __init__(self, max_retries):
#         global GLOBAL_VARIABLE  # 声明 GLOBAL_VARIABLE 为全局变量
#         GLOBAL_VARIABLE += max_retries  # 修改全局变量的值
#         print(GLOBAL_VARIABLE)
#
# # 创建类的实例并修改全局变量
# my_instance = MyClass(5)
# print(GLOBAL_VARIABLE)
#
# test()