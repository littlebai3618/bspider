from bspider.core.api import BaseService, RabbitMQMixIn, GetSuccess, DeleteSuccess


class RabbitMQService(BaseService, RabbitMQMixIn):

    def get_project_queue_info(self, project_id: int):
        queue_infos = self.op_get_project_queue_detail(project_id)
        result = dict()
        for queue_info in queue_infos:
            result[queue_info['name'].replace(f'_{project_id}', '')] = {
                'total': [queue_info['messages'], queue_info['messages_details']['rate']],
                'unacknowledged': [queue_info['messages_unacknowledged'], queue_info['messages_unacknowledged_details']['rate']],
                'ready': [queue_info['messages_ready'], queue_info['messages_ready_details']['rate']],
            }
        return GetSuccess(msg='get queue info success', data=result)

    def purge_project_queue(self, project_id: int):
        self.op_purge_queue_msg(project_id)
        return DeleteSuccess()


