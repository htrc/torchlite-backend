#!/usr/bin/env python3
import argparse
import asyncio
import json
import logging
import sys

from htrc.torchlite.database import mongo_client
from htrc.torchlite.models.schemas import DashboardSummary

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed_dashboards")


async def main(args):
    # ensure the DB is accessible
    await mongo_client.ping()

    dashboards_col = mongo_client.db.get_collection("dashboards")

    with open(args.data_file, 'r') as f:
        data = json.load(f)

    dashboards = [DashboardSummary(**dashboard) for dashboard in data]

    delete_result = await dashboards_col.delete_many({"_id": {"$in": [d.id for d in dashboards]}})
    if delete_result.deleted_count > 0:
        log.info(f"Removed {delete_result.deleted_count} existing records")

    insert_result = await dashboards_col.insert_many([d.dict(by_alias=True, exclude_defaults=True) for d in dashboards])
    if len(insert_result.inserted_ids) > 0:
        log.info(f"Inserted {len(insert_result.inserted_ids)} records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", help="The data to seed")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args)))
