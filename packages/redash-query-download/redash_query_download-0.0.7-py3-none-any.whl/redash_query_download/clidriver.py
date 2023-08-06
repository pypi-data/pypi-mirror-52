#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import pandas as pd
from redash_dynamic_query import RedashDynamicQuery
from datetime import datetime
import configparser
import os

def get_config(config_path):
    parser = configparser.RawConfigParser()
    config = os.path.expanduser(config_path)

    parser.read([config])

    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv

@click.command()
@click.option('-q', '--query_id', nargs=1, required=True, type=int)
@click.option('-p', '--parameters', nargs=2, type=(str, str), multiple=True)
@click.option('-o', '--output', nargs=1, type=str)
@click.option('-c', '--config', default='~/.rqdrc', nargs=1, type=str)
@click.option('-s', '--sequence', default='all', help='all, downlaod or execute')
@click.option('-i', '--ignore-error', is_flag=True)
def cmd(query_id, parameters, output, config, sequence, ignore_error):
    if sequence == "download":
        download_query(query_id, output, config, ignore_error)
    elif sequence == "execute":
        execute_query(query_id, parameters, output, config, ignore_error)
    else:
        execute_download_query(query_id, parameters, output, config, ignore_error)

def execute_download_query(query_id, parameters, output, config, ignore_error=True):
    if output == None:
        raise click.UsageError("Specify output option when sequence option is all.")

    if ignore_error == True:
        error = "ignore"
    else:
        error = "strict"
    query_paremters = {}
    for key, value in parameters:
        query_paremters[key] = value

    bind = {}
    if(parameters != ()):
        for key, value in parameters:
            bind.update([(key, value)])

    cfg = get_config(config)
    encoding = 'utf-8'
    if('redash.encoding' in cfg):
        encoding = cfg['redash.encoding']

    redash = RedashDynamicQuery(
        endpoint=cfg['redash.endpoint'],
        apikey=cfg['redash.apikey'],
        data_source_id=None,
        max_age=0,
        max_wait=1200,
    )

    result = redash.query(query_id=query_id, bind=bind)
    data = result['query_result']['data']
    columns = [column['name'] for column in data['columns']]
    query_df = pd.DataFrame(data['rows'], columns=columns)
    with open(output, mode="w", encoding=encoding, errors=error) as f:
        query_df.to_csv(f, index=False, header=True)

def download_query(query_id, output, config, ignore_error=True):
    if ignore_error == True:
        error = "ignore"
    else:
        error = "strict"

    cfg = get_config(config)
    encoding = 'utf-8'
    if('redash.encoding' in cfg):
        encoding = cfg['redash.encoding']

    redash = RedashDynamicQuery(
        endpoint=cfg['redash.endpoint'],
        apikey=cfg['redash.apikey'],
        data_source_id=None,
        max_age=0,
        max_wait=1200,
    )

    result = redash._api_queries(query_id=query_id)
    latest_query_data_id = result['latest_query_data_id']

    result = redash._api_query_results_json(query_id, latest_query_data_id)
    data = result['query_result']['data']
    columns = [column['name'] for column in data['columns']]
    query_df = pd.DataFrame(data['rows'], columns=columns)
    with open(output, mode="w", encoding=encoding, errors=error) as f:
        query_df.to_csv(f, index=False, header=True)

def execute_query(query_id, parameters, output, config, ignore_error=True):
    if ignore_error == True:
        error = "ignore"
    else:
        error = "strict"
    query_paremters = {}
    for key, value in parameters:
        query_paremters[key] = value

    bind = {}
    if(parameters != ()):
        for key, value in parameters:
            bind.update([(key, value)])

    cfg = get_config(config)
    encoding = 'utf-8'
    if('redash.encoding' in cfg):
        encoding = cfg['redash.encoding']

    redash = RedashDynamicQuery(
        endpoint=cfg['redash.endpoint'],
        apikey=cfg['redash.apikey'],
        data_source_id=None,
        max_age=0,
        max_wait=1200,
    )

    result = redash.query(query_id=query_id, bind=bind)

def main():
    cmd()
