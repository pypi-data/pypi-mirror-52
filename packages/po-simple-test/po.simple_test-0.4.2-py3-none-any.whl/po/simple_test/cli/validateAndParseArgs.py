# ------- #
# Imports #
# ------- #

from .._vendor.po.case_conversion import camelcase
from copy import deepcopy
from .._vendor.simple_test_process.parseArgs import _grepArgs, _grepArgsKeys
from types import SimpleNamespace as o
from ..fns import isLaden
from .usage import usage
import os


# ---- #
# Init #
# ---- #

arguments = set(["--project-dir", "--reporter", "--silent", *_grepArgsKeys])
helpOrVersion = set(["--help", "--version"])


# ---- #
# Main #
# ---- #


def validateAndParseArgs(args, cliResult):
    argsObj = o(
        reporter=None, projectDir=None, silent=False, grepArgs=deepcopy(_grepArgs)
    )
    validationResult = o(
        argsObj=argsObj, cliResult=cliResult, hasError=False, positionalArgs=[]
    )

    i = 0

    while i < len(args):
        if not args[i].startswith("--"):
            break

        arg = args[i]
        if arg not in arguments:
            if not argsObj.silent:
                if arg in helpOrVersion:
                    cliResult.stderr = f"'{arg}' must be the only argument when passed"
                else:
                    cliResult.stderr = f"invalid option '{arg}'"
                    cliResult.stderr += os.linesep + usage

            cliResult.code = 2
            validationResult.hasError = True

            return validationResult

        if arg == "--silent":
            argsObj.silent = True

        elif arg == "--reporter":
            if i == len(args) - 1:
                if not argsObj.silent:
                    cliResult.stderr = "'--reporter' must be given a value"
                    cliResult.stderr += os.linesep + usage

                cliResult.code = 2
                validationResult.hasError = True
                return validationResult

            i += 1
            arg = args[i]
            argsObj.reporter = arg

        elif arg == "--project-dir":
            i += 1
            if i == len(args):
                if not argsObj.silent:
                    cliResult.stderr = "'--project-dir' must be given a value"
                    cliResult.stderr += os.linesep + usage

                cliResult.code = 2
                validationResult.hasError = True
                return validationResult

            arg = args[i]
            argsObj.projectDir = arg

        else:  # arg in _grepArgsKeys
            i += 1
            if i == len(args):
                if not argsObj.silent:
                    cliResult.stderr = f"{arg} must be given a value"
                    cliResult.stderr += os.linesep + usage

                cliResult.code = 2
                validationResult.hasError = True
                return validationResult

            grepVals = getattr(argsObj.grepArgs, camelcase(arg))
            grepVals.append(args[i])

        i += 1

    positionalArgs = args[i:]
    if isLaden(positionalArgs):
        if not argsObj.silent:
            cliResult.stderr = "this command doesn't take positional arguments"
            cliResult.stderr += os.linesep + usage

        cliResult.code = 2
        validationResult.hasError = True
        return validationResult

    return validationResult
