from typing import Callable, TypeVar, List, Annotated, Any,Dict
from functools import wraps
 
T = TypeVar('T', bound=Callable[..., Any])


def add_list_decorator(fn: T) -> Callable[..., Annotated[List[Any], 'List of original return type']]:
    """
    装饰器函数，用于将函数的返回类型修改为 List[原始返回类型]。

    :param fn: 原始函数
    :return: 新函数，返回类型被修改为 List[原始返回类型]
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        return [fn(*args, **kwargs)]

    # 更新类型提示
    return_type = List[fn.__annotations__.get('return', Any)]
    wrapper.__annotations__ = {**fn.__annotations__, 'return': Annotated[return_type, 'List of original return type']}

    return wrapper


# 示例原始函数
@add_list_decorator
def example_function(param1: int, param2: str) -> dict:
    return 1.0


# 打印新函数的类型提示
print("New function type hints:")
print(example_function.__annotations__)

# 示例调用
print("\nCalling the new function:")
print(example_function(1, 'test'))
example_function()