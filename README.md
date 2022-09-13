## This is my submission for the Sayari Data Task.
Assumptions:

Some trademarks have two owners, I only kept the first.

I treat owners and registered agents as the same. 
I will be matching these to companies.

Requests was used for the inital request. 
Since it is a single request requests is a less verbose choice.
Aiohttp was used to grab the business detail information.
This information is stored in a "drawer" element for each company.
Requiring a request for each company.
Using aiohttp brought the time down to ~25s from ~2m40s
