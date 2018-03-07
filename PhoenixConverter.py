#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast
import pprint
import json
import logging
#import requests
import operator
import os
import pdb
import re
import sys
import time
import urllib

from EventCoder import EventCoder
try:
    from mordecai import query_mordecai
except ImportError:
    #logging.warn("Mordecai not installed")
    pass 


class PhoenixConverter:

    def __init__(self, geo_ip="localhost", geo_port="8080"):
        phoenix_data = json.load(open("phoenix_data.json","r"))

        self.goldstein_scale = phoenix_data.get("goldstein_score")
        self.quad_conversion = phoenix_data.get("quad_class")
        self.countries = phoenix_data.get("countries")
        self.root_actors = phoenix_data.get("root_actors")
        self.primary_agent = phoenix_data.get("primary_agents")
        self.geo_ip = geo_ip
        self.geo_port = geo_port
        self.iso_country_code = phoenix_data.get("iso_country_code")

        # logging.info(f"{self.primary_agent}")



    def process_cameo(self, event):
        """
        Provides the "root" CAMEO event, a Goldstein value for the full CAMEO code,
        and a quad class value.
        Parameters
        ----------
        event: Tuple.

                (DATE, SOURCE, TARGET, EVENT) format.
        Returns
        -------
        root_code: String.

                    First two digits of a CAMEO code. Single-digit codes have

                    leading zeros, hence the string format rather than
       event_quad: Int.

                        Quad class value for a root CAMEO category.

        goldstein: Float.
                    Goldstein value for the full CAMEO code.
        """

        #Goldstein values pulled from

        #http://eventdata.parusanalytics.com/cameo.dir/CAMEO.SCALE.txt

        root_code = event[:2]

        try:
            event_quad = self.quad_conversion[root_code]
        except KeyError:
            logging.error('Bad event: {}'.format(event))
            event_quad = ''

        try:
            goldstein = self.goldstein_scale[event]
        except KeyError:
            logging.info('\nMissing Goldstein Value: {}'.format(event))
            try:
                goldstein = self.goldstein_scale[root_code]
            except KeyError:
                logging.info('Bad event: {}'.format(event))
                goldstein = ''
        return root_code, event_quad, goldstein


    def process_actors(self, event):
        """
        Splits out the actor codes into separate fields to enable easier
        querying/formatting of the data.
        Parameters
        ----------
        event: Tuple.

                (DATE, SOURCE, TARGET, EVENT) format.
        Returns
        -------
        actors: Tuple.
                Tuple containing actor information. Format is
                (source, source_root, source_agent, source_others, target,
                target_root, target_agent, target_others). Root is either
                a country code or one of IGO, NGO, IMG, or MNC. Agent is
                one of GOV, MIL, REB, OPP, PTY, COP, JUD, SPY, MED, EDU, BUS, CRM,
                or CVL. The ``others`` contains all other actor or agent codes.
        """


        sauce = event
        if sauce[:3] in self.countries or sauce[:3] in self.root_actors:
            sauce_root = sauce[:3]
        else:
            sauce_root = ''

        if sauce[3:6] in self.primary_agent:
            sauce_agent = sauce[3:6]
        else:
            sauce_agent = ''
        sauce_others = ''

        if len(sauce) > 3:
            if sauce_agent:
                start = 6
                length = len(sauce[6:])
            else:
                start = 3
                length = len(sauce[3:])

            for i in range(start, start + length, 3):
                sauce_others += sauce[i:i + 3] + ';'

            sauce_others = sauce_others[:-1]

        actors = (sauce, sauce_root, sauce_agent, sauce_others)
        return actors


    def geoLocation(self, host, port, text):
        logger = logging.getLogger('pipeline_log')
        locationDetails = {'lat': '', 'lon': '', 'placeName': '', 'countryCode': '', 'stateName': '', 'restype': ''}

        #print cliffDict
        try:
            result = query_mordecai(text)
            lat = result[0]['lat']
            lon = result[0]['lon']
            countryCode = result[0]['countrycode']
            placeName = result[0]['placename']
            locationDetails = {'lat': lat, 'lon': lon, 'placeName': placeName, 'restype': 'country', 'countryCode': countryCode, 'stateName': ''}
            return locationDetails
        except:
            logging.error("ISSUE")
            return locationDetails


    def format(self, event_dict, additional_info={}):
        try:
            if len(event_dict) == 0:
                logging.warning(f"Empty Keys: {event_dict.keys()}")
                return {}

            docid = list(event_dict.keys())[0]

            # date8 = re.findall('[0-9]+', docid[0])[0]
            date8 = event_dict[docid]['meta']['date']
            # sents = doc_id[docid[0]]['sents']
            sents = event_dict[docid]['sents']

            phoenixDict = {}
            phoenixDict["code"] = None
            phoenixDict["root_code"] = None
            phoenixDict["quad_class"] = None
            phoenixDict["goldstein"] = None
            phoenixDict["source"] = None
            phoenixDict["target"] = None
            phoenixDict["src_actor"] = None
            phoenixDict["tgt_actor"] = None
            phoenixDict["src_agent"] = None
            phoenixDict["tgt_agent"] = None
            phoenixDict["src_other_agent"] = None
            phoenixDict["tgt_other_agent"] = None

            phoenixDict["date8"] = date8
            phoenixDict["year"] = date8[0:4]
            phoenixDict["month"] = date8[4:6]
            phoenixDict["day"] = date8[6:]
            phoenixDict["source"] = additional_info.get("source", "")
            phoenixDict["url"] = additional_info.get("url", "")

            # logging.warning(f"event_dict: {event_dict[docid].keys()}")
            phoenixDict["doc_id"] = event_dict.get('doc_id', None)
            phoenixDict["mongo_id"] = event_dict.get('mongo_id', None)

            events = []

            if (sents != None):
                for s in sents:
                    try:

                        info = sents[s]
                        if "meta" in info.keys():
                            meta = info["meta"]
                            # FIXME why is the dictionary redefined? do we need the code above?
                            phoenixDict = {}
                            if (('actorroot' in meta) and (len(meta['actorroot'].keys()) > 0)):
                                phoenixDict["code"] = list(meta['actorroot'].keys())[0][2]
                                phoenixDict["root_code"], phoenixDict["quad_class"], phoenixDict["goldstein"] = self.process_cameo( phoenixDict["code"])
                                phoenixDict["source"], phoenixDict["src_actor"], phoenixDict["src_agent"], phoenixDict[ "src_other_agent"] = self.process_actors(list(meta['actorroot'].keys())[0][0])
                                phoenixDict["target"], phoenixDict["tgt_actor"], phoenixDict["tgt_agent"], phoenixDict[ "tgt_other_agent"] = self.process_actors(list(meta['actorroot'].keys())[0][1])

                            # Geolocation is cancelled
                            if False:
                                geoDict = self.geoLocation(self.geo_ip, self.geo_port, info['content'])
                                phoenixDict['latitude'] = geoDict['lat']
                                phoenixDict['longitude'] = geoDict['lon']
                                phoenixDict['country_code'] = self.iso_country_code.get(geoDict['countryCode'],geoDict['countryCode'])
                                phoenixDict['geoname'] = geoDict['placeName'] + ' ' + geoDict['stateName']

                            phoenixDict['id'] = additional_info.get("mongo_id","")+"_"+str(s)
                            phoenixDict["date8"] = date8
                            phoenixDict["year"] = date8[0:4]
                            phoenixDict["month"] = date8[4:6]
                            phoenixDict["day"] = date8[6:]
                            phoenixDict["source"] = additional_info.get("source", "")
                            phoenixDict["url"] = additional_info.get("url", "")
                            phoenixDict["doc_id"] = event_dict[docid].get('doc_id', None)
                            phoenixDict["mongo_id"] = event_dict[docid].get('mongo_id', None)
                            events.append(phoenixDict)
                    except Exception as e:
                        logging.exception(e)
            return events

        except Exception as e :
            logging.error(e)
            logging.exception(e)
            return []


def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


