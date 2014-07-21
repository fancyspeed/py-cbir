#encoding: utf-8
import copy

def blending(result_lists, max_len=5, max_weight=-1):
    '''
    result_lists: [(list<path, weight>, list_weight)]
    '''
    mixed_dict = {} 
    for result_list, list_weight in result_lists:
        for path, weight in result_list:
            if path not in mixed_dict:
                mixed_dict[path] = weight * list_weight
            else:
                mixed_dict[path] = min(weight * list_weight, mixed_dict[path])
    sort_list = sorted(mixed_dict.items(), key=lambda d:d[1])
    result_list = []
    for k, v in sort_list[:max_len]:
        if max_weight < 0 or v <= max_weight:
            result_list.append((k, v))
    return result_list


def ensembling(result_lists, max_len=5, max_weight=-1):
    '''
    result_lists: [(list<path, weight>, list_weight)]
    '''
    default_list = []
    for result_list, list_weight in result_lists:
        default_weight = -1
        for path, weight in result_list:
            if weight * list_weight > default_weight:
                default_weight = weight * list_weight * 1.5
        default_list.append(default_weight)
    mixed_dict = {}
    for i, list_pair in enumerate(result_lists):
        result_list, list_weight = list_pair
        for path, weight in result_list:
            if path not in mixed_dict:
                mixed_dict[path] = copy.deepcopy(default_list)
            mixed_dict[path][i] = weight * list_weight
    for path in mixed_dict:
        mixed_dict[path] = sum(mixed_dict[path])
    sort_list = sorted(mixed_dict.items(), key=lambda d:d[1])
    result_list = []
    for k, v in sort_list[:max_len]:
        if max_weight < 0 or v <= max_weight:
            result_list.append((k, v))
    return result_list
