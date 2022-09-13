import aiohttp
import asyncio
import requests
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import logging

## Uncomment for LaTeX printing
# plt.rcParams.update(
#     {
#         "text.usetex": True,
#         "font.family": "serif",
#     }
# )

BIZ_SEARCH_URL = "https://firststop.sos.nd.gov/api/Records/businesssearch"

BIZ_JSON = {"SEARCH_VALUE": "X", "STARTS_WITH_YN": "false", "ACTIVE_ONLY_YN": "true"}

resp = requests.post(BIZ_SEARCH_URL, json=BIZ_JSON)
response_json = resp.json()

onlyX = {}
IDs = []

for biz_id in response_json["rows"]:
    if response_json["rows"][biz_id]["TITLE"][0][0] in ["x", "X"]:
        onlyX[str(biz_id)] = {
            "TITLE": response_json["rows"][biz_id]["TITLE"][0].upper()
        }


async def getBizAgent(session, url):
    async with session.get(url) as resp:
        bizAgentResponse = await resp.json()
        return bizAgentResponse


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
            logging.exception("The connection was dropped before we finished")
        except aiohttp.ClientError:
            logging.exception("No connection error, something else went wrong.")


asyncio.run(main())

for agentID, bizID in zip(IDs, onlyX.keys()):
    for item in agentID["DRAWER_DETAIL_LIST"]:
        if item["LABEL"] in [
            "Registered Agent",
            "Owner Name",
            "Commercial Registered Agent",
            "Owners",
        ]:
            onlyX[bizID]["AGENT"] = item["LABEL"].upper()
            onlyX[bizID]["ID"] = item["VALUE"].upper()

onlyXList = list(onlyX.values())
df = pd.DataFrame(onlyXList)
# df.to_csv("businesses.csv")
# df = pd.read_csv("businesses.csv", index_col=0)

plt.figure(figsize=(12, 12))

g = nx.from_pandas_edgelist(df, source="ID", target="TITLE")
nx.draw_networkx(g, pos=graphviz_layout(g), node_size=50, with_labels=False)

plt.title(r"North Dakota ``X'' Businesses", fontsize=30)
# plt.show()
plt.savefig("businesses.pdf")
