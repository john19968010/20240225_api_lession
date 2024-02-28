# Introduction
from dotenv import load_dotenv
import os

# """
# @print_func_name
# def execute():
#     print("nice")

# execute()
# >>> The function name is execute
# >>> nice
# """


# ## function的加工
# """

# def print_func_name(func):
#     print(f"The function name is {func.__name__}")
#     func()


# def execute():
#     print("nice")


# def execute2():
#     print("nice2")


# if __name__ == "__main__":

#     execute()
#     print_func_name(execute2)

# """

# ########################################################


# ## function的加工2


# # def print_func_name(func):
# #     def warp():
# #         print(f"The function name is {func.__name__}")
# #         func()

# #     return warp

# """
# def print_func_name(func):
#     def warp(*args, **kwargs):
#         print(f"The function name is {func.__name__}")
#         func()

#     return warp


# def execute():
#     print("nice")


# def execute2():
#     print("nice2")


# if __name__ == "__main__":
#     # print_func_name(execute)
#     a = print_func_name(execute)
#     b = print_func_name(execute2)
#     a()
#     b()
# """

# ########################################################

# # Basic decorator


# def print_func_name(func):
#     def warp(*args, **kwargs):
#         print("args")
#         print(type(args))
#         print(args)
#         print("=====")
#         print("kwargs")
#         print(type(kwargs))
#         print(kwargs)
#         print(kwargs)
#         print(f"The function name is {func.__name__}")
#         """
#         func()

#     return warp


# @print_func_name
# def execute():
#     print("nice")


# if __name__ == "__main__":
#     # print_func_name(execute)()

#     execute()


# # ########################################################
# # # Multi decorator

# # """
# # def print_func_hash_code(func):
# #     def warp():
# #         print(f"The function hash code is {func.__hash__()}")
# #         func()

# #     return warp


# # def print_func_name(func):
# #     def warp():
# #         print(f"The function name is {func.__name__}")
# #         func()

# #     return warp


# # @print_func_hash_code
# # @print_func_name
# # def execute():
# #     print("nice")


# # if __name__ == "__main__":
# #     execute()
# # """


# # ########################################################
# # # Decorator with parameter

# # """
# # def print_func_with_param(param):
# #     def decorator(func):
# #         def wrap():
# #             print(f"The function name is {func.__name__}, parameter is {param}")
# #             func()

# #         return wrap

# #     return decorator


# # @print_func_with_param("nice")
# # def execute():
# #     print("Main execute")


# # if __name__ == "__main__":
# #     execute()
# # """

####
"""
練習題:
在yahoo_finance的func中加入驗證的裝飾器, 驗證內容為輸入正確的帳號密碼(input)
帳號密碼自行定義, 要驗證通過才能取response值
# """


def login(func):
    def warp(*args, **kwargs):
        print(f"args: {args}, type: {type(args)}")
        print(args[0], args[1])
        print("---------")
        print(f"kwargs: {kwargs}, type: {type(kwargs)}")
        print(kwargs["fir_with_default"], kwargs["sec_with_default"])
        """
        args: (1, 2), type: <class 'tuple'>
        1 2
        ---------
        kwargs: {'fir_with_default': 'nice3', 'sec_with_default': 'nice4'}, type: <class 'dict'>
        nice3 nice4
        """
        username, password = input("您的帳號為："), input("您的密碼為：")
        if username == os.getenv("AM_ACCOUNT") and password == os.getenv("AM_PASSWORD"):
            return func(*args, **kwargs)
        else:
            print("帳號密碼登入失敗")

    return warp


@login
def execute(fir, sec, fir_with_default="nice", sec_with_default="nice2"):
    print("nice")


if __name__ == "__main__":
    load_dotenv()
    execute(1, 2, fir_with_default="nice3", sec_with_default="nice4")
