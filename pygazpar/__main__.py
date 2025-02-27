import argparse
import json
import traceback
import os
import logging
import asyncio
from pygazpar.enum import Frequency
from pygazpar.client import Client
from pygazpar.datasource import JsonWebDataSource, ExcelWebDataSource, TestDataSource, ExcelFileDataSource
from pygazpar.version import __version__  # noqa: F401

async def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        action="version",
                        version=f"PyGazpar {__version__}")
    parser.add_argument("-u", "--username",
                        required=True,
                        help="GRDF username (email)")
    parser.add_argument("-p", "--password",
                        required=True,
                        help="GRDF password")
    parser.add_argument("-c", "--pce",
                        required=True,
                        help="GRDF PCE identifier")
    parser.add_argument("-t", "--tmpdir",
                        required=False,
                        default="/tmp",
                        help="tmp directory (default is /tmp)")
    parser.add_argument("-ex", "--excelfile",
                        required=False,
                        help="Excel file path")
    parser.add_argument("-f", "--frequency",
                        required=False,
                        type=lambda frequency: Frequency[frequency], choices=list(Frequency),
                        default="DAILY",
                        help="Meter reading frequency (DAILY, WEEKLY, MONTHLY, YEARLY)")
    parser.add_argument("-d", "--lastNDays",
                        required=False,
                        type=int,
                        default=365,
                        help="Get only the last N days of records (default: 365 days)")
    parser.add_argument("--datasource",
                        required=False,
                        default="json",
                        help="Datasource: json | excel | excelweb | test")

    args = parser.parse_args()

    # We create the tmp directory if not already exists.
    if not os.path.exists(args.tmpdir):
        os.mkdir(args.tmpdir)

    # We remove the pygazpar log file.
    pygazparLogFile = f"{args.tmpdir}/pygazpar.log"
    if os.path.isfile(pygazparLogFile):
        os.remove(pygazparLogFile)

    # Setup logging.
    logging.basicConfig(filename=f"{pygazparLogFile}", level=logging.DEBUG, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    logging.info(f"PyGazpar {__version__}")
    logging.info(f"--tmpdir {args.tmpdir}")
    logging.info(f"--excelfile {args.excelfile}")
    logging.info(f"--frequency {args.frequency}")
    logging.info(f"--lastNDays {args.lastNDays}")
    logging.info(f"--datasource {bool(args.datasource)}")
    if args.datasource == "json":
        client = Client(JsonWebDataSource(args.username, args.password))
    elif args.datasource == "excelweb":
        client = Client(ExcelWebDataSource(args.username, args.password, args.tmpdir))
    elif args.datasource == "excel":
        client = Client(ExcelFileDataSource(args.excelfile))
    elif args.datasource == "test":
        client = Client(TestDataSource())
    else:
        raise Exception("Invalid datasource: (json | excel | excelweb | test) is expected")

    try:
        data = await client.load_since(args.pce, int(args.lastNDays), [args.frequency])
    except BaseException:
        print('An error occured while querying PyGazpar library : %s', traceback.format_exc())
        return 1

    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
