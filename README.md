# Territory control via nzz.ch map

*Note: If you plan on publishing graphics based upon this data or use it
commercially, be mindful of the fact that it would not exist without the hard
work of the folks from [liveuamap.com](https://liveuamap.com/). A subscription
helps keep this vital source about the war alive.*

### Scraping the data

Run `python scrape.py`. The data is updated automatically via GitHub actions
once a day from nzz.ch.

Article: [Interactive map: How the Ukraine war is developing, day by day](https://www.nzz.ch/english/ukraine-war-interactive-map-of-the-current-front-line-ld.1688087)

Endpoints: Served from `q-server.st-cdn.nzz.ch` as base API server.

- [Example `getAreas` request](https://q-server.st-cdn.nzz.ch/tools/custom_code/endpoints/2484ed2804c37655aa53312284ef8f7f/getAreas?appendItemToPayload=c43940da317fdc578cf589dd9357512c&toolRuntimeConfig=%7B%22fileRequestBaseUrl%22%3A%22https%3A%2F%2Fq-server.st-cdn.nzz.ch%2Ffile%22%7D&to=2023-03-08)
- [Example `getBattalions` request](https://q-server.st-cdn.nzz.ch/tools/custom_code/endpoints/2484ed2804c37655aa53312284ef8f7f/getBattalions?appendItemToPayload=c43940da317fdc578cf589dd9357512c&toolRuntimeConfig=%7B%22fileRequestBaseUrl%22%3A%22https%3A%2F%2Fq-server.st-cdn.nzz.ch%2Ffile%22%7D&from=2023-03-06&to=2023-03-08)
- [Example `getAnnotations` request](https://q-server.st-cdn.nzz.ch/tools/custom_code/endpoints/2484ed2804c37655aa53312284ef8f7f/getAnnotations?appendItemToPayload=c43940da317fdc578cf589dd9357512c&toolRuntimeConfig=%7B%22fileRequestBaseUrl%22%3A%22https%3A%2F%2Fq-server.st-cdn.nzz.ch%2Ffile%22%7D&from=2023-03-06&to=2023-03-08&language=en)

### Analysis

See the accompanying ipython jupyter notebook:
[nzz_territory.ipynb](nzz_territory.ipynb)

**Russian-occupied Ukrainian territory in km^2**
![total](nzz_area_total.png)

**Net territory control change in km²**
![net](nzz_area_net.png)

### Data sources

NZZ says this about themselves:

> For our map we use data from Liveuamap. This organization emerged in 2014 in
> Ukraine during the annexation of Crimea. Since then, the staff has dealt with
> various conflicts both in and outside Europe. The NZZ has also relied on its
> data for other conflicts.

NZZ also only periodically updates data and works in time frames, not daily
changes. See ["Limitations"](https://github.com/conflict-investigations/nzz-maps/issues/1).
