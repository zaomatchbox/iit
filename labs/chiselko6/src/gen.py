from typing import Iterable, List

from .schema.attr import Attr
from .schema.dim import Dimension
from .schema.entity import Entity
from .schema.level import Level


def gen_entities(dims: Iterable[Dimension]) -> List[Entity]:
    return [
        Entity(
            dim=dims[0],
            level=dims[0].levels[0],
            attrs={'Attr11': 'something', 'Attr13': 'here'},
        ),
        Entity(
            dim=dims[1],
            level=dims[1].levels[1],
            attrs={'Attr41': 'something', 'Attr42': 'here'},
        ),
    ]


def gen_dims() -> List[Dimension]:
    return [
        Dimension(
            name='Dim1',
            levels=[
                Level(
                    name='Level1',
                    attrs=[
                        Attr('Attr11', 'string'),
                        Attr('Attr12', 'string'),
                        Attr('Attr13', 'numeric'),
                    ],
                ),
                Level(
                    name='Level2',
                    attrs=[
                        Attr('Attr21', 'string'),
                        Attr('Attr22', 'string'),
                        Attr('Attr3', 'numeric'),
                    ],
                ),
            ],
            hiers=[],
        ),
        Dimension(
            name='Dim2',
            levels=[
                Level(
                    name='Level3',
                    attrs=[
                        Attr('Attr31', 'string'),
                        Attr('Attr32', 'string'),
                        Attr('Attr33', 'numeric'),
                    ],
                ),
                Level(
                    name='Level4',
                    attrs=[
                        Attr('Attr41', 'string'),
                        Attr('Attr42', 'string'),
                        Attr('Attr43', 'numeric'),
                    ],
                ),
            ],
            hiers=[],
        ),
    ]
