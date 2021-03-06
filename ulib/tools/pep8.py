import inspect
import re


##### Public constants #####
RENAME_REGEXP       = r"([a-z0-9])([A-Z])"
RENAME_PLACEHOLDERS = r"\1_\2"


##### Public methods #####
def setupAliases(obj = None) :
    if obj is None :
        frame = inspect.stack()[1]
        obj = inspect.getmodule(frame[0])

    rename_regexp = re.compile(RENAME_REGEXP)

    for name in dir(obj) :
        if name.startswith("_") :
            continue
        attr = getattr(obj, name)

        if inspect.isclass(attr) :
            setupAliases(attr)

        elif inspect.isfunction(attr) :
            pep8_name = re.sub(rename_regexp, RENAME_PLACEHOLDERS, name).lower()
            if name != pep8_name and not hasattr(obj, pep8_name) :
                setattr(obj, pep8_name, attr)

