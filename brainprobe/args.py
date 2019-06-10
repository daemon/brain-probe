from argparse import ArgumentParser, Namespace
from typing import Dict, Iterable, Union, Tuple, Any
import enum


RawDictOption = Tuple[Union[Iterable[str], str], Dict[str, Any]]


class DictOption(object):

    def __init__(self, 
                 arg_names: Union[Iterable[str], str],
                 data: Dict[str, Any]) -> None:
        self.arg_names = arg_names
        self.data = data

    def default(self, default: Any):
        self.data['default'] = default
        return self

    def help(self, help_str: str):
        self.data['help'] = help_str
        return self

    def required(self, is_required: bool):
        self.data['required'] = is_required
        return self

    def __getitem__(self, idx):
        if idx == 0:
            return self.arg_names
        if idx == 1:
            return self.data
        raise IndexError


ArgDict = Iterable[Union[RawDictOption, DictOption]]


def add_dict_options(parser: ArgumentParser,
                     dict_options: ArgDict) -> None:
    for arg_names, dict_ in dict_options:
        if isinstance(arg_names, str):
            arg_names = (arg_names,)
        parser.add_argument(*arg_names, **dict_)


def opt(*args, **kwargs):
    return DictOption(args, kwargs)


def args_to_dict(args: Namespace, filter_: Iterable[str] = []):
    arg_dict = vars(args).copy()
    if filter_:
        keep_args = set(filter_)
        for k in list(arg_dict.keys()):
            if k not in keep_args:
                del arg_dict[k]
    return arg_dict


class OptionEnum(enum.Enum):
    SEED = opt('--seed', type=int, default=0)