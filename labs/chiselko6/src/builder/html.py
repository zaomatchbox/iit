from typing import Iterable
import os
import shutil

from ..schema.attr import Attr
from ..schema.dim import Dimension
from ..schema.entity import Entity
from ..schema.hier import Hierarchy
from ..schema.level import Level

from .constants import DIR


def build_dim(dim: Dimension) -> str:
    initial = f'<b id={dim.id} style="font-size: 32px;">{dim.name}</b>'
    level_wrapper = '<div style="margin-left: 16px;">{}</div>'
    html_levels = []
    for level in dim.levels:
        html_levels.append(level_wrapper.format(build_level(level)))
    hier_wrapper = '<div style="margin-left: 16px;">{}</div>'
    html_hiers = []
    for hier in dim.hiers:
        html_hiers.append(hier_wrapper.format(build_hierarchy(hier)))
    all_levels = ''.join(html_levels)
    all_hiers = ''.join(html_hiers)
    return f'<div>{initial}<div></div>{all_levels}</div><div>{all_hiers}</div>'


def build_level(level: Level) -> str:
    initial = f'<i id={level.id} style="font-size: 24px;">{level.name}</i>'
    mapped = []
    attr_wrapper = '<div style="margin-left: 16px;">{}</div>'
    for attr in level.attrs:
        mapped.append(attr_wrapper.format(build_attr(attr)))
    all_attrs = ''.join(mapped)
    return f'<div style="margin-left: 16px;">{initial}{all_attrs}</div>'


def build_attr(attr: Attr) -> str:
    format = {
        'numeric': 'Num',
        'string': 'Str',
    }
    return f'<span id={attr.id} style="font-size: 16px;">{attr.name}({format[attr.type]})</span>'


def build_hierarchy(hier: Hierarchy) -> str:
    html_levels = []
    for level in hier.levels:
        level_link = os.path.join(DIR, f'{hier.dim.id}.html#{level.id}')
        html_levels.append(f'<a href="{level_link}">{level.name}</a>')
    all_levels = ', '.join(html_levels)
    return f'<div><b style="font-size: 24px;">{hier.name}</b>: {all_levels}</div>'


def build_entity(entity: Entity) -> str:
    dim_ref = os.path.join(DIR, f'{entity.dim.id}.html')
    dim = f'Dimension: <b style="font-size: 32px;"><a href="{dim_ref}">{entity.dim.name}</a></b>'
    level_ref = f'{dim_ref}#{entity.level.id}'
    level = f'Level: <b style="font-size: 24px;"><a href="{level_ref}">{entity.level.name}</a></b>'
    attr_value = '<div><i><a href="{}">{}</a></i>: {}</div>'
    attrs = []
    for key, value in entity.attrs.items():
        attr = entity.level.get_attr_by_name(key)
        attrs.append(attr_value.format(f'{dim_ref}#{attr.id}', key, value))
    return '<div>{}</div><div>{}</div><div>{}</div>'.format(
        dim,
        level,
        ''.join(attrs)
    )


def build(dims: Iterable[Dimension], entities: Iterable[Entity]) -> None:
    if os.path.exists(DIR):
        shutil.rmtree(DIR)
    os.makedirs(os.path.join(DIR, 'entity'))
    for dim in dims:
        res = build_dim(dim)
        with open(os.path.join(DIR, f'{dim.id}.html'), 'w') as fout:
            fout.write(res)
    for e in entities:
        res = build_entity(e)
        with open(os.path.join(DIR, f'entity/{e.id}.html'), 'w') as fout:
            fout.write(res)
