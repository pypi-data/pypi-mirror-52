# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import List, Optional

import connect.models
from .base import BaseModel
from connect.models.schemas import ValueChoiceSchema, ConstraintsSchema, ParamSchema


class ValueChoice(BaseModel):
    """ A value choice for a parameter. """

    _schema = ValueChoiceSchema()

    value = None  # type: str
    """ (str) Value. """

    label = None  # type: str
    """ (str) Label. """


class Constraints(BaseModel):
    """ Parameter constraints. """

    _schema = ConstraintsSchema()

    hidden = None  # type: bool
    """ (bool) Is the parameter hidden? """

    required = None  # type: bool
    """ (bool) Is the parameter required? """

    choices = None  # type: List[ValueChoice]
    """ (List[:py:class:`.ValueChoice`]) Parameter value choices. """

    unique = None  # type: bool
    """ (bool) Is the constraint unique? """


class Param(BaseModel):
    """ Parameters are used in product and asset definitions. """

    _schema = ParamSchema()

    name = None  # type: str
    """ (str) Name of parameter. """

    description = None  # type: str
    """ (str) Description of parameter. """

    type = None  # type: str
    """ (str) Type of parameter. """

    value = None  # type: Optional[str]
    """ (str|None) Value of parameter. """

    value_error = None  # type: Optional[str]
    """ (str|None) Error indicated for parameter. """

    value_choice = None  # type: Optional[List[str]]
    """ (List[str]|None) Available choices for parameter. """

    # Undocumented fields (they appear in PHP SDK)

    title = None  # type: Optional[str]
    """ (str|None) Title for parameter. """

    scope = None  # type: Optional[str]
    """ (str|None) Scope of parameter. """

    constraints = None  # type: Optional[Constraints]
    """ (:py:class:`.Constraints` | None) Parameter constraints. """

    value_choices = None  # type: Optional[List[ValueChoice]]
    """ (List[str]|None) Available dropdown choices for parameter. """

    phase = None  # type: Optional[str]
    """ (str|None) Param phase. """

    events = None  # type: Optional[connect.models.Events]
    """ (:py:class:`.Events` | None) Events. """

    marketplace = None  # type: Optional[connect.models.Marketplace]
    """ (:py:class:`.Marketplace` | None) Marketplace. """
