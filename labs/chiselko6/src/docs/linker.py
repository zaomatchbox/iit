from ..builder.html.links import (
    gen_attr_link, gen_dim_link, gen_hier_link, gen_level_link
)
from ..schema.attr import Attr
from ..schema.base import BaseSchemaModel
from ..schema.dim import Dimension
from ..schema.hier import Hierarchy
from ..schema.level import Level
from .models import Document


def to_doc(obj: BaseSchemaModel) -> Document:
    if isinstance(obj, Attr):
        links = [gen_dim_link(obj.level.dim), gen_level_link(obj.level)]
        return Document(name=obj.name,
                        content=obj.info,
                        links=links,
                        gate=gen_attr_link(obj))
    if isinstance(obj, Dimension):
        links = [gen_hier_link(hier) for hier in obj.hiers]
        for level in obj.levels:
            links.append(gen_level_link(level))
            links.extend([gen_attr_link(attr) for attr in level.attrs])
        return Document(name=obj.name,
                        content=obj.info,
                        links=links,
                        gate=gen_dim_link(obj))
    if isinstance(obj, Hierarchy):
        links = [gen_level_link(level) for level in obj.levels]
        links.append(gen_dim_link(obj.dim))
        return Document(name=obj.name,
                        content=obj.info,
                        links=links,
                        gate=gen_hier_link(obj))
    if isinstance(obj, Level):
        links = [gen_attr_link(attr) for attr in obj.attrs]
        links.append(gen_dim_link(obj.dim))
        return Document(name=obj.name,
                        content=obj.info,
                        links=links,
                        gate=gen_level_link(obj))
