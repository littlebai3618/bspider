# @Time    : 2019/11/19 2:58 下午
# @Author  : baii
# @File    : rabbitmq
# @Use     :
from bspider.core.api import BaseService, RabbitMQMixIn, GetSuccess


class RabbitMQService(BaseService, RabbitMQMixIn):

    def get_project_queue_info(self, project_id: int):
        queue_infos = self.op_get_project_queue_detail(project_id)
        result = dict()
        for queue_info in queue_infos:
            result[queue_info['name'].replace(f'_{project_id}', '')] = {
                'total': [queue_info['messages'], queue_info['messages_details']['rate']],
                'unacknowledged': [queue_info['messages_unacknowledged'], queue_info['messages_unacknowledged']['rate']],
                'ready': [queue_info['messages_ready'], queue_info['messages_ready']['rate']],
            }
        return GetSuccess(msg='get queue info success', data=result)

