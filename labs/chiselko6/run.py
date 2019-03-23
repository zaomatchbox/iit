from src.builder.html import build
from src.gen import gen_dims, gen_entities


if __name__ == '__main__':
    dims = gen_dims()
    entities = gen_entities(dims)
    build(dims, entities)
