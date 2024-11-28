import os
import pandas as pd

class GTFS_data:
    base_path = os.path.join(os.getcwd(), "storage/datasets/GTFS_File")
    _agency = None
    _calendar_dates = None
    _calendar = None
    _feed_info = None
    _routes = None
    _shapes = None
    _stop_times = None
    _stops = None
    _transfers = None
    _translations = None
    _trips = None

    @property
    def agency(self):
        if self._agency is None:
            self._agency = pd.read_csv(os.path.join(self.base_path, "agency.txt"))
        return self._agency

    @property
    def calendar_dates(self):
        if self._calendar_dates is None:
            self._calendar_dates = pd.read_csv(os.path.join(self.base_path, "calendar_dates.txt"))
        return self._calendar_dates

    @property
    def calendar(self):
        if self._calendar is None:
            self._calendar = pd.read_csv(os.path.join(self.base_path, "calendar.txt"))
        return self._calendar

    @property
    def feed_info(self):
        if self._feed_info is None:
            self._feed_info = pd.read_csv(os.path.join(self.base_path, "feed_info.txt"))
        return self._feed_info

    @property
    def routes(self):
        if self._routes is None:
            self._routes = pd.read_csv(os.path.join(self.base_path, "routes.txt"))
        return self._routes

    @property
    def shapes(self):
        if self._shapes is None:
            self._shapes = pd.read_csv(os.path.join(self.base_path, "shapes.txt"))
        return self._shapes

    @property
    def stop_times(self):
        if self._stop_times is None:
            self._stop_times = pd.read_csv(os.path.join(self.base_path, "stop_times.txt"))
        return self._stop_times

    @property
    def stops(self):
        if self._stops is None:
            self._stops = pd.read_csv(os.path.join(self.base_path, "stops.txt"))
        return self._stops

    @property
    def transfers(self):
        if self._transfers is None:
            self._transfers = pd.read_csv(os.path.join(self.base_path, "transfers.txt"))
        return self._transfers

    @property
    def translations(self):
        if self._translations is None:
            self._translations = pd.read_csv(os.path.join(self.base_path, "translations.txt"))
        return self._translations

    @property
    def trips(self):
        if self._trips is None:
            self._trips = pd.read_csv(os.path.join(self.base_path, "trips.txt"))
        return self._trips