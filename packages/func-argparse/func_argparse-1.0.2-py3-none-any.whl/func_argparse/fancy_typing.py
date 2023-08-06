import inspect
import sys
import numpy as np
from typing import Any, Callable, Sequence, TypeVar, Union, overload, List
from mypy_extensions import TypedDict


def test_numpy():
    a: np.ndarray[np.int32] = np.array([1, 2])
    reveal_type(a)
    b: np.ndarray[np.float32] = np.array([1, 2])
    reveal_type(b)
    reveal_type(a + b)
    reveal_type((a + b).item(0))


_L = TypeVar("_L")
_R = TypeVar("_R")


class A:
    ...


class AA(A):
    ...


@overload
def choice(left: _L, right: _R, chose_left: bool) -> Union[_L, _R]:
    return left if chose_left else right


def choice(left, right, chose_left):
    return left if chose_left else right


def test_union(aa: bool):
    reveal_type(choice(AA(), A(), aa))
    reveal_type(choice([AA()], [A()], aa))
    aas: Sequence[A] = [AA()]
    reveal_type(choice([AA()], [A()], aa))
    i: np.ndarray[np.int16] = np.array([0])
    i32: np.ndarray[np.int32] = i

    reveal_type(choice(i, i32, aa))
    reveal_type(i + i32)
    reveal_type(np.array([0]))
    reveal_type(np.array(0, dtype="int32"))


# def _new_FuncArgType(fn: FunctionType) -> type:
#     spec = inspect.getfullargspec(fn)
#     annotations = dict(spec.annotations)
#     for a in spec.args:
#         if a in annotations:
#             continue
#         annotations[a] = Any
#     return _typeddict_new(fn.__name__ + "Args", annotations)

# _TypedDictMeta = type(TypedDict)


def one_arg(x: Any) -> Any:
    pass


def get_annotations(fn: Callable):
    spec = inspect.getfullargspec(fn)
    annotations = dict(spec.annotations)
    for a in spec.args:
        if a in annotations:
            continue
        annotations[a] = Any
    print("Function", fn, "has signature", annotations)
    return annotations


class FuncArgTypeMeta(type):
    def __new__(cls, fn: Callable):
        return TypedDict(fn.__name__ + "Args", get_annotations(fn))


# class FuncArgType(metaclass=FuncArgTypeMeta):
#     pass


# class FuncArgType2(TypedDict):
#     """Args of a function as a typed dict"""

#     def __new__(cls, fn):
#         return super().__init__(get_annotations(fn))


def FuncArgType3(fn: Callable) -> type:
    return TypedDict(fn.__name__ + "Args", get_annotations(fn))


def _meta(fn: Callable) -> type:
    import pdb

    pdb.set_trace()  # breakpoint ed8fdb1b //
    print("_meta", fn, file=sys.stderr)

    class _FuncArgTypeMeta(type):
        _fn = fn
        _annotations = get_annotations(fn)

        def __getitem__(cls, item: str) -> type:
            return cls._annotations[item]

        @classmethod
        def __instancecheck__(cls, inst: dict):
            return isinstance(inst, dict) and all(
                key in cls._annotations for key in inst.keys()
            )

    return _FuncArgTypeMeta


def _dict_new(cls, *args, **kwargs):
    return dict(*args, **kwargs)


class _FuncArgTypeMeta4(type):
    def __new__(cls, name, fn=None):
        # Create new typed dict class object.
        # This method is called directly when TypedDict is subclassed,
        # or via _typeddict_new when TypedDict is instantiated. This way
        # TypedDict supports all three syntaxes described in its docstring.
        # Subclasses and instances of TypedDict return actual dictionaries
        # via _dict_new.
        # ns['__new__'] = _dict_new
        tp_dict = super(_FuncArgTypeMeta4, cls).__new__(cls, name, (dict,), ns)

        fn = getattr(tp_dict, "fn", fn)
        if fn is None:
            tp_dict.__annotations__ = {}
            return tp_dict
        tp_dict.__annotations__ = get_annotations(fn)
        return tp_dict


def f(xx: int, yy: float):
    pass


FuncArgType4 = _FuncArgTypeMeta4("FuncArgType4", f)

# FArgs = TypedDict("FArgs", **get_annotations(f))
FArgs = FuncArgType4("FArgs", f)


def h(xx: VarArg):
    pass


def g(f_args: FuncArgType4):
    reveal_type(FuncArgType4)
    reveal_type(f_args)
    pass


g({"foo": 1})


from nptyping import Array


def index_array(x: Array[int, 10, 1]) -> float:
    return x[0, 0, 0]
