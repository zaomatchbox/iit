from typing import Iterable
import os
import shutil

from ...schema.attr import Attr
from ...schema.dim import Dimension
from ...schema.entity import Entity
from ...schema.hier import Hierarchy
from ...schema.level import Level

from .constants import ATTR_TYPES, DIR
from .links import (
    gen_attr_link, gen_dim_link, gen_hier_link, gen_level_link
)


def build_dim(dim: Dimension) -> str:
    initial = f'<h1>Dimension: <b>{dim.name}</b></h1>'
    info = f'<h2>Info: {dim.info}</h2>'
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
    return f'<div>{initial}</div><div>{info}</div><div>{all_levels}</div><div>{all_hiers}</div>'


def build_level(level: Level) -> str:
    initial = f'<i style="font-size: 24px;"><a href="{gen_level_link(level)}">{level.name}</a></i>'
    mapped = []
    attr_wrapper = '<div style="margin-left: 16px;">{}</div>'
    for attr in level.attrs:
        mapped.append(attr_wrapper.format(build_attr(attr)))
    all_attrs = ''.join(mapped)
    return f'<div style="margin-left: 16px;">{initial}{all_attrs}</div>'


def build_hierarchy(hier: Hierarchy) -> str:
    html_levels = []
    for level in hier.levels:
        html_levels.append(
            f'<a href="{gen_level_link(level)}">{level.name}</a>')
    all_levels = ', '.join(html_levels)
    return f'<div><b style="font-size: 24px;"><a href="{gen_hier_link(hier)}">{hier.name}</a></b>: {all_levels}</div>'


def build_attr(attr: Attr) -> str:
    return f'<span style="font-size: 16px;"><a href="{gen_attr_link(attr)}">{attr.name} ({ATTR_TYPES[attr.type]})</a></span>'


def build_extended_attr(attr: Attr) -> str:
    props = f'<div><h1>Attribute: <b>{attr.name}</b> ({ATTR_TYPES[attr.type]})</h1></div>'
    info = f'<div><h2>Info: {attr.info}</h2></div>'
    level = f'<div><h3>Level:  <i><a href="{gen_level_link(attr.level)}">{attr.level.name}</a></i></h3></div>'
    dim = f'<div><span>Dimension: <a href="{gen_dim_link(attr.level.dim)}">{attr.level.dim.name}</a></span></div>'
    return f'<div>{props}{info}{level}{dim}</div>'


def build_extended_level(level: Level) -> str:
    initial = f'<div><h1>Level: <b>{level.name}</b></h1></div>'
    info = f'<div><h2>Info: {level.info}</h2></div>'
    dim = f'<div><h3>Dimension: <i><a href="{gen_dim_link(level.dim)}">{level.dim.name}</a></i></h3></div>'
    mapped = []
    attr_wrapper = '<div style="margin-left: 32px;">{}</div>'
    for attr in level.attrs:
        mapped.append(attr_wrapper.format(build_attr(attr)))
    all_attrs = ''.join(mapped)
    return f'<div>{initial}{info}{dim}{all_attrs}</div>'


def build_extended_hierarchy(hier: Hierarchy) -> str:
    initial = f'<div><h1>Hierarchy: <b>{hier.name}</b></h1></div>'
    info = f'<div><h2>Info: {hier.info}</h2></div>'
    dim = f'<div><h3>Dimension: <i><a href="{gen_dim_link(hier.dim)}">{hier.dim.name}</a></i></h3></div>'
    html_levels = []
    for level in hier.levels:
        html_levels.append(
            f'<a href="{gen_level_link(level)}">{level.name}</a>')
    all_levels = ', '.join(html_levels)
    return f'<div>{initial}{info}{dim}<div><h3>Levels: {all_levels}</h3></div></div>'


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
    os.makedirs(os.path.join(DIR, 'dim'))
    os.makedirs(os.path.join(DIR, 'level'))
    os.makedirs(os.path.join(DIR, 'hier'))
    os.makedirs(os.path.join(DIR, 'attr'))
    for dim in dims:
        res = build_dim(dim)
        with open(os.path.join(DIR, f'dim/{dim.id}.html'), 'w') as fout:
            fout.write(res)
        for level in dim.levels:
            res = build_extended_level(level)
            with open(os.path.join(DIR, f'level/{level.id}.html'), 'w') as fout:
                fout.write(res)
            for attr in level.attrs:
                res = build_extended_attr(attr)
                with open(os.path.join(DIR, f'attr/{attr.id}.html'), 'w') as fout:
                    fout.write(res)
        for hier in dim.hiers:
            res = build_extended_hierarchy(hier)
            with open(os.path.join(DIR, f'hier/{hier.id}.html'), 'w') as fout:
                fout.write(res)
    for e in entities:
        res = build_entity(e)
        with open(os.path.join(DIR, f'entity/{e.id}.html'), 'w') as fout:
            fout.write(res)
