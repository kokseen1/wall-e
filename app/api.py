import os
import requests

URL_BASE = "https://www.carousell.sg/"
URL_SEARCH = URL_BASE + "api-service/filter/cf/4.0/search/"
LISTING_URL = "https://www.carousell.sg/p/{}"

SSL_VERIFY = not os.environ.get("NO_SSL_VERIFY", "False").lower() in ['true']

def api_search(query=None, count=None, sort=None, collection=None, min_price=None, max_price=None):
    """
    Make a search request to the API with query
    """
    if not query:
        return
    if not count:
        count = 20
    if not sort:
        sort = "3"

    # Initialize array of search filters
    filters = []

    price_filter = {
        "fieldName": "price",
        "rangedFloat": {},
    }

    collections_filter = {
        "fieldName": "collections",
        "idsOrKeywords": {"value": []},
    }

    # Handle price filter if required
    if min_price:
        price_filter["rangedFloat"]["start"] = {"value": min_price}
    if max_price:
        price_filter["rangedFloat"]["end"] = {"value": max_price}
    if price_filter.get("rangedFloat"):
        filters.append(price_filter)

    # Handle collection filter if required
    if collection:
        collection_list = collection.split(",")
        collections_filter["idsOrKeywords"]["value"] = collection_list
    if collections_filter["idsOrKeywords"].get("value"):
        filters.append(collections_filter)

    # Initialize request body
    request_body = {
        "bestMatchEnabled": "true",
        "canChangeKeyword": "false",
        "count": int(count),
        "countryCode": "SG",
        "countryId": "1880251",
        "filters": filters,
        "includeSuggestions": "false",
        "locale": "en",
        "prefill": {"prefill_sort_by": sort},
        "query": query,
        "sortParam": {"fieldName": sort},
    }

    # Send the api request
    resp = requests.post(
        URL_SEARCH,
        json=request_body,
        verify=SSL_VERIFY,
    )

    print(f"[API REQUEST] {request_body}")
    # print(f"[API RESPONSE] {resp.json()}")

    # For debugging
    # import json
    # with open('data.json', 'w') as f:
    #     json.dump(resp.json(), f)
    try:
        return resp.json()
    except Exception:
        return
    
