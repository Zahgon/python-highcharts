# -*- coding: UTF-8 -*-
from past.builtins import basestring
import json, datetime
from .common import Formatter, Events, Position, ContextButton, Options3d, ResetZoomButton, DrillUpButton, Labels, \
    Marker, Point, States, Tooltip, Title, JSfunction, MapObject, ColorObject, CSSObject, SVGObject, \
    CommonObject, ArrayObject

PLOT_OPTION_ALLOWED_ARGS = {
  "common": {
    "animation": bool,
    "color": (ColorObject, basestring, dict),
    "cursor": basestring,
    "dataLabels": (Labels, dict),
    "enableMouseTracking": bool,
    "events": (Events, dict),
    "id": basestring,
    "index": [float, int],
    "marker": (Marker, dict),
    "name": basestring,
    "point": (Point, dict),
    "selected": bool,
    "showCheckbox": bool,
    "showInLegend": bool,
    "states": (States, dict),
    "stickyTracking": bool,
    "tooltip": (Tooltip, dict),
    "visible": bool,
    "xAxis": [int, basestring],
    "yAxis": [int, basestring],
    "zIndex": int,
    },  "heatmap": {
    "allowPointSelect": bool,
    "borderColor": (ColorObject, basestring, dict),
    "borderWidth": [int, float, basestring],
    "colsize": int,
    "legendIndex": [int, float],
    "rowsize": int,
    "mapData": (MapObject, list, basestring),
    "nullColor": (ColorObject, basestring, dict),
    "shadow": [bool, dict], #shadow object
  },
  "map": {
    "allAreas": bool,
    "allowPointSelect": bool,
    "borderColor": (ColorObject, basestring, dict),
    "borderWidth": [int, float, basestring],
    "dashStyle": basestring,  
    "joinBy": [basestring, list],
    "legendIndex": [int, float],
    "mapData": (MapObject, list, basestring),
    "nullColor": (ColorObject, basestring, dict),
    "shadow": [bool, dict],
  },
  "mapbubble": {
    "allAreas": bool,
    "allowPointSelect": bool,
    "borderColor": (ColorObject, basestring, dict),
    "borderWidth": [int, float, basestring],
    "displayNegative": bool, 
    "joinBy": [basestring, list],
    "legendIndex": [int, float],
    "mapData": (MapObject, list, basestring),
    "maxSize": [basestring, int],
    "minSize": [basestring, int],
    "negativeColor": (ColorObject, basestring, dict),
    "shadow": [bool, dict],
    "sizeBy": basestring,
    "zMax": int,
    "zMin": int,
    "zThreshold": [int, float],
  },
  "mapline": {
    "allAreas": bool,
    "allowPointSelect": bool,
    "dashStyle": basestring,
    "fillColor": (ColorObject, basestring, dict),
    "joinBy": [basestring, list],
    "legendIndex": [int, float],
    "lineWidth": [int, float],
    "mapData": (MapObject, list, basestring),
    "maxSize": [basestring, int],
    "minSize": [basestring, int],
    "negativeColor": (ColorObject, basestring, dict),
    "shadow": [bool, dict],
    "sizeBy": basestring,
    "zMax": int,
    "zMin": int,
    "zThreshold": [int, float],
  },
  "mappoint": {
    "legendIndex": [int, float],
    "mapData": (MapObject, list, basestring),
  },
}

DATA_SERIES_ALLOWED_OPTIONS = {
    "color": (ColorObject, basestring, dict),
    "dataLabels": (Labels, dict),
    "dataParser": NotImplemented,
    "dataURL": NotImplemented,
    "drilldown": basestring,
    "events": (Events, dict),
    "high": [int, float],
    "id": basestring,
    "index": int,
    "legendIndex": int,
    "lat": [float, int],
    "lon": [float, int],
    "labelrank": [int, float],
    "middleX": [int, float],
    "middleY": [int, float],
    "name": basestring,
    "path": basestring,
    "value": [int, float, list],
    "x": [int, float],
    "y": [int, float],
    "z": [float, int],
    "xAxis": int,
    "yAxis": int,
}

DEFAULT_OPTIONS = {

}

class OptionTypeError(Exception):

    def __init__(self, *args):
        self.args = args


class SeriesOptions(object):
    """Class for plotOptions"""

    def __init__(self, series_type="map", supress_errors=False, **kwargs):
        self.load_defaults(series_type)
        self.process_kwargs(kwargs, series_type=series_type, supress_errors=supress_errors)

    @staticmethod
    def __validate_options__(k, v, ov):
        if isinstance(ov,list):
            if isinstance(v,tuple(ov)): return True
            else:
                raise OptionTypeError("Option Type Currently Not Supported: %s" % k)
        else:
          if ov == NotImplemented: raise OptionTypeError("Option Type Currently Not Supported: %s" % k)
          if isinstance(v,ov): return True
          else: return False

    def __options__(self):
        return self.__dict__

    def __jsonable__(self):
        return self.__dict__

    def __display_options__(self):
        print(json.dumps(self.__options__(),indent=4,sort_keys=True))

    def update(self,series_type, **kwargs):
        pass
                

    def process_kwargs(self, kwargs, series_type, supress_errors=False):
        pass

    def load_defaults(self, series_type):
        pass

    def __getattr__(self, item):
        if not item in self.__dict__:
            return None # Attribute Not Set
        else:
            return True


class Series(object):
    """Series class for input data """

    def __init__(self, data, series_type="line", supress_errors=False, **kwargs):

        # List of dictionaries. Each dict contains data and properties, 
        # which need to handle before construct the object for series 
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if k in DATA_SERIES_ALLOWED_OPTIONS:
                            if SeriesOptions.__validate_options__(k,v,DATA_SERIES_ALLOWED_OPTIONS[k]):
                                if isinstance(DATA_SERIES_ALLOWED_OPTIONS[k], tuple):
                                    if isinstance(v, dict):
                                        item.update({k:DATA_SERIES_ALLOWED_OPTIONS[k][0](**v)})
                                    elif isinstance(v, datetime.datetime):
                                        item.update({k:v})                            
                                    else:
                                        item.update({k:DATA_SERIES_ALLOWED_OPTIONS[k][0](v)})
                                else:
                                    item.update({k:v})
                        
        self.__dict__.update({
          "data": data,
          "type": series_type,
          })

        # Series propertie can be input as kwargs, which is handled here 
        for k, v in kwargs.items():
            if k in DATA_SERIES_ALLOWED_OPTIONS:
                if SeriesOptions.__validate_options__(k,v,DATA_SERIES_ALLOWED_OPTIONS[k]):
                    if isinstance(DATA_SERIES_ALLOWED_OPTIONS[k], tuple):
                        if isinstance(v, dict):
                            self.__dict__.update({k:DATA_SERIES_ALLOWED_OPTIONS[k][0](**v)})
                        elif isinstance(v, datetime.datetime):
                            self.__dict__.update({k:v})                            
                        else:
                            self.__dict__.update({k:DATA_SERIES_ALLOWED_OPTIONS[k][0](v)})
                    else:
                        self.__dict__.update({k:v})
                else: 
                    if not supress_errors: raise OptionTypeError("Option Type Mismatch: Expected: %s" % DATA_SERIES_ALLOWED_OPTIONS[k])
            
    def __jsonable__(self):
        return self.__dict__

    def __options__(self):
        return self.__dict__
