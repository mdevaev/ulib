import hashlib
import multiprocessing
import json


##### Public methods #####
def riter(data_dict, level, keys_hook = None, keys_list = ()) :
    for key in ( data_dict if keys_hook == None else keys_hook(list(data_dict.keys())) ) :
        if level > 0 :
            for result in riter(data_dict[key], level - 1, keys_hook, keys_list+(key,)) :
                yield result
        else :
            yield (keys_list+(key,), data_dict[key])

def hasKeysChain(data_dict, keys_list) :
    for key in keys_list :
        if not key in data_dict :
            return False
        data_dict = data_dict[key]
    return True

def setKeysChain(data_dict, value, keys_list, selector = None) :
    for key in keys_list[:-1] :
        data_dict.setdefault(key, {})
        data_dict = data_dict[key]
    key = keys_list[-1]
    if callable(selector) and key in data_dict :
        value = selector(data_dict[key], value)
    data_dict[key] = value


###
def dictToList(data_dict) :
    data_list = []
    for key in sorted(data_dict.keys()) :
        value = data_dict[key]
        if isinstance(value, dict) :
            value = dictToList(value)
        data_list.append((key, value))
    return data_list

def utf8Hasher(text) :
    return hashlib.sha1(text.encode("utf-8")).hexdigest()

def objectHash(value, hasher=utf8Hasher, encoder=json.dumps) :
    # FIXME (minor): {"foo":"bar"} == hash(("foo", "bar"))
    # FIXME (major): hash([{3: 4, 1: 2}]) != hash([{1: 2, 3: 4}])
    if isinstance(value, dict) :
        value = dictToList(value)
    return hasher(encoder(value))


###
def extendReplace(source_list, item, replace_list) :
    index = source_list.index(item)
    return source_list[:index] + replace_list + source_list[index + 1:]

def chunks(items_list, chunk_size) :
    return [
        items_list[offset:offset+chunk_size]
        for offset in range(0, len(items_list), chunk_size)
    ]


###
def pmap(method, items_list, processes = 0) :
    if processes == 0 or processes == 1 :
        return list(map(method, items_list))
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


###
def average(n_list) :
    return sum(n_list) / len(n_list)

def median(n_list) :
    n_list = sorted(n_list)
    mid = len(n_list) // 2
    if len(n_list) % 2 == 0 :
        return (n_list[mid-1] + n_list[mid]) / 2
    else :
        return n_list[mid]

