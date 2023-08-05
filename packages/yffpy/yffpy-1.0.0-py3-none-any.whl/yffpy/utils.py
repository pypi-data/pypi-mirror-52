import logging
from collections import ChainMap

import stringcase

logger = logging.getLogger(__name__)


# noinspection PyTypeChecker
def unpack_data(json_obj, parent_class=None):
    subclasses = {}
    if parent_class:
        subclasses = {stringcase.snakecase(cls.__name__): cls for cls in parent_class.__subclasses__()}

    if json_obj:
        if isinstance(json_obj, list):
            json_obj = [obj for obj in json_obj if obj]

            if len(json_obj) == 1:
                return unpack_data(json_obj[0], parent_class)
            else:
                if any(isinstance(obj, dict) for obj in json_obj):
                    return flatten_dict_list(json_obj, parent_class)

                return [unpack_data(obj, parent_class) for obj in json_obj if obj]

        elif isinstance(json_obj, dict):

            if "0" in json_obj.keys() and "1" not in json_obj.keys():
                if len(json_obj.keys()) == 1:
                    return unpack_data(json_obj.get("0"), parent_class)
                else:
                    if isinstance(json_obj.get("0"), dict):
                        json_obj.update(json_obj.get("0"))

            if "count" in json_obj.keys() and "position" in json_obj.keys():
                return get_type({k: unpack_data(v, parent_class) for k, v in json_obj.items()}, parent_class,
                                subclasses)
            else:
                return get_type(dict({k: unpack_data(v, parent_class) for k, v in json_obj.items() if k != "count"}),
                                parent_class, subclasses)
        else:
            return json_obj


def flatten_dict_list(json_obj_dict_list, parent_class):
    json_obj_dict_list = [obj for obj in json_obj_dict_list if obj]
    item_keys = []
    ndx = 0
    for item in json_obj_dict_list:
        if isinstance(item, list):
            flattened_item = flatten_dict_list(item, parent_class)
            json_obj_dict_list[ndx] = flattened_item
            item_keys.extend(list(flattened_item.keys()))
        else:
            item_keys.extend(list(item.keys()))
        ndx += 1

    if len(item_keys) == len(set(item_keys)):
        agg_dict = {}
        for dict_item in json_obj_dict_list:
            agg_dict.update(dict_item)

        return unpack_data(agg_dict, parent_class)
    else:
        return [unpack_data(obj, parent_class) for obj in json_obj_dict_list if obj]


def get_type(json_obj_dict, parent_class, subclasses):
    for k, v in json_obj_dict.items():
        if k in subclasses.keys() and isinstance(v, dict) and not isinstance(v, subclasses[k]):
            json_obj_dict[k] = subclasses[k](unpack_data(v, parent_class))
    return json_obj_dict


def complex_json_handler(obj):
    if hasattr(obj, "serialized"):
        return obj.serialized()
    else:
        try:
            return str(obj, "utf-8")
        except TypeError:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


def reformat_json_list(json_obj):
    if isinstance(json_obj[0], list):
        if len(json_obj) > 1:
            return reformat_json_list(
                [reformat_json_list(item) if isinstance(item, list) else item for item in json_obj])
        else:
            return reformat_json_list(json_obj[0])
    else:
        return ChainMap(*[value for value in json_obj if value])
