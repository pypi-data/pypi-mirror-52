import datetime


class BaseMoudel():
    '''
    服务以及业务的模型基类

    '''

    def __init__(self):
        self.response_data = {'code': '8999', 'data_type': '2', 'response_data': '', 'msg': '', 'timestamp': ''}

    def build_return_response_data(self, code, msg=None, response_data=None, data_type=None, timestamp_now=False):
        '''
        构造返回信息

        :param code:
        :param msg:
        :return:
        '''
        self.response_data['code'] = code
        if msg:
            self.response_data['msg'] = msg
        if response_data:
            self.response_data['response_data'] = response_data
        if data_type:
            self.response_data['data_type'] = data_type
        if timestamp_now:
            self.response_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.response_data

    def build_success_response_data(self, response_data=None, timestamp_now=False):
        '''
        构建业务成功的返回数据

        :param response_data:
        :return:
        '''

        return self.build_return_response_data('1000', data_type='1', response_data=response_data,
                                               timestamp_now=timestamp_now)

    def build_error_response_data(self, code='1000', msg=None, timestamp_now=False):
        '''
        构建业务失败的返回数据

        :param msg:
        :return:
        '''

        return self.build_return_response_data(code, data_type='2', msg=msg, timestamp_now=timestamp_now)
