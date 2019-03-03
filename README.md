# zomato-top-ten
Gets top 10 restaurants for different collections such as pubs, microbreweries, trending, pizzas, breakfasts, luxury dining, desserts in a city using the Zomato API v2.1

## Installation

```bash
 pip3 install --extra-index-url https://testpypi.python.org/pypi zomato_top_ten==1.0.1
```

## Getting Started
### Written in Python 3.

### CLI Usage
```bash
zomato_top_ten <city_name> <collection_option>

only the following cities are supported as of now:
- Bangalore

only the following collection options are supported as of now:
 1. Bars/Pubs
 2. Microbreweries
 3. Trending restaurants
 4. Pizza restaurants
 5. Breakfasts
 6. Luxury Dining
 7. Desserts

Example:
zomato_top_ten Bangalore 2
+-----------------------------------------------------------------------------+--------+-------+
|                               Restaurant name                               | Rating | Votes |
+-----------------------------------------------------------------------------+--------+-------+
|                  Byg Brewski Brewing Company, Sarjapur Road                 |  4.9   | 16686 |
|                              Toit, Indiranagar                              |  4.7   | 15075 |
|                            Biergarten, Whitefield                           |  4.7   |  6995 |
|                   Vapour Brewpub and Diner, Sarjapur Road                   |  4.6   |  2811 |
|                          Communiti, Residency Road                          |  4.6   |  4003 |
| Brew and Barbeque - A Microbrewery Pub, Soul Space Arena Mall, Marathahalli |  4.6   |  5894 |
|                        Big Pitcher, Old Airport Road                        |  4.6   |  9240 |
|  The Terrace at Gilly's Redefined, Gilly's Redefined, Koramangala 4th Block |  4.5   |  917  |
|                            The Pallet, Whitefield                           |  4.5   |  2668 |
|                            Red Rhino, Whitefield                            |  4.5   |  1961 |
+-----------------------------------------------------------------------------+--------+-------+
```

### API (wrapper) Usage
#### To add zomato_top_ten to your application:
- Takes user key as input
- Returns an object of class zomato.
```bash
Example:
from zomato_top_ten import zomato
z = zomato(user_key)
```
#### Get city id
- Takes city name as input.
- Returns city id on success and -1 on failure.
```bash
city_id = z.get_city_id(city_name)
Example:
city_id = z.get_city_id("Bangalore")
```
#### Get collection id
- Takes city name and collection option as inputs.
- Returns collection id on success and -1 on failure.
```bash
Example:
collection_id = z.get_collection_id("Bangalore", 2)
```
#### Get top 10 list
- Takes city name and collection option as inputs.
- Displays top 10 list in a tabular format.
- Returns 0 on success and -1 on failure.
```bash
z.get_top_ten_list("Bangalore", 2)
```
