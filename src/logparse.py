#!/usr/bin/python

import argparse
import csv
import datetime
import logging
import os
import re
import time
import sys
import traceback


__doc__ = """
Read one or more log files, filter entries by IP address, method, protocol, or status and write applicable entries to a CSV file.

Example:
    logparse -f ../data/data-1.log ../data/data-2.log -k method -e POST
"""

__version__ = "0.0.1"


def get_opts():
    """Return an argparse object."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--verbose", default=logging.INFO, action="store_const", const=logging.DEBUG, help="enable debug logging")
    parser.add_argument("-v", "--version", action="version", version=__version__, help="show version and exit")
    parser.add_argument("-t", "--time", dest="time", action="store_true", help="include execution time")
    parser.add_argument("-f", "--files", metavar="FILE", nargs="+", help="input file(s)")
    parser.add_argument("-o", "--output", help="output file name (default: output.csv)", default="output.csv")
    parser.add_argument("-k", "--filter_key", type=str, help="key to filter logs by; supported keys: ipaddr, method, protcol, status")
    parser.add_argument("-e", "--filter_value", type=str, help="value to filter logs by")

    args = parser.parse_args()
    logging.basicConfig(level=args.verbose)
    return args


def parse_log_data(log: str) -> list:
    """parse log entries and create a list of dictionaries where each dict represents a log entry

    example log entry:
        193.105.7.171 - - [24/Jan/2018:00:01:12 +0300] "GET /wp-includes/js/wp-emoji-release.min.js?ver=4.6.1 HTTP/1.0" 200 4012 "http://some-blog.ru/trenirovki/kak-sest-na-shpagat-v-domashnix-usloviyax-uprazhneniya/" "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.132 Mobile Safari/537.36"

    Args:
        log (str): file content as read from a log file

    Returns:
        list: list of dictionaries representing log entries
    """
    pattern = '''(?P<ip_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}?) - - \[(?P<timestamp>\d{1,2}\/\w{3,5}\/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}?)] "(?P<method>\w{3,6}?) (?P<path>\S+?) (?P<protocol>\S+?)" (?P<status>\d{3}?) (?P<bytes>\d+|\-?) "(?P<referrer>\S+?)" "(?P<user_agent>.*?)"'''
    return [m.groupdict() for m in re.finditer(pattern, log)]


def write_output_file(source: str, data: list, output_file="output.csv") -> None:
    """write logs from a source log file to an output csv file

    Args:
        source (str): name of file sourcing the logs
        data (list): list of dictionaries representing log entries
        output_file (str, optional): output file to write; Defaults to "output.csv".
    """
    if not data:
        return
    file_exists = os.path.exists(output_file)
    headers = list(data[0].keys())
    headers.insert(0, "source")
    with open(output_file, "a" if file_exists else "w") as f:
        writer = csv.DictWriter(f, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        for row in data:
            row["source"] = source
            writer.writerow(row)


def read_files(file_list: list, filter_key: str | None, filter_value: str | None, output_file: str | None) -> None:
    """read data from a list of log files; filter data based on key/value, and write matching log entries to a csv file

    Args:
        file_list (list): list of log file names to read/parse/filter
        filter_key (str | None): key to filter log entries on
        filter_value (str | None): value (of key) to filter log entries on
    """
    log_data = []
    for file_name in file_list:
        with open(file_name, "r") as f:
            log_data = parse_log_data(f.read())
            if filter_key and filter_value:
                filtered_data = [d for d in log_data if d[filter_key] == filter_value]
                logging.info(f"{file_name}: found {len(filtered_data)} log entries where {filter_key} is {filter_value}")
                write_output_file(source=file_name, data=filtered_data, output_file=output_file)
            else:
                write_output_file(source=file_name, data=log_data, output_file=output_file)


def main():
    try:
        opts = get_opts()
        if opts.time:
            start = datetime.datetime.now()
        
        # call function(s) to do work here
        read_files(opts.files, opts.filter_key, opts.filter_value, opts.output)

        if opts.time:
            end = datetime.datetime.now()
            logging.info(f"script completed in: {end - start}")
    except Exception as err:
        logging.error(err)
        if opts.verbose == 10:
            traceback.print_exc()
        return 255


if __name__ == "__main__":
    sys.exit(main())
