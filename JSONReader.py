#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Added by Sayeed Salam sxs149331@utdallas.edu

import json
import logging
import sys

from dateutil import parser
from datetime import datetime
from dateutil import parser

try:
    from mordecai import query_mordecai
except ImportError:
    logging.warn("Mordecai not installed")

from petrarch3 import utilities


def read_json(article_main):
    # import pdb
    holding = {}
    sentence_limit = 7

    try:
        if ('date' not in article_main) or (len(article_main['date']) == 0):
            dateObject = datetime.now()
            article_date = parser.parse(dateObject).strftime('%Y%m%d')
        else:
            logging.info("{}".format(article_main))
            dateObject = article_main['date']
            article_date = parser.parse(dateObject).strftime('%Y%m%d')

        article = json.loads(article_main['phrases'], encoding='utf-8')

        entry_id = article_main['doc_id']
        
        sent_dict = {}
        meta_content = {'date': article_date}
        for sentence in article[0: sentence_limit]:
 
            sent_id = sentence['sen_id']

            parsed_text = utilities._format_parsed_str(sentence['parse_tree'])
    
            geodata = {}
            if False: # Disable mordecai
                geodata = query_mordecai(sentence['sentence'])

            sent_dict[sent_id] = {'content': sentence['sentence'],
                                  'parsed': parsed_text,
                                  'geo-location': geodata}

        content_dict = {'sents': sent_dict,
                        'meta': meta_content,
                        'mongo_id': article_main['mongo_id']}
        holding[entry_id] = content_dict
        return holding
    except Exception as e:
        logging.error(e)
        logging.error(e.args)
        logging.error(sys.exc_info()[0])
        raise e

        return {}
