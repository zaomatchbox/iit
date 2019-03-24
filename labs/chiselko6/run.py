import os

from src.builder.html.constants import DIR
from src.builder.html.gen import build
from src.docs.index import Indexer
from src.docs.linker import to_doc
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
    items = build(model, [])
    index = Indexer()
    for item in items:
        index.add(to_doc(item))
    index.index()
    while True:
        print('Enter your query:', end=' ')
        query = input()
        if query == 'get_distance':
            src, dest = input().split()
            src = os.path.join(DIR, src.strip())
            dest = os.path.join(DIR, dest.strip())
            print(index.get_distance(src, dest))
        else:
            relevant_docs = index.search(query)
            print('Result:')
            for doc in relevant_docs:
                print(f'{doc.name}: {doc.gate}')
