#!/usr/bin/env python

import argparse
import logging
import os
from timeit import default_timer as timer

from dumper import dump
from parser import parse


def set_log_level(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def get_solver(solver_name):
    if solver_name == 'dummy':
        from dummy import DummySolver
        return DummySolver()
    elif solver_name == 'chunky':
        from chunky import ChunkySolver
        return ChunkySolver()


def main():
    parser = argparse.ArgumentParser(description='run solver',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_file_paths', nargs='+', type=str, help='input file paths e.g. a_example.in')
    parser.add_argument('--out', dest="output_file_path", default='out', type=str,
                        help='output file path e.g. a_example.out')
    parser.add_argument('--solver', type=str, default='dummy', help='solver name e.g. <solver>.py')
    parser.add_argument('--debug', action='store_true', help='for debug purpose')
    args = parser.parse_args()
    set_log_level(args)

    for input_file_path in args.input_file_paths:
        start = timer()
        images = parse(input_file_path)
        end = timer()

        logging.debug('parsing input took %s s', end - start)

        start = timer()
        solver = get_solver(args.solver)
        slides = solver.solve(images)
        end = timer()

        logging.debug('solving took %s s', end - start)

        start = timer()
        file_name, _ = os.path.splitext(input_file_path)
        dump(slides, file_name + '.out')
        end = timer()

        logging.debug('dumping took %s s', end - start)


if __name__ == '__main__':
    main()
