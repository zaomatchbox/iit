import os

from ...schema.attr import Attr
from ...schema.dim import Dimension
from ...schema.hier import Hierarchy
from ...schema.level import Level
from .constants import DIR


def gen_dim_link(dim: Dimension) -> str:
    return os.path.join(DIR, f'dim/{dim.id}.html')


def gen_level_link(level: Level) -> str:
    return os.path.join(DIR, f'level/{level.id}.html')


def gen_attr_link(attr: Attr) -> str:
    return os.path.join(DIR, f'attr/{attr.id}.html')


def gen_hier_link(hier: Hierarchy) -> str:
    return os.path.join(DIR, f'hier/{hier.id}.html')
