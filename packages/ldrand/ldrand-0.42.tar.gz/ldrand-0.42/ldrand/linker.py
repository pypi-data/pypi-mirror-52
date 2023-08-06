"""
Enables the randomization of the link order during the building of programs.
It's used to create a wrapper for `ld` (@see ../scripts/ld).

An implementation of this wrapper in C++ is given in the ../scripts/linker directory.
This python implementation is only the fall back solution if the C++ version isn't available.

The link order randomization only works for compilers that use the `ld` tool.
"""

import random
import shutil
import typing as t
import os, json, subprocess

from ldrand.util import BIN_PATH


def link(argv: t.List[str], ld_tool: str):
    """
    Function that gets all argument the ``ld`` wrapper gets passed, randomized their order and executes the original
    ``ld``.

    :param argv: ``ld`` arguments
    :param ld_tool: used ``ld`` tool
    """
    args = argv[1:] # type: t.List[str]
    arg_groups = [] # type: t.List[t.Tuple[bool, t.List[str]]]

    def is_randomizable(arg: str) -> bool:
        return arg.startswith("-L") or arg.endswith(".o")

    new_args = args

    for arg in args:
        r = is_randomizable(arg)
        if not arg_groups or arg_groups[-1][0] != r:
            arg_groups.append((r, [arg]))
        else:
            arg_groups[-1][1].append(arg)

    for (r, g) in arg_groups:
        if r:
            random.shuffle(g)

        new_args = [x for (r, g) in arg_groups for x in g]
    cmd = "{} {}".format(ld_tool, " ".join(new_args))
    proc = subprocess.Popen(["/bin/sh", "-c", cmd], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.poll() > 0:
        raise OSError("Linker failed: out={!r}, err={!r}".format(out, err))


def process_linker(call: t.List[str]):
    """
    Uses the passed ``ld`` arguments to randomize the link order during linking.
    It's configured by environment variables.

    :param call: arguments for ``ld``
    """
    ld_tool = os.environ["LDRAND_LINKER"] \
        if "LDRAND_LINKER" in os.environ \
        else shutil.which("ld", path=os.environ["PATH"].replace(BIN_PATH + ":", ""))
    for i in range(0, int(os.environ["LDRAND_TRIES"]) if "LDRAND_TRIES" in os.environ else 10):
        try:
            link(call, ld_tool)
        except OSError:
            continue
        return
    os.system("{} {}".format(ld_tool, " ".join(call[1:])))
