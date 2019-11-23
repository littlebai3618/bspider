# @Time    : 2019/11/22 7:06 下午
# @Author  : baii
# @File    : chart
# @Use     : 用于生成图表数据
from bspider.core.api import BaseService, GetSuccess
from .impl.chart_impl import ChartImpl


class ChartService(BaseService):

    def __init__(self):
        self.impl = ChartImpl()

    def parser_pv(self, project_id: int = None):
        p_total = list()
        p_error = list()
        legend = ['P.TOTAL', 'P.ERROR']

        parser_metadata = self.impl.get_project_parser_pv(project_id)

        x_axis = list()
        for metadata in parser_metadata:
            p_total.append(metadata['total'])
            p_error.append(metadata['exception'])
            x_axis.append(metadata['time'])

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': self.get_two_line_chart_series(p_error, p_total)
        })

    def downloader_pv(self, project_id: int = None):
        d_total = list()
        d_error = list()
        legend = ['D.TOTAL', 'D.ERROR']

        downloader_metadata = self.impl.get_project_downloader_pv(project_id)

        x_axis = list()
        for metadata in downloader_metadata:
            d_total.append(metadata['total'])
            d_error.append(metadata['exception'])
            x_axis.append(metadata['time'])

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': self.get_two_line_chart_series(d_error, d_total)
        })

    def get_two_line_chart_series(self, series_one, series_two):
        return [{
            'name': 'expected',
            'itemStyle': {
                'normal': {
                    'color': '#FF005A',
                    'lineStyle': {
                        'color': '#FF005A',
                        'width': 2
                    }
                }
            },
            'smooth': True,
            'type': 'line',
            'data': series_one,
            'animationDuration': 2800,
            'animationEasing': 'cubicInOut'
        },
        {
            'name': 'actual',
            'smooth': True,
            'type': 'line',
            'itemStyle': {
                'normal': {
                    'color': '#3888fa',
                    'lineStyle': {
                        'color': '#3888fa',
                        'width': 2
                    },
                    'areaStyle': {
                        'color': '#f3f8ff'
                    }
                }
            },
            'data': series_two,
            'animationDuration': 2800,
            'animationEasing': 'quadraticOut'
        }]
