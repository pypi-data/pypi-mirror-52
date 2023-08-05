from lib.serp_api_client import *

class BingSearchResults(SerpApiClient):
    """BingSearchResults enables to search google and parse the result.
    ```python
    from lib.bing_search_results import BingSearchResults
    query = BingSearchResults({"q": "coffee", "location": "Austin,Texas"})
    data = query.get_json()
    ```

    doc: https://serpapi.com/bing-search-api
    """

    def __init__(self, params_dict):
        super().__init__(params_dict, BING_ENGINE)

