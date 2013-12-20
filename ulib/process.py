import os
import subprocess
import threading
import signal
import logging

from . import tools
import ulib.tools.pep8 # pylint: disable=W0611


##### Public constants #####
LOGGER_NAME = "process"


##### Private objects #####
_logger = logging.getLogger(LOGGER_NAME)


##### Exceptions #####
class SubprocessError(Exception) :
    pass


##### Public methods #####
def getLogger() :
    return _logger

def setLogger(logger) :
    global _logger
    _logger = logger


###
def execProcess(
        proc_args_list,
        proc_input = None,
        env_dict = None,
        fatal_flag = True,
        shell_flag=False,
        private_input_flag = False,
        show_output_flag = False
    ) :

    _logger.debug("Executing child process: %s", proc_args_list)

    if env_dict is not None :
        assert isinstance(env_dict)
        env_dict = dict(env_dict)
        env_dict.setdefault("LC_ALL", "C")

    proc = subprocess.Popen(
        proc_args_list,
        shell=shell_flag,
        bufsize=1024,
        close_fds=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env_dict,
    )
    (proc_stdout, proc_stderr) = proc.communicate(proc_input)
    proc_retcode = proc.returncode

    if proc_retcode != 0 or show_output_flag :
        if proc_input is None :
            proc_input = ""
        elif private_input_flag and _logger.isEnabledFor(logging.DEBUG) :
            proc_input = "<PRIVATE>"
        message = "Process \"%s\" results:\nStdout: %s\nStderr: %s\nStdin: %s\nReturn code: %d" % (
            proc_args_list,
            proc_stdout.strip(),
            proc_stderr.strip(),
            proc_input,
            proc_retcode,
        )

        if proc_retcode == 0 :
            _logger.debug(message)
        else :
            if fatal_flag :
                raise SubprocessError(message)
            _logger.error(message)

    _logger.debug("Child process \"%s\" is finished; retcode: %d", proc_args_list, proc_retcode)
    return (proc_stdout, proc_stderr, proc_retcode)


##### Public classes #####
class SuicideWatchdog(threading.Thread) :
    def __init__(self, timeout, signum = signal.SIGKILL) :
        self._timeout = timeout
        self._signum = signum
        self._event = threading.Event()
        threading.Thread.__init__(self, name="SuicideWatchdog")

    ### Public ###

    def stop(self) :
        self._event.set()


    ### Private ###

    def run(self) :
        self._event.wait(self._timeout)
        if not self._event.is_set() :
            pid = os.getpid()
            pgid = os.getpgid(pid)
            _logger.warn("Suicide by timeout(%d sec): pid: %d; pgid: %d; signum: %d", self._timeout, pid, pgid, self._signum)
            os.killpg(pgid, self._signum)


##### PEP8 #####
tools.pep8.setupAliases()

