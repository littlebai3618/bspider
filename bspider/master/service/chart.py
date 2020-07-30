from bspider.core.api import BaseService, GetSuccess
from .impl.chart_impl import ChartImpl


class ChartService(BaseService):

    def __init__(self):
        self.impl = ChartImpl()

    def parser_pv(self, project_id: int = None):
        p_total = list()
        p_error = list()
        legend = ['P.ERROR', 'P.TOTAL']

        parser_metadata = self.impl.get_project_parser_pv(project_id)

        x_axis = list()
        for metadata in parser_metadata:
            p_total.append(metadata['total'])
            p_error.append(metadata['exception'])
            x_axis.append(metadata['time'])

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': self.get_two_line_chart_series(legend, p_error, p_total)
        })

    def downloader_pv(self, project_id: int = None):
        d_total = list()
        d_error = list()
        legend = ['D.ERROR', 'D.TOTAL']

        downloader_metadata = self.impl.get_project_downloader_pv(project_id)

        x_axis = list()
        for metadata in downloader_metadata:
            d_total.append(metadata['total'])
            d_error.append(metadata['exception'])
            x_axis.append(metadata['time'])

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': self.get_two_line_chart_series(legend, d_error, d_total)
        })

    def get_two_line_chart_series(self, legend, error, total):
        return [{
            'name': legend[0],
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
            'data': error,
            'animationDuration': 2800,
            'animationEasing': 'cubicInOut'
        },
            {
                'name': legend[1],
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
                'data': total,
                'animationDuration': 2800,
                'animationEasing': 'quadraticOut'
            }]

    def get_three_line_chart_series(self, legend, cpu, memory, disk):
        return [
            {
                'name': legend[0],
                'itemStyle': {
                    'normal': {
                        'color': '#5793f3',
                        'lineStyle': {
                            'color': '#5793f3',
                            'width': 2
                        }
                    }
                },
                'smooth': True,
                'type': 'line',
                'data': cpu,
            },
            {
                'name': legend[1],
                'itemStyle': {
                    'normal': {
                        'color': '#d14a61',
                        'lineStyle': {
                            'color': '#d14a61',
                            'width': 2
                        }
                    }
                },
                'smooth': True,
                'type': 'line',
                'data': memory,
            },
            {
                'name': legend[2],
                'itemStyle': {
                    'normal': {
                        'color': '#FF005A',
                        'lineStyle': {
                            'color': '#675bba',
                            'width': 2
                        }
                    }
                },
                'smooth': True,
                'type': 'line',
                'data': disk,
            }
        ]

    def get_code_type_detail(self):
        infos = self.impl.get_code_type_detail()
        legend = list()
        for info in infos:
            legend.append(info['name'])

        return GetSuccess(data={
            'data': infos,
            'legend': legend
        })

    def node_pv(self, node_ip: str):
        cpu = list()
        memory = list()
        disk = list()
        legend = ['CPU', 'MEMORY', 'DISK']

        node_metadata = self.impl.get_node_pv(node_ip)

        x_axis = list()
        for metadata in node_metadata:
            cpu.append(metadata['cpu'])
            memory.append(metadata['memory'])
            disk.append(metadata['disk'])
            x_axis.append(metadata['time'])

        return GetSuccess(data={
            'xAxis': x_axis,
            'legend': legend,
            'series': self.get_three_line_chart_series(legend, cpu, memory, disk)
        })
