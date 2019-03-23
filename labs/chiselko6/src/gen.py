from typing import Iterable, List

from .schema.attr import Attr
from .schema.dim import Dimension
from .schema.entity import Entity
from .schema.hier import Hierarchy
from .schema.level import Level


def gen_entities(dims: Iterable[Dimension]) -> List[Entity]:
    return [
        Entity(
            dim=dims[0],
            level=dims[0].levels[0],
            attrs={'Attr111': 'something', 'Attr113': 'here'},
        ),
        Entity(
            dim=dims[1],
            level=dims[1].levels[1],
            attrs={'Attr221': 'blabla'},
        ),
        Entity(
            dim=dims[0],
            level=dims[0].levels[2],
            attrs={'Attr133': 'lala'},
        ),
    ]


def gen_dims() -> List[Dimension]:
    attrs = [
        Attr('Attr111', 'string'),
        Attr('Attr112', 'string'),
        Attr('Attr113', 'numeric'),

        Attr('Attr121', 'string'),
        Attr('Attr122', 'string'),
        Attr('Attr123', 'numeric'),

        Attr('Attr131', 'string'),
        Attr('Attr132', 'string'),
        Attr('Attr133', 'numeric'),

        Attr('Attr211', 'string'),
        Attr('Attr212', 'string'),
        Attr('Attr213', 'numeric'),

        Attr('Attr221', 'string'),
        Attr('Attr222', 'string'),
        Attr('Attr223', 'numeric'),
    ]
    levels = [
        Level(
            name='Level11',
        ).add_attrs(attrs[:3]),
        Level(
            name='Level12',
        ).add_attrs(attrs[3:6]),
        Level(
            name='Level13',
        ).add_attrs(attrs[6:9]),
        Level(
            name='Level21',
        ).add_attrs(attrs[9:12]),
        Level(
            name='Level22',
        ).add_attrs(attrs[12:15]),
    ]
    hiers = [
        Hierarchy(
            name='Hier13',
        )
        .add_level(levels[0])
        .add_level(levels[2]),
        Hierarchy(
            name='Hier123',
        )
        .add_level(levels[0])
        .add_level(levels[1])
        .add_level(levels[2]),
        Hierarchy(
            name='Hier34',
        )
        .add_level(levels[3])
        .add_level(levels[4]),
    ]
    return [
        Dimension(
            name='Dim1',
        )
        .add_levels(levels[:3])
        .add_hiers(hiers[:2]),
        Dimension(
            name='Dim2',
        )
        .add_levels(levels[3:])
        .add_hier(hiers[2]),
    ]
