import argparse
import configparser
import copy

from . import tools
import ulib.tools.pep8 # pylint: disable=W0611

from .validatorlib import ValidatorError


##### Private constants #####
_OPT_VALIDATOR = "validator"
_OPT_OPTION    = "option"
_OPT_DEST      = "dest"
_OPT_DEFAULT   = "default"


##### Public methods #####
class Namespace(argparse.Namespace) : # pylint: disable=R0924,R0903
    def __getitem__(self, option) :
        return getattr(self, option[1])

    def __contains__(self, key) :
        raise RuntimeError("Use hasattr() for this")


class OptionsConfig :
    def __init__(self, options_list, config_file_path, argv_list = None, **kwargs_dict) :
        self.__all_options_dict = {}
        self.__all_dests_dict = {}
        for option_tuple in options_list :
            (option, dest, default, validator) = option_tuple
            option_dict = {
                _OPT_OPTION    : option_tuple,
                _OPT_DEST      : dest,
                _OPT_DEFAULT   : default,
                _OPT_VALIDATOR : validator,
            }
            self.__all_options_dict[option] = option_dict
            if not dest is None :
                self.__all_dests_dict[dest] = option_dict

        parser = argparse.ArgumentParser(add_help=False)
        version = kwargs_dict.pop("version", None)
        if not version is None :
            parser.add_argument("-v", "--version", action="version", version=version)
        parser.add_argument("-c", "--config", dest="config_file_path", default=config_file_path, metavar="<file>")
        (options, self.__remaining_list) = parser.parse_known_args(argv_list)

        self.__config_dict = ( {} if options.config_file_path is None else self.__readConfig(options.config_file_path) )
        kwargs_dict.update({
                "formatter_class" : argparse.RawDescriptionHelpFormatter,
                "parents"         : [parser],
            })
        self.__parser = argparse.ArgumentParser(**kwargs_dict)


    ### Public ###

    def addArgument(self, arg_tuple) :
        options_list = [
            ( option if option.startswith("-") else "--"+option )
            for option in arg_tuple[0]
        ]
        kwargs_dict = arg_tuple[2]
        kwargs_dict.update({ _OPT_DEST : arg_tuple[1][1], _OPT_DEFAULT : None })
        self.__parser.add_argument(*options_list, **kwargs_dict)

    def addArguments(self, *args_tuple) :
        for arg_tuple in args_tuple :
            self.addArgument(arg_tuple)

    def parser(self) :
        return self.__parser

    def sync(self, sections_list, ignore_list = ()) :
        raw_options = self.__parser.parse_args(self.__remaining_list, namespace=Namespace())
        options = copy.copy(raw_options)
        for (dest, option_dict) in self.__all_dests_dict.items() :
            option_tuple = option_dict[_OPT_OPTION]
            if option_tuple in ignore_list or not hasattr(options, dest) :
                continue
            value = self.getCommonOption(sections_list, option_tuple, getattr(options, dest))
            setattr(options, dest, value)
        return (options, raw_options)

    def getOption(self, section, option_tuple) :
        (option, _, default, validator) = option_tuple
        return self.__raiseIncorrectValue(option, validator, self.__config_dict[section].get(option, default))

    def getCommonOption(self, sections_list, option_tuple, cli_value = None) :
        (option, _, default, validator) = option_tuple
        if cli_value is None :
            requests_list = [ (section, option) for section in sections_list ]
            value = self.__lastValue(default, requests_list)
        else :
            value = cli_value
        return self.__raiseIncorrectValue(option, validator, value)


    ### Private ###

    def __readConfig(self, file_path) :
        parser = configparser.ConfigParser()
        parser.read(file_path)
        config_dict = {}
        for section in parser.sections() :
            config_dict.setdefault(section, {})
            for option in parser.options(section) :
                validator = self.__all_options_dict.get(option, {}).get(_OPT_VALIDATOR)
                if validator is None :
                    raise ValidatorError("Unknown option: %s::%s" % (section, option))
                else :
                    value = parser.get(section, option)
                    value = self.__raiseIncorrectValue("%s::%s" % (section, option), validator, value)
                    config_dict[section][option] = value
        return config_dict

    def __lastValue(self, first, requests_list) :
        assert len(requests_list) > 0
        last_value = first
        for (section, option) in requests_list :
            if option in self.__config_dict.get(section, {}) :
                last_value = self.__config_dict[section][option]
        return last_value

    def __raiseIncorrectValue(self, option, validator, value) :
        try :
            return validator(value)
        except ValidatorError as err :
            raise ValidatorError("Incorrect value for option \"%s\": %s" % (option, err))


##### PEP8 #####
tools.pep8.setupAliases()

