from .searchOnlineTool import fetch_web_page, search_duckduckgo
from .getStopsTool import get_all_stop_times

FUNCTION_MAPPING = {
    "fetch_web_page": fetch_web_page,
    "search_duckduckgo": search_duckduckgo,
    "get_all_stop_times": get_all_stop_times
}

