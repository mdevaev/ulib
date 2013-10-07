# -*- coding: utf-8 -*-


import hashlib
import multiprocessing
import cjson


##### Public methods #####
def riter(data_dict, level, keys_hook = None, keys_list = ()) :
    for key in ( data_dict if keys_hook == None else keys_hook(data_dict.keys()) ) :
        if level > 0 :
            for result in riter(data_dict[key], level - 1, keys_hook, keys_list+(key,)) :
                yield result
        else :
            yield (keys_list+(key,), data_dict[key])

def hasKeysChain(data_dict, keys_list) :
    for key in keys_list :
        if not data_dict.has_key(key) :
            return False
        data_dict = data_dict[key]
    return True

def dictToList(data_dict) :
    data_list = []
    for key in sorted(data_dict.keys()) :
        value = data_dict[key]
        if isinstance(value, dict) :
            value = dictToList(value)
        data_list.append((key, value))
    return data_list

def dictHash(data_dict, function=hashlib.md5) :
    return function(cjson.encode(dictToList(data_dict))).hexdigest()


###
def extendReplace(source_list, item, replace_list) :
    index = source_list.index(item)
    return source_list[:index] + replace_list + source_list[index + 1:]

def chunks(items_list, chunk_size) :
    return [
        items_list[offset:offset+chunk_size]
        for offset in xrange(0, len(items_list), chunk_size)
    ]


###
def pmap(method, items_list, processes = 0) :
    if processes == 0 or processes == 1 :
        return map(method, items_list)
    else :
        if len(items_list) == 0 :
            return []
        pool = multiprocessing.Pool(processes=processes)
        try :
            results_list = pool.map(method, items_list)
            return results_list
        finally :
            pool.close()
            pool.join()

