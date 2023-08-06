```
#My qwant toolbox

Qwant is search context-independet and non-spying engine
* Better for e-commerce search than Google
* Free. Using on industrial scale
requires proxy that is way cheeper than google
* Available for multithreading
* Context-independet, that means a consistent output for you queries

import qwant

qwant.search("Barbie doll") 

#get only items of search. 10 by default
qwant.items("Barbie doll")

#but you can get more. It's done with multiple requests
qwant.items("Barbie doll",count=100)

#you can set web site of search
qwant.items("site:allegro.pl/oferta/ Barbie doll")

#add your proxy
session={<define your session here>}
qwant.items("site:allegro.pl/oferta/ Barbie doll",session=session)

#you can use luminati so EVERY request would be done from different IP
import luminati
session = luminati.session("<login>", "<password>")
qwant.items("site:allegro.pl/oferta/ Illuminati doll",session=session)
```
