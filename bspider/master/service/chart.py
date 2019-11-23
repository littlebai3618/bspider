# @Time    : 2019/11/22 7:06 下午
# @Author  : baii
# @File    : chart
# @Use     : 用于生成图表数据
from bspider.core.api import BaseService, GetSuccess
from .impl.chart_impl import ChartImpl


class ChartService(BaseService):
    line_chart_series = {
        'name': None,
        'itemStyle': {
            'normal': {
                'color': None,
                'lineStyle': {
                    'color': None,
                    'width': 2
                }
            }
        },
        'smooth': True,
        'type': 'line',
        'data': None,
        'animationDuration': 2800,
        'animationEasing': None
    }

    def __init__(self):
        self.impl = ChartImpl()

    def parser_pv(self, project_id: int = None):
        p_total = list()
        p_error = list()
        base_config = [
            ('P.TOTAL', '#3888fa', p_total, 'quadraticOut'),
            ('P.ERROR', '#FF005A', p_error, 'cubicInOut')
        ]

        parser_metadata = self.impl.get_project_parser_pv(project_id)

        x_axis = list()
        for metadata in parser_metadata:
            p_total.append(metadata['total'])
            p_error.append(metadata['exception'])
            x_axis.append(metadata['time'])

        series = list()
        legend = list()

        for l, c, d, a in base_config:
            cur_series = self.line_chart_series.copy()
            cur_series['name'] = l
            cur_series['itemStyle']['normal']['color'] = c
            cur_series['itemStyle']['normal']['lineStyle']['color'] = c
            cur_series['data'] = d
            cur_series['animationEasing'] = a
            series.append(cur_series)
            legend.append(l)

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': series
        })

    def downloader_pv(self, project_id: int = None):
        d_total = list()
        d_error = list()
        base_config = [
            ('D.TOTAL', '#3888fa', d_total, 'quadraticOut'),
            ('D.ERROR', '#FF005A', d_error, 'cubicInOut')
        ]

        downloader_metadata = self.impl.get_project_downloader_pv(project_id)

        x_axis = list()
        for metadata in downloader_metadata:
            d_total.append(metadata['total'])
            d_error.append(metadata['exception'])
            x_axis.append(metadata['time'])

        series = list()
        legend = list()

        for l, c, d, a in base_config:
            cur_series = self.line_chart_series.copy()
            cur_series['name'] = l
            cur_series['itemStyle']['normal']['color'] = c
            cur_series['itemStyle']['normal']['lineStyle']['color'] = c
            cur_series['data'] = d
            cur_series['animationEasing'] = a
            series.append(cur_series)
            legend.append(l)

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': series
        })
