# -*- coding: utf-8 -*-

import re
import urllib
from parser import parse_string


class GoogleChartError(Exception):
    pass


class GoogleChart(object):
    baseurl = 'https://chart.googleapis.com/chart?'

    def __init__(self, code, format, **options):
        self.code = code
        self.format = format
        self.options = options

    @property
    def url(self):
        if self.format == 'chart':
            params = self._url_for_chart()
        elif self.format == 'graphviz':
            params = self._url_for_graphviz()
        else:
            msg = "unknown format: %s" % self.format
            raise GoogleChartError(msg)

        quoted = ("%s=%s" % (k, urllib.quote(v)) for k, v in params.items())
        url = self.baseurl + "&".join(quoted)

        return url

    def _url_for_chart(self):
        chart = parse_string(self.code)
        if chart.type in ('p', 'p3'):
            params = self._url_for_piechart(chart)
        elif chart.type in ('lc',):
            params = self._url_for_linechart(chart)
        elif chart.type in ('lxy',):
            params = self._url_for_linechart_xy(chart)
        elif chart.type in ('bhs', 'bvs', 'bhg', 'bvg'):
            params = self._url_for_barchart(chart)
        elif chart.type in ('v'):
            params = self._url_for_venndiagram(chart)
        elif chart.type in ('s'):
            params = self._url_for_spotchart(chart)
        else:
            params = {}

        params['cht'] = chart.type
        params['chs'] = self.options.get('size', '320x240')

        return params

    def _url_for_piechart(self, chart):
        data = "t:" + ",".join(zip(*chart.items)[0])
        colors = ",".join(chart.colors)
        labels = "|".join(chart.labels)

        return dict(chd=data, chl=labels, chco=colors)

    def _url_for_linechart(self, chart):
        series = (",".join(n) for n in chart.items)
        data = "t:" + "|".join(series)
        colors = ",".join(chart.colors)
        labels = "|".join(chart.labels)

        axes = ",".join(n[0] for n in chart.axes)
        _labels = ([str(i) + ":"] + n for i, n in chart.axis_labels.items())
        axis_labels = "|".join("|".join(n) for n in _labels)

        params = dict(chd=data, chdl=labels, chco=colors)
        if chart.axes:
            params['chxt'] = axes
            params['chxl'] = axis_labels

        return params

    def _url_for_linechart_xy(self, chart):
        series = []
        [series.extend(m) for m in (zip(*n) for n in chart.items)]
        data = "t:" + "|".join(",".join(n) for n in series)
        colors = ",".join(chart.colors)
        labels = "|".join(chart.labels)

        axes = []
        if chart.axes:
            axes = ",".join(chart.axes[0])

        _labels = []
        if chart.axis_labels:
            _labels = chart.axis_labels[0]

        if _labels and isinstance(_labels[0], tuple):
            _labels = ([str(i) + ":"] + list(n) for i, n in enumerate(_labels))
        axis_labels = "|".join("|".join(n) for n in _labels)

        params = dict(chd=data, chdl=labels, chco=colors)
        if chart.axes:
            params['chxt'] = axes
            params['chxl'] = axis_labels

        return params

    def _url_for_barchart(self, chart):
        data = "t:" + "|".join(",".join(n) for n in chart.items)
        colors = ",".join(chart.colors)
        labels = "|".join(chart.labels)

        axes = ",".join(n[0] for n in chart.axes)
        _labels = ([str(i) + ":"] + n for i, n in chart.axis_labels.items())
        axis_labels = "|".join("|".join(n) for n in _labels)

        params = dict(chd=data, chdl=labels, chco=colors)
        if chart.axes:
            params['chxt'] = axes
            params['chxl'] = axis_labels

        return params

    def _url_for_venndiagram(self, chart):
        data = "t:" + ",".join(chart.items.next())

        return dict(chd=data)

    def _url_for_venndiagram(self, chart):
        data = "t:" + ",".join(chart.items.next())

        return dict(chd=data)

    def _url_for_spotchart(self, chart):
        data = "t:" + "|".join(",".join(n) for n in zip(*chart.items.next()))

        axes = []
        if chart.axes:
            axes = ",".join(chart.axes[0])

        _labels = []
        if chart.axis_labels:
            _labels = chart.axis_labels[0]

        if _labels and isinstance(_labels[0], tuple):
            _labels = ([str(i) + ":"] + list(n) for i, n in enumerate(_labels))
        axis_labels = "|".join("|".join(n) for n in _labels)

        params = dict(chd=data)
        if chart.axes:
            params['chxt'] = axes
            params['chxl'] = axis_labels

        return params

    def _url_for_graphviz(self):
        _type = self.options.get('type', 'dot')
        striped = re.sub('\\s+', ' ', self.code)

        params = dict(cht="gv:%s" % _type, chl=striped)

        if self.options.get('size'):
            params['chs'] = self.options.get('size')

        return params

    def save(self, filename):
        fd = urllib.urlopen(self.url)

        if fd.getcode() == 200:
            open(filename, 'w').write(fd.read())
        else:
            msg = "google chart error: a malformed or illegal request"
            raise GoogleChartError(msg)
