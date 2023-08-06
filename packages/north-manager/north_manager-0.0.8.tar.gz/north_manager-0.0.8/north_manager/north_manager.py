import sys
from os import path
sys.path = [path.join(path.dirname(__file__), '..')] + sys.path
import logging
from invoke import Program, Collection
from north_manager.tasks import firmware, root

logging.basicConfig(level=logging.INFO, format='%(message)s')

root_collection = Collection.from_module(root)
root_collection.add_collection(Collection.from_module(firmware), 'firmware')

program = Program(version='0.0.1', namespace=root_collection)


def run():
    program.run(sys.argv)


if __name__ == '__main__':
    run()
