#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Birdcage version 2.0.

    This python file takes two arguments as parameters.
    First, a json dictionary for options and second, an event data sentence. 
"""
import argparse
import json
import logging
import sys

import EventCoder
from EventCoder import EventCoder
from JSONReader import read_json

import petrarch3 # Using the Petrarch 3
from PhoenixConverter import PhoenixConverter


def main(param, data):
    logging.info(f"{param}")
    logging.info(f"{data}")

    # Run Event Coder ####################################################
    from petrarch3 import petrarch3, PETRglobals, PETRreader, utilities
    from petrarch3 import PETRtree as ptree

    config = petrarch3.utilities._get_data('data/config/', 'PETR_config.ini')
    petrarch3.PETRreader.parse_Config(config)
    petrarch3.read_dictionaries()

    # Run the formatter ##################################################
    for article in data:
        #coder = EventCoder(petrGlobal={})
        #events_dict = coder.gen_cameo_event(article) 
        article_dict = json.loads(article) # Catch error here
        events = read_json(article_dict)
        updated_events = petrarch3.do_coding(events)

        formatter = PhoenixConverter(geo_ip="35.224.178.74", geo_port="5000") 
        events = formatter.format(updated_events, {})
     
        # Output to stdout / write to mongo
        if events:
            print(">> {}".format(events))



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--param', type=json.loads,
                        default={}, help="A python dictionary for run options.")
    parser.add_argument('-d', '--data', type=str,
                        default={}, help="Sentence data in json form.")

    args = parser.parse_args()
    if args.data == '-':
        main(args.param, (line for line in sys.stdin))
    #main(args.param, args.data)

