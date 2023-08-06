import requests
import json
import luminati

api = "https://api.qwant.com/api/search/web"


def search(q="Barbie easy bake oven buy San Francisco",
           count=10, offset=0,
           t="web", uiv=1,
           session=None, headers={},
           *args, **kwargs):
    # count=max(count,10) #qwant doesn't display more than 10 items
    if not session:
        session = requests
    if not headers:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                                 + '(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
    params = {"q": q, "count": count, "offset": offset, "t": t, "uiv": uiv}
    r = session.get(api, params=params, headers=headers)
    return r.json()


def items(q, count=10, offset=0, *args, **kwargs):
    if count <= 10:
        return search(q, count=count, offset=offset, *args, **kwargs)['data']['result']['items']
    else:
        return items(q, count=10, offset=offset, *args, **kwargs) + items(q, count=count - 10, offset=offset + 10,
                                                                          *args,
                                                                          **kwargs)


def prettyprint(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


if __name__ == "__main__":
    session = luminati.session("lum-customer-hl_7c6aa799-zone-zone1", "№№№№№")
    data = items("site:allegro.pl/oferta/ Lol doll", session=session, count=10)
    links = list(map(lambda item: item['url'], data))
    prettyprint(data)
    prettyprint(links)
