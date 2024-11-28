from app.tool.gtfs.data_loader import GTFS_data


def get_all_stop_times(stop_name):
    gtfs = GTFS_data()
    stop_times = gtfs.stop_times
    stops = gtfs.stops

    # Filter stops DataFrame to get stop IDs for the given stop name
    stop_ids = stops[stops['stop_name'] == stop_name]['stop_id'].tolist()

    # Filter stop_times DataFrame to get times for the stop IDs
    result = stop_times[stop_times['stop_id'].isin(stop_ids)]

    return result.to_json(orient='records')
    


# print(get_all_stop_times("max Metro Station 1"))