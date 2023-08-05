"""
@author: Scott Orr

This subpackage provides XML- and JSON-based representations of the Coalesce
Java classes, and functions to manipulate them.

Most of the modules in the subpackage define classes and functions based on
the Coalesce entity XSD; the classes can be instanced from XML (string)
objects and exported to XML using the functions in
:mod:`~pyCoalesce.classes.entity_utilities`.  The
:mod:`~pyCoalesce.classes.entity` module is auto-generated by the
:mod:`generateDS` package, and its classes should not be instanced directly;
instead, instance the classes in :mod:`~pyCoalesce.classes.coalesce_entity`,
or, for templates,
:class:`~pyCoalesce.classes.coalesce_entity_template.CoalesceEntityTemplate`
in :mod:`~pyCoalesce.classes.coalesce_entity_template`.

Because Python package tend not to handle XML entities very gracefully,
Coalesce XML entities are represented as nested objects in
:mod:`pyCoalesce`, meaning that type of entity component has its own subclass.

For the most part, :mod:`pyCoalesce` does not include classes or functions for
handling the JSON versions of Coalesce objects:  because of the close
correspondence between JSON objects and Python :class:`dict` and :class:`list`
objects, manipulating Coalesce JSON objects in Python in relatively simple,
and providing custom classes for this purpose would be superfluous.  The one
exception is the :class:`pyCoalesce.classes.coalesce_JSON.CoalesceAPILinkage`
class, which provides an easy means of converting XML-based
:class:`pyCoalesce.classes.coalesce_entity.CoalesceLinkage` objects to and
from JSON, a useful feature given that the Coalese Linkage API does not
include an XML option.

All classes and functions in this subpackage can be imported directly from
the subpackage, omitting the module name.

"""

from coalesce_entity import *
from coalesce_entity_template import CoalesceEntityTemplate
from entity_utilities import *
from coalesce_json import *

__all__ = ["coalesce_entity", "coalesce_entity_template", "entity_utilities",
           "coalesce_json"]
