#!/usr/bin/env python3
import argparse
import sys


def main(args):

    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", help="The data to seed")
    args = parser.parse_args()
    sys.exit(main(args))
