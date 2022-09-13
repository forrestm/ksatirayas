## Sayari Data Task Submission.
Assumptions:

Some trademarks have two owners, I only kept the first.

I will be matching  owners and registered agents to companies.

_Requests_ was used for the inital request. 
Since it is a single request, _requests_ is a less verbose choice.
_Aiohttp_ was used to grab the business detail information.
This information is stored in a "drawer" element for each company.
Requiring a request for each company.
Using _aiohttp_ brought the time down to ~25s from ~2m40s

You will need graphviz installed (`brew install graphviz`) for the networkx layout to work.