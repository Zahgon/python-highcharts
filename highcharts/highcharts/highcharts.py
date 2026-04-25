# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
from future.standard_library import install_aliases
install_aliases()
from past.builtins import basestring

from jinja2 import Environment, PackageLoader

import json, uuid
import re
import datetime
import urllib.request, urllib.error, urllib.parse
import html
from collections import Iterable
from .options import BaseOptions, ChartOptions, ColorAxisOptions, \
    ColorsOptions, CreditsOptions, DrilldownOptions, ExportingOptions, \
    GlobalOptions, LabelsOptions, LangOptions, \
    LegendOptions, LoadingOptions, NavigationOptions, PaneOptions, \
    PlotOptions, SeriesData, SubtitleOptions, TitleOptions, \
    TooltipOptions, xAxisOptions, yAxisOptions, zAxisOptions, MultiAxis

from .highchart_types import Series, SeriesOptions
from .common import Levels, Formatter, CSSObject, SVGObject, JSfunction, RawJavaScriptText, \
    CommonObject, ArrayObject, ColorObject

CONTENT_FILENAME = "content.html"
PAGE_FILENAME = "page.html"

pl = PackageLoader('highcharts.highcharts', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

template_content = jinja2_env.get_template(CONTENT_FILENAME)
template_page = jinja2_env.get_template(PAGE_FILENAME)
    

class Highchart(object):
    """
    Highcharts Base class.
    """
    #: chart count
    count = 0

    # this attribute is overriden by children of this
    # class
    CHART_FILENAME = None
    template_environment = Environment(lstrip_blocks=True, trim_blocks=True,
                                       loader=pl)

    def __init__(self, **kwargs):
        """
        This is the base class for all the charts. The following keywords are
        accepted:
        :keyword: **display_container** - default: ``True``
                  **offline - default: ``False``
                            If True, download all .js and .css file and put them
                            into the generated .html so it can be viewed offline.
        """
        # set the model
        self.model = self.__class__.__name__  #: The chart model,
        self.div_name = kwargs.get("renderTo", "container")

        # an Instance of Jinja2 template
        self.template_page_highcharts = template_page
        self.template_content_highcharts = template_content

        
        # set Javascript src, Highcharts lib needs to make sure it's up to date
        self.JSsource = [
                'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                'https://code.highcharts.com/6/highcharts.js',
                'https://code.highcharts.com/6/highcharts-more.js',
                'https://code.highcharts.com/6/modules/heatmap.js',
                'https://code.highcharts.com/6/modules/exporting.js'
            ]

        # set CSS src
        self.CSSsource = [
                'https://www.highcharts.com/highslide/highslide.css',

            ]

        self.offline = kwargs.get("offline", False)

        # set data
        self.data = []
        self.data_temp = []
        # Data from jsonp
        self.jsonp_data_flag = False
        self.jsonp_data_url_list = [] # DEM 2017/07/27: List of JSON data sources

        # set drilldown data
        self.drilldown_data = []
        self.drilldown_data_temp = []

        # javascript
        self.jscript_head_flag = False
        self.jscript_head = kwargs.get('jscript_head', None)
        self.jscript_end_flag = False
        self.jscript_end = kwargs.get('jscript_end', None)

        # accepted keywords
        self.div_style = kwargs.get('style', '')
        self.drilldown_flag = kwargs.get('drilldown_flag', False)

        # None keywords attribute that should be modified by methods
        # We should change all these to _attr

        self._htmlcontent = ''  #: written by buildhtml
        self.htmlheader = ''
        #: Place holder for the graph (the HTML div)
        #: Written by ``buildcontainer``
        self.container = u''
        #: Header for javascript code
        self.containerheader = u''
        # Loading message
        self.loading = 'Loading....'

        # Bind Base Classes to self
        self.options = {
            "chart": ChartOptions(),
            #"colorAxis" : ColorAxisOptions(),
            "colors": ColorsOptions(),
            "credits": CreditsOptions(),
            #"data": #NotImplemented
            "drilldown": DrilldownOptions(),
            "exporting": ExportingOptions(),
            "labels": LabelsOptions(),
            "legend": LegendOptions(),
            "loading": LoadingOptions(),
            "navigation": NavigationOptions(),
            "pane": PaneOptions(),
            "plotOptions": PlotOptions(),
            "series": SeriesData(),
            "subtitle": SubtitleOptions(),
            "title": TitleOptions(),
            "tooltip": TooltipOptions(),
            "xAxis": xAxisOptions(),
            "yAxis": yAxisOptions(),   
        }

        self.setOptions = {
            "global": GlobalOptions(),
            "lang": LangOptions(),
        }

        self.__load_defaults__()

        # Process kwargs
        allowed_kwargs = [
            "width",
            "height",
            "renderTo",
            "backgroundColor",
            "events",
            "marginBottom",
            "marginTop",
            "marginRight",
            "marginLeft"
        ]

        for keyword in allowed_kwargs:
            if keyword in kwargs:
                self.options['chart'].update_dict(**{keyword:kwargs[keyword]})
        # Some Extra Vals to store:
        self.data_set_count = 0
        self.drilldown_data_set_count = 0


    def __load_defaults__(self):
        self.options["chart"].update_dict(renderTo='container')
        self.options["title"].update_dict(text='A New Highchart')
        self.options["credits"].update_dict(enabled=False)


    def add_JSsource(self, new_src):
        """add additional js script source(s)"""
        pass


    def add_CSSsource(self, new_src):
        """add additional css source(s)"""
        pass


    def add_3d_rotation(self):
        pass

    def add_data_set(self, data, series_type="line", name=None, **kwargs):
        """set data for series option in highcharts"""
        pass


    def add_drilldown_data_set(self, data, series_type, id, **kwargs):
        """set data for drilldown option in highcharts"""
        pass


    def add_data_from_jsonp(self, data_src, data_name='json_data', series_type="line", name=None, **kwargs):
        """set map data directly from a https source
        the data_src is the https link for data
        and it must be in jsonp format
        """
        pass


    def add_JSscript(self, js_script, js_loc):
        """add (highcharts) javascript in the beginning or at the end of script
        use only if necessary
        """
        pass


    def set_options(self, option_type, option_dict, force_options=False):
        """set plot options """
        pass


    def set_dict_options(self, options):
        """for dictionary-like inputs (as object in Javascript)
        options must be in python dictionary format
        """
        pass


    def buildcontent(self):
        """build HTML content only, no header or body tags"""
        pass


    def buildhtml(self):
        """build the HTML page
        create the htmlheader with css / js
        create html page
        """
        pass
        

    def buildhtmlheader(self):
        """generate HTML header content"""
        pass


    def buildcontainer(self):
        """generate HTML div"""
        pass

    @property
    def htmlcontent(self):
        pass

    @property
    def iframe(self):
        pass
    

    def __str__(self):
        """return htmlcontent"""
        #self.buildhtml()
        return self.htmlcontent

    def save_file(self, filename = 'Chart'):
        """ save htmlcontent as .html file """
        pass

class HighchartsEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)
        self._replacement_map = {}

    def default(self, obj):
        pass

    def encode(self, obj):
        pass


class OptionTypeError(Exception):

    def __init__(self,*args):
        self.args = args
