#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys

from htrc.torchlite.database import mongo_client
from htrc.torchlite.models.schemas import DashboardSummary


async def main(args):
    # ensure the DB is accessible
    await mongo_client.ping()

    with open(args.data_file, 'r') as f:
        data = json.load(f)

    for dashboard in data:
        ds = DashboardSummary(**dashboard)
        print(ds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", help="The data to seed")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args)))
