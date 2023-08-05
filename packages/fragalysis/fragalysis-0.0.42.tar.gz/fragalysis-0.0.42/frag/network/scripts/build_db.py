#!/usr/bin/env python
#
# Build fragment network.
# If using Docker start container like this:
# docker run -it --rm -v $PWD:$PWD:z -u $(id -u):$(id -g) informaticsmatters/fragalysis:0.0.17 bash
#
# Input in SMILES format needs to be SMILES<space>ID<space>OTHER<space>FIELDS
# SMILES and ID columns are needed.
#
# Run like this:
# path/to/fragalysis/frag/network/scripts/build_db.py --non_isomeric --input smiles.txt --base_dir .
# In Docker container path/to/fragalysis is /usr/local/fragalysis. e.g.
# /usr/local/fragalysis/frag/network/scripts/build_db.py --non_isomeric --input nk.txt --base_dir .


import argparse
import os
import sys

from rdkit import Chem

from frag.network.models import NodeHolder, Attr
from frag.utils.network_utils import build_network, write_data
from frag.utils.parser import parse_mols

from tqdm import tqdm


def main():
    # Read in a SD or SMILES file - then write out into a specified directory
    parser = argparse.ArgumentParser(
        description="Convert a SMILES or SDFile to input for Astex Fragment network."
    )
    parser.add_argument("--input")
    parser.add_argument("--input_format", default="smi")
    parser.add_argument("--base_dir")
    parser.add_argument("--isomeric", dest="iso_flag", action="store_true")
    parser.add_argument("--non_isomeric", dest="iso_flag", action="store_false")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", dest="verbosity", action="store_const", const=1)
    group.add_argument("-vv", dest="verbosity", action="store_const", const=2)

    parser.set_defaults(verbosity=0)
    parser.set_defaults(iso_flag=True)

    args = parser.parse_args()

    # Do we have an input and base directory?
    if not args.input:
        print('ERROR: Must specify an input')
        sys.exit(1)
    if not os.path.isfile(args.input):
        print('ERROR: input (%s) does not exist' % args.input)
        sys.exit(1)
    if not args.base_dir:
        print('ERROR: Must specify a base directory')
        sys.exit(1)
    if not os.path.isdir(args.base_dir):
        print('ERROR:input base directory (%s) does not exist' % args.base_dir)
        sys.exit(1)

    tqdm_disable = True if args.verbosity else False
    attrs = []
    id = 0
    mols = parse_mols(args.input, args.input_format)
    for x in tqdm(mols, disable=tqdm_disable):
        print("Processing " + Chem.MolToSmiles(x, isomericSmiles=True))
        if x is None:
            continue
        attr = Attr(
            Chem.CanonSmiles(Chem.MolToSmiles(x, isomericSmiles=True)),
            ["EM", x.GetProp("_Name")],
        )
        attrs.append(attr)
        id += 1
    if not os.path.isdir(args.base_dir):
        os.mkdir(args.base_dir)
    # Build the network
    node_holder = NodeHolder(iso_flag=args.iso_flag)
    max_frags = 0
    node_holder = build_network(attrs, node_holder,
                                max_frags,
                                args.base_dir,
                                args.verbosity)
    # Write the data out
    write_data(args.base_dir, node_holder, attrs)


if __name__ == "__main__":
    main()
