# from .searchOnlineTool import fetch_web_page, search_duckduckgo
# from .getStopsTool import get_all_stop_times
from .generateMidiTool import convert_text_to_midi

# TODO ADD TOOL LOAD CONTROL IN CONFIG FILE, AND MIGRATE TO HYDRA.

FUNCTION_MAPPING = {
    # "fetch_web_page": fetch_web_page,
    # "search_duckduckgo": search_duckduckgo,
    # "get_all_stop_times": get_all_stop_times,
    "convert_text_to_midi": convert_text_to_midi,
}

