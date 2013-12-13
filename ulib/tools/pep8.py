import inspect
import re


##### Public methods #####
def setupAliases(obj = None) :
    if obj is None :
        frame = inspect.stack()[1]
        obj = inspect.getmodule(frame[0])

    rename_regexp = re.compile(r"([a-z0-9])([A-Z])")

    for name in dir(obj) :
        if name.startswith("_") :
            continue
        attr = getattr(obj, name)

        if inspect.isclass(attr) :
            setupAliases(attr)

        elif inspect.isfunction(attr) :
            pep8_name = re.sub(rename_regexp, r"\1_\2", name).lower()
            if name != pep8_name :
                if not getattr(obj, pep8_name, None) is None :
                    raise RuntimeError("Cannot create PEP8 alias: %s.%s -> %s.%s (destination is already exists)" % (
                        obj.__name__, name, obj.__name__, pep8_name ))
                setattr(obj, pep8_name, attr)

