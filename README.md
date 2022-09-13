## Sayari Data Task Submission.
Assumptions:

Some trademarks have two owners, I only kept the first.

I treat owners and registered agents as the same. 
I will be matching these to companies.

_Requests_ was used for the inital request. 
Since it is a single request, _requests_ is a less verbose choice.
_Aiohttp_ was used to grab the business detail information.
This information is stored in a "drawer" element for each company.
Requiring a request for each company.
Using _aiohttp_ brought the time down to ~25s from ~2m40s
