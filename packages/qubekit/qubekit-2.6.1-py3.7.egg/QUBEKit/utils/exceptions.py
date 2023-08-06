#!/usr/bin/env python3

from importlib import import_module


def missing_import(name, fail_msg=''):
    """
    Generates a class which raises an import error when initialised.
    e.g. SomeClass = missing_import('SomeClass') will make SomeClass() raise ImportError
    """
    def init(self, *args, **kwargs):
        raise ImportError(
            f'The class {name} you tried to call is not importable; '
            f'this is likely due to it not doing installed.\n\n'
            f'{f"Fail Message: {fail_msg}" if fail_msg else ""}'
        )
    return type(name, (), {'__init__': init})


def try_load(engine, module):
    """
    Try to load a particular engine from a module.
    If this fails, a dummy class is imported in its place with an import error raised on initialisation.

    :param engine: Name of the engine (PSI4, OpenFF, ONETEP, etc).
    :param module: Name of the QUBEKit module (.psi4, .openff, .onetep, etc).
    :return: Either the engine is imported as normal, or it is replaced with dummy class which
    just raises an import error with a message.
    """
    try:
        module = import_module(module, __name__)
        return getattr(module, engine)
    except (ModuleNotFoundError, AttributeError) as exc:
        print(f'Warning, failed to load: {engine}; continuing for now.\nReason: {exc}\n')
        return missing_import(engine, fail_msg=str(exc))


class OptimisationFailed(Exception):
    """
    Raise for seg faults from PSI4 - geomeTRIC/Torsiondrive/QCEngine interactions.
    This should mean it's more obvious to users when there's a segfault.
    """
    pass


class HessianCalculationFailed(Exception):
    """

    """

    pass


class TorsionDriveFailed(Exception):
    """

    """

    pass


class PickleFileNotFound(Exception):
    """
    Cannot find .QUBEKit_states.
    """

    pass


class QUBEKitLogFileNotFound(Exception):
    """
    Cannot find QUBEKit_log.txt. This is only raised when a recursive search fails.
    """

    pass


class FileTypeError(Exception):
    """
    Invalid file type e.g. trying to read a mol file when we only accept pdb or mol2.
    """
    pass


class TopologyMismatch(Exception):
    """
    This indicates that the topology of a file does not match the stored topology.
    """

    pass


class ChargemolError(Exception):
    """
    Chargemol did not execute properly.
    """

    pass


class Psi4Error(Exception):
    """
    Psi4 did not execute properly
    """

    pass

