#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 13:24:15 2017

@author: noore
"""

import argparse
import logging
from util.SBtab import SBtabTools
from equilibrator_api.pathway import ParsedPathway
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Calculate the Max-min Driving Force (MDF) of a pathway.')
    parser.add_argument(
        'infile', type=argparse.FileType(),
        help='path to input file containing reactions')
    parser.add_argument(
        'outfile', type=str,
        help='path to output PDF file')
    logging.getLogger().setLevel(logging.WARNING)

    args = parser.parse_args()

    sbtabs = SBtabTools.openMultipleSBtabFromFile(args.infile)
    tdict = dict([(t.getTableInformation()[1].upper(), t) for t in sbtabs])
    expected_tnames = ['REACTION', 'RELATIVEFLUX', 'CONCENTRATIONCONSTRAINT',
                       'REACTIONCONSTANT']
    assert set(expected_tnames).issubset(tdict.keys())

    sbtabs = [tdict[n] for n in expected_tnames]
    
    pp = ParsedPathway.from_full_sbtab(*sbtabs)
    
    output_pdf = PdfPages(args.outfile)
    mdf_res = pp.calc_mdf()
    
    output_pdf.savefig(mdf_res.conc_plot)
    output_pdf.savefig(mdf_res.mdf_plot)
    output_pdf.close()