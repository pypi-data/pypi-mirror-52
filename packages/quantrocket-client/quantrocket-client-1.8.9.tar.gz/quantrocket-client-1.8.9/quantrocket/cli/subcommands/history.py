# Copyright 2017 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

def add_subparser(subparsers):
    _parser = subparsers.add_parser("history", description="QuantRocket historical market data CLI", help="Collect and query historical data")
    _subparsers = _parser.add_subparsers(title="subcommands", dest="subcommand")
    _subparsers.required = True

    examples = """
Create a new history database.

The historical data requirements you specify when you create a new database (bar size,
universes, etc.) are applied each time you collect data for that database.

Examples:

Create an end-of-day database called "arca-etf-eod" for a universe called "arca-etf":

    quantrocket history create-db 'arca-etf-eod' --universes 'arca-etf' --bar-size '1 day'

Create a similar end-of-day database, but collect primary exchange prices instead of
consolidated prices, adjust prices for dividends (=ADJUSTED_LAST), and use an explicit
start date:

    quantrocket history create-db 'arca-etf-eod' -u 'arca-etf' -z '1 day' --primary-exchange --bar-type 'ADJUSTED_LAST' -s 2010-01-01

Create a database of 1-minute bars showing the midpoint for a universe of forex pairs:

    quantrocket history create-db 'fx-1m' -u 'fx' -z '1 min' --bar-type MIDPOINT

Create a database of 1-second bars just before the open for a universe of Canadian energy
stocks in 2016:

    quantrocket history create-db 'tse-enr-929' -u 'tse-enr' -z '1 secs' --outside-rth --times 09:29:55 09:29:56 09:29:57 09:29:58 09:29:59 -s 2016-01-01 -e 2016-12-31

Create a database for collecting Sharadar prices:

    quantrocket history create-db 'sharadar-1d' --vendor 'sharadar'
    """
    parser = _subparsers.add_parser(
        "create-db",
        help="create a new history database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the code to assign to the database (lowercase alphanumerics and hyphens only)")
    parser.add_argument(
        "-u", "--universes",
        metavar="UNIVERSE",
        nargs="*",
        help="include these universes")
    parser.add_argument(
        "-i", "--conids",
        metavar="CONID",
        nargs="*",
        help="include these conids")
    parser.add_argument(
        "-s", "--start-date",
        metavar="YYYY-MM-DD",
        help="collect history back to this start date (default is to collect as far back as data "
        "is available)")
    parser.add_argument(
        "-e", "--end-date",
        metavar="YYYY-MM-DD",
        help="collect history up to this end date (default is to collect up to the present)")
    parser.add_argument(
        "-v", "--vendor",
        metavar="VENDOR",
        choices=["ib", "sharadar"],
        help="the vendor to collect data from (default 'ib'. Possible choices: "
        "%(choices)s)")
    parser.add_argument(
        "-z", "--bar-size",
        metavar="BAR_SIZE",
        choices=[
            "1 secs", "5 secs", "10 secs", "15 secs", "30 secs",
            "1 min", "2 mins", "3 mins", "5 mins", "10 mins", "15 mins", "20 mins", "30 mins",
            "1 hour", "2 hours", "3 hours", "4 hours", "8 hours",
            "1 day",
            "1 week",
            "1 month"],
        help="the bar size to collect. Possible choices: %(choices)s")
    parser.add_argument(
        "-t", "--bar-type",
        metavar="BAR_TYPE",
        choices=["TRADES",
                 "ADJUSTED_LAST",
                 "MIDPOINT",
                 "BID",
                 "ASK",
                 "BID_ASK",
                 "HISTORICAL_VOLATILITY",
                 "OPTION_IMPLIED_VOLATILITY"],
        help="the bar type to collect (if not specified, defaults to MIDPOINT for forex and "
        "TRADES for everything else). Possible choices: %(choices)s")
    parser.add_argument(
        "-o", "--outside-rth",
        action="store_true",
        help="include data from outside regular trading hours (default is to limit to regular "
        "trading hours)")
    parser.add_argument(
        "-p", "--primary-exchange",
        action="store_true",
        help="limit to data from the primary exchange")
    times_group = parser.add_mutually_exclusive_group()
    times_group.add_argument(
        "--times",
        nargs="*",
        metavar="HH:MM:SS",
        help="limit to these times (refers to the bar's start time; mutually exclusive "
        "with --between-times)")
    times_group.add_argument(
        "--between-times",
        nargs=2,
        metavar="HH:MM:SS",
        help="limit to times between these two times (refers to the bar's start time; "
        "mutually exclusive with --times)")
    parser.add_argument(
        "--shard",
        metavar="HOW",
        choices=["year", "month", "day", "time", "conid", "conid,time", "off"],
        help="whether and how to shard the database, i.e. break it into smaller pieces. "
        "Required for intraday databases. Possible choices are `year` (separate "
        "database for each year), `month` (separate database for each year+month), "
        "`day` (separate database for each day), `time` (separate database for each bar "
        "time), `conid` (separate database for each security), `conid,time` (duplicate "
        "copies of database, one sharded by conid and the other by time),or `off` (no "
        "sharding). See http://qrok.it/h/shard for more help.")
    parser.add_argument(
        "-n", "--no-config",
        action="store_true",
        help="create a database with no config (data can be loaded manually instead of collected "
        "from a vendor)")
    parser.add_argument(
        "-f", "--config-file",
        dest="config_filepath_or_buffer",
        metavar="CONFIG_FILE",
        help="the path to a YAML config file defining the historical data requirements")
    parser.set_defaults(func="quantrocket.history._cli_create_db")

    examples = """
List history databases.

Examples:

    quantrocket history list
    """
    parser = _subparsers.add_parser(
        "list",
        help="list history databases",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func="quantrocket.history._cli_list_databases")

    examples = """
Collect historical market data from IB and save it to a history database. The request is queued
and the data is collected asynchronously.

Examples:

Collect historical data for 3 history databases of Japanese stocks:

    quantrocket history collect 'jpn-lrg-1d' 'jpn-mid-1d' 'jpn-sml-1d'

Collect how far back data is available but don't yet collect the data:

    quantrocket history collect 'usa-stk-15min' --availability

Collect historical data for a database of US futures, using the priority queue to jump
in front of other queued collections:

    quantrocket history collect 'globex-10m' --priority
    """
    parser = _subparsers.add_parser(
        "collect",
        help="collect historical market data from IB and save it to a history database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "codes",
        metavar="CODE",
        nargs="+",
        help="the database code(s) to collect data for")
    parser.add_argument(
        "-p", "--priority",
        action="store_true",
        help="use the priority queue (default is to use the standard queue)")
    parser.add_argument(
        "-i", "--conids",
        nargs="*",
        metavar="CONID",
        help="collect history for these conids, overriding config "
        "(typically used to collect a subset of securities)")
    parser.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="collect history for these universes, overriding config "
        "(typically used to collect a subset of securities)")
    parser.add_argument(
        "-s", "--start-date",
        metavar="YYYY-MM-DD",
        help="collect history back to this start date, overriding config")
    parser.add_argument(
        "-e", "--end-date",
        metavar="YYYY-MM-DD",
        help="collect history up to this end date, overriding config")
    parser.add_argument(
        "-a", "--availability",
        action="store_true",
        dest="availability_only",
        help="determine and store how far back data is available but "
        "don't yet collect the data")
    parser.add_argument(
        "--delist-missing",
        action="store_true",
        default=False,
        help="auto-delist securities that are no longer available from IB")
    parser.set_defaults(func="quantrocket.history._cli_collect_history")

    examples = """
Get the current queue of historical data collections.

Examples:

    quantrocket history queue
    """
    parser = _subparsers.add_parser(
        "queue",
        help="get the current queue of historical data collections",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(func="quantrocket.history._cli_get_history_queue")

    examples = """
Cancel running or pending historical data collections.

Examples:

Cancel all queued collections for a database called 'jpn-lrg-1d':

    quantrocket history cancel 'jpn-lrg-1d'

Cancel queued collections for a database called 'jpn-lrg-1d', but only in the standard queue:

    quantrocket history cancel 'jpn-lrg-1d' --queues standard
    """
    parser = _subparsers.add_parser(
        "cancel",
        help="cancel running or pending historical data collections",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "codes",
        metavar="CODE",
        nargs="+",
        help="the database code(s) to cancel collections for")
    parser.add_argument(
        "-q", "--queues",
        metavar="QUEUE",
        choices=["standard", "priority"],
        help="only cancel collections in these queues. Possible choices: %(choices)s")
    parser.set_defaults(func="quantrocket.history._cli_cancel_collections")

    examples = """
Wait for historical data collection to finish.

Examples:

Wait at most 10 minutes for data collection to finish for a database called 'fx-1h':

    quantrocket history wait 'fx-1h' -t 10min
    """
    parser = _subparsers.add_parser(
        "wait",
        help="wait for historical data collection to finish",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "codes",
        metavar="CODE",
        nargs="+",
        help="the database code(s) to wait for")
    parser.add_argument(
        "-t", "--timeout",
        metavar="TIMEDELTA",
        help="time out if data collection hasn't finished after this much time (use Pandas "
        "timedelta string, e.g. 30sec or 5min or 2h)")
    parser.set_defaults(func="quantrocket.history._cli_wait_for_collections")

    examples = """
Load market data from a CSV file into a history database.

Examples:

Load market data from a CSV into a database called "lse-bid-ask":

    quantrocket history load lse-bid-ask bidask.csv

Copy a subset of market data from one history database to another.

    quantrocket history get nyse-eod --universes nyse-sml | quantrocket history load nyse-sml-eod
    """
    parser = _subparsers.add_parser(
        "load",
        help="load market data from a CSV file into a history database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        help="the database code to load into")
    parser.add_argument(
        "infilepath_or_buffer",
        metavar="infile",
        nargs="?",
        default="-",
        help="CSV file containing market data (omit to read file from stdin)")
    parser.set_defaults(func="quantrocket.history._cli_load_history_from_file")

    examples = """
Query historical market data from a history database and download to file.

Examples:

Download a CSV of all historical market data since 2015 from a database called
"arca-eod" to a file called arca.csv:

    quantrocket history get arca-eod --start-date 2015-01-01 -o arca.csv
    """
    parser = _subparsers.add_parser(
        "get",
        help="query historical market data from a history database and download to file",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the code of the database to query")
    filters = parser.add_argument_group("filtering options")
    filters.add_argument(
        "-s", "--start-date",
        metavar="YYYY-MM-DD",
        help="limit to history on or after this date")
    filters.add_argument(
        "-e", "--end-date",
        metavar="YYYY-MM-DD",
        help="limit to history on or before this date")
    filters.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="limit to these universes")
    filters.add_argument(
        "-i", "--conids",
        type=int,
        nargs="*",
        metavar="CONID",
        help="limit to these conids")
    filters.add_argument(
        "--exclude-universes",
        nargs="*",
        metavar="UNIVERSE",
        help="exclude these universes")
    filters.add_argument(
        "--exclude-conids",
        type=int,
        nargs="*",
        metavar="CONID",
        help="exclude these conids")
    filters.add_argument(
        "-t", "--times",
        nargs="*",
        metavar="HH:MM:SS",
        help="limit to these times")
    outputs = parser.add_argument_group("output options")
    outputs.add_argument(
        "-o", "--outfile",
        metavar="OUTFILE",
        dest="filepath_or_buffer",
        help="filename to write the data to (default is stdout)")
    output_format_group = outputs.add_mutually_exclusive_group()
    output_format_group.add_argument(
        "-j", "--json",
        action="store_const",
        const="json",
        dest="output",
        help="format output as JSON (default is CSV)")
    output_format_group.add_argument(
        "-p", "--pretty",
        action="store_const",
        const="txt",
        dest="output",
        help="format output in human-readable format (default is CSV)")
    outputs.add_argument(
        "-f", "--fields",
        metavar="FIELD",
        nargs="*",
        help="only return these fields (pass '?' or any invalid fieldname to see "
        "available fields)")
    outputs.add_argument(
        "--tz-naive",
        action="store_true",
        help="return timestamps without UTC offsets: 2018-02-01T10:00:00 (default is to "
        "include UTC offsets: 2018-02-01T10:00:00-4000)")
    outputs.add_argument(
        "-c", "--cont-fut",
        choices=["concat"],
        metavar="HOW",
        help="stitch futures into continuous contracts using this method "
        "(default is not to stitch together). Possible choices: %(choices)s")
    parser.set_defaults(func="quantrocket.history._cli_download_history_file")

    examples = """
Query historical market data availability from a history database and download
to file.

This command is normally called after running:

    quantrocket history collect [DB] --availability

Examples:

Download a CSV of available start dates by ticker from a database called
"usa-stk" to a file called start_dates.csv:

    quantrocket history availability usa-stk -o start_dates.csv
    """
    parser = _subparsers.add_parser(
        "availability",
        help="query historical market data availability from a history database "
        "and download to file",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        metavar="CODE",
        help="the code of the database to query")
    outputs = parser.add_argument_group("output options")
    outputs.add_argument(
        "-o", "--outfile",
        metavar="OUTFILE",
        dest="filepath_or_buffer",
        help="filename to write the data to (default is stdout)")
    output_format_group = outputs.add_mutually_exclusive_group()
    output_format_group.add_argument(
        "-j", "--json",
        action="store_const",
        const="json",
        dest="output",
        help="format output as JSON (default is CSV)")
    parser.set_defaults(func="quantrocket.history._cli_download_history_availability_file")

    examples = """
Return the configuration for a history database.

Examples:

Return the configuration for a database called "jpn-lrg-15m":

    quantrocket history config 'jpn-lrg-15m'
    """
    parser = _subparsers.add_parser(
        "config",
        help="return the configuration for a history database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        help="the database code")
    parser.set_defaults(func="quantrocket.history._cli_get_db_config")

    examples = """
Delete a history database.

Deleting a history database deletes its configuration and data and is irreversible.

Examples:

Delete a database called "jpn-lrg-15m":

    quantrocket history drop-db 'jpn-lrg-15m' --confirm-by-typing-db-code-again 'jpn-lrg-15m'

    """
    parser = _subparsers.add_parser(
        "drop-db",
        help="delete a history database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "code",
        help="the database code")
    parser.add_argument(
        "--confirm-by-typing-db-code-again",
        metavar="CODE",
        required=True,
        help="enter the db code again to confirm you want to drop the database, its config, "
        "and all its data")
    parser.set_defaults(func="quantrocket.history._cli_drop_db")

    examples = """
Collect historical market data from IB and save it to a history database.

[DEPRECATED] `fetch` is deprecated and will be removed in a future release,
please use `collect` instead.
    """
    parser = _subparsers.add_parser(
        "fetch",
        help="[DEPRECATED] collect historical market data from IB and save it to a history database",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "codes",
        metavar="CODE",
        nargs="+",
        help="the database code(s) to collect data for")
    parser.add_argument(
        "-p", "--priority",
        action="store_true",
        help="use the priority queue (default is to use the standard queue)")
    parser.add_argument(
        "-i", "--conids",
        nargs="*",
        metavar="CONID",
        help="collect history for these conids, overriding config "
        "(typically used to collect a subset of securities)")
    parser.add_argument(
        "-u", "--universes",
        nargs="*",
        metavar="UNIVERSE",
        help="collect history for these universes, overriding config "
        "(typically used to collect a subset of securities)")
    parser.add_argument(
        "-s", "--start-date",
        metavar="YYYY-MM-DD",
        help="collect history back to this start date, overriding config")
    parser.add_argument(
        "-e", "--end-date",
        metavar="YYYY-MM-DD",
        help="collect history up to this end date, overriding config")
    parser.add_argument(
        "-a", "--availability",
        action="store_true",
        dest="availability_only",
        help="determine and store how far back data is available but "
        "don't yet collect the data")
    parser.add_argument(
        "--delist-missing",
        action="store_true",
        default=False,
        help="auto-delist securities that are no longer available from IB")
    parser.set_defaults(func="quantrocket.history._cli_fetch_history")
