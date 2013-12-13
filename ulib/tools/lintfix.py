import re

import astroid
import astroid.nodes

from . import pep8


##### Public methods #####
def register(linter):
    astroid.MANAGER.register_transform(astroid.nodes.Module, __transformPep8)
    astroid.MANAGER.register_transform(astroid.nodes.Class, __transformPep8)


##### Private methods #####
def __transformPep8(obj) :
    rename_regexp = re.compile(pep8.RENAME_REGEXP)
    if isinstance(obj, astroid.nodes.Module) :
        module_name = obj.name
    elif isinstance(obj, astroid.nodes.Class) :
        if not isinstance(obj.parent, astroid.nodes.Module) :
            return
        module_name = obj.parent.name
    else :
        raise RuntimeError("Invalid input object: %s" % (obj))

    if module_name == "ulib" or module_name.startswith("ulib.") :
        for name in tuple(obj.locals) :
            method = obj.locals[name][0]
            if not isinstance(method, astroid.nodes.Function) or name.startswith("_") :
                continue
            pep8_name = re.sub(rename_regexp, pep8.RENAME_PLACEHOLDERS, name).lower()
            if name != pep8_name :
                if pep8_name in obj.locals :
                    raise RuntimeError("Cannot create PEP8 alias: %s.%s -> %s.%s (destination is already exists)" % (
                        obj.name, name, obj.name, pep8.name ))
                obj.locals[pep8_name] = obj.locals[name]

