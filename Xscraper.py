import aiohttp
import asyncio
import requests
import pandas as pd

BIZ_JSON = {"SEARCH_VALUE": "X", "STARTS_WITH_YN": "false", "ACTIVE_ONLY_YN": "true"}

BIZ_SEARCH_URL = "https://firststop.sos.nd.gov/api/Records/businesssearch"

resp = requests.post(BIZ_SEARCH_URL, json=BIZ_JSON)
a = resp.json()

onlyX = {}
IDs = []

for biz_id in a["rows"]:
    if a["rows"][biz_id]["TITLE"][0][0] in ["x", "X"]:
        onlyX[str(biz_id)] = {"TITLE": a["rows"][biz_id]["TITLE"][0]}


async def getBizAgent(session, url):
    async with session.get(url) as resp:
        b = await resp.json()
        return b


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        try:
            for bizID in onlyX.keys():
                bizURL = f"https://firststop.sos.nd.gov/api/FilingDetail/business/{int(bizID)}/false"
                tasks.append(asyncio.ensure_future(getBizAgent(session, bizURL)))

            BizAgents = await asyncio.gather(*tasks)
            for agent in BizAgents:
                IDs.append(agent)

        except aiohttp.ClientConnectionError:
            # something went wrong with the exception, decide on what to do next
            print("Oops, the connection was dropped before we finished")
        except aiohttp.ClientError:
            # something went wrong in general. Not a connection error, that was handled
            # above.
            print("Oops, something else went wrong with the request")


asyncio.run(main())

for agentID, bizID in zip(IDs, onlyX.keys()):
    for item in agentID["DRAWER_DETAIL_LIST"]:
        if item["LABEL"] in [
            "Registered Agent",
            "Owner Name",
            "Commercial Registered Agent",
            "Owners",
        ]:
            onlyX[bizID]["AGENT"] = item["LABEL"]
            onlyX[bizID]["ID"] = item["VALUE"]

onlyXList = list(onlyX.values())
df = pd.DataFrame(onlyXList)
df.to_csv("businesses.csv")
