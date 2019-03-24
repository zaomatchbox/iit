from src.builder.html.gen import build
from src.gen import gen_dims, gen_entities
from src.parser.parser import Parser


def try_gen():
    dims = gen_dims()
    entities = gen_entities(dims)
    build(dims, entities)


def try_parse():
    p = Parser()
    with open('./example.imml', 'r') as fin:
        for line in fin.readlines():
            p.feed(line)
    return p.model


if __name__ == '__main__':
    # try_gen()
    model = try_parse()
    print(len(model))
    print(len(model[0].levels))
    build(model, [])
