""" [ Autoload script ] """

from pathlib import Path
import typing
import inspect
import pkgutil
import importlib


#import os
import bpy
#import sys
from .construct import load_m
from .src.SystemInterface.EnsureModules import check_install
from .src.MaterialManagers.ManagerInstance import construct_mgm
#CUSTOM CLASS IMPORT


__all__ = (
    "init",
    "register",
    "unregister",
)

modules = []
ordered_classes = []

def init():
    """ [ get lists of modules and submodules ] """
    
    check_install()
    
    global modules  # pylint: disable=global-statement
    global ordered_classes  # pylint: disable=global-statement

    modules = get_all_submodules(Path(__file__).parent)
    ordered_classes = get_ordered_classes_to_register(modules)

def register():
    """[ register ]"""
    construct_mgm()
    for cls in ordered_classes:
        bpy.utils.register_class(cls)
    load_m()

    
    for module in modules:
        if module.__name__ == __name__:
            continue
        if hasattr(module, "register"):
            module.register()

def unregister():
    """ [ unregister classes ]"""
    debug = False
    for cls in reversed(ordered_classes):
        if debug:
            print(cls)
        bpy.utils.unregister_class(cls)

    for module in modules:
        if module.__name__ == __name__:
            continue
        if hasattr(module, "unregister"):
            module.unregister()


# Import modules
#################################################

def get_all_submodules(directory):
    """
    Returns:
        [ list ]: [ all submodules ]
    """
    return list(iter_submodules(directory, directory.name))

def iter_submodules(path, package_name):
    """[summary]

    Args:
        path ([type]): [description]
        package_name ([type]): [description]

    Yields:
        [type]: [description]
    """
    for name in sorted(iter_submodule_names(path)):
        yield importlib.import_module("." + name, package_name)

def iter_submodule_names(path, root=""):
    """[summary]

    Args:
        path ([type]): [description]
        root (str, optional): [description]. Defaults to "".

    Yields:
        [type]: [description]
    """
    for _, module_name, is_package in pkgutil.iter_modules([str(path)]):
        if is_package:
            sub_path = path / module_name
            sub_root = root + module_name + "."
            yield from iter_submodule_names(sub_path, sub_root)
        else:
            yield root + module_name


# Find classes to register
#################################################

def get_ordered_classes_to_register(modules): # pylint: disable=redefined-outer-name
    """[summary]

    Args:
        modules ([type]): [description]

    Returns:
        [type]: [description]
    """
    return toposort(get_register_deps_dict(modules))

def get_register_deps_dict(modules): # pylint: disable=redefined-outer-name
    """[summary]

    Args:
        modules ([type]): [description]

    Returns:
        [type]: [description]
    """
    deps_dict = {}
    classes_to_register = set(iter_classes_to_register(modules))
    for cls in classes_to_register:
        deps_dict[cls] = set(iter_own_register_deps(cls, classes_to_register))
    return deps_dict

def iter_own_register_deps(cls, own_classes):
    """[summary]

    Args:
        own_classes ([type]): [description]

    Yields:
        [type]: [description]
    """
    yield from (dep for dep in iter_register_deps(cls) if dep in own_classes)

def iter_register_deps(cls):
    """[ ]"""
    for value in typing.get_type_hints(cls, {}, {}).values():
        dependency = get_dependency_from_annotation(value)
        if dependency is not None:
            yield dependency

def get_dependency_from_annotation(value):
    """[ ]"""
    if isinstance(value, tuple) and len(value) == 2:
        if value[0] in (bpy.props.PointerProperty, bpy.props.CollectionProperty):
            return value[1]["type"]
    return None

def iter_classes_to_register(modules): # pylint: disable=redefined-outer-name
    """[ ]"""
    base_types = get_register_base_types()
    for cls in get_classes_in_modules(modules):
        if any(base in base_types for base in cls.__bases__):
            if not getattr(cls, "is_registered", False):
                yield cls
def get_classes_in_modules(modules): # pylint: disable=redefined-outer-name
    """[ ]"""
    classes = set()
    for module in modules:
        for cls in iter_classes_in_module(module):
            classes.add(cls)
    return classes

def iter_classes_in_module(module):
    """[ ]"""
    for value in module.__dict__.values():
        if inspect.isclass(value):
            yield value

def get_register_base_types():
    """[ ]"""
    return set(getattr(bpy.types, name) for name in [
        "Panel", "Operator", "PropertyGroup",
        "AddonPreferences", "Header", "Menu",
        "Node", "NodeSocket", "NodeTree",
        "UIList", "RenderEngine"
    ])


# Find order to register to solve dependencies
#################################################

def toposort(deps_dict):
    """[ ]"""
    sorted_list = []
    sorted_values = set()
    while len(deps_dict) > 0:
        unsorted = []
        for value, deps in deps_dict.items():
            if len(deps) == 0:
                sorted_list.append(value)
                sorted_values.add(value)
            else:
                unsorted.append(value)
        deps_dict = {value : deps_dict[value] - sorted_values for value in unsorted}
    return sorted_list
