# -*- coding: utf-8 -*-
"""
    tools
    Implements tools base.
    :copyright: 2019 Kalaiya86
    :license: MIT License
"""
from flask import jsonify
from howfo.logger import logger as log


def common_resp(data):
    """
        统一返回数据处理

        :param:
            * data(string): 数据

        :return:
            * result(dict): 返回字典

    """
    log.info('return_format_data return info is {}'.format(str(format_data)))
    if not format_data:
        return_dict = {'return_code': 90000, 'data': '', 'message': ''}
        return_status = 200
    else:
        return_code, return_data, return_message, return_status = 90000, {}, '', 200
        if 'code' in format_data and format_data.get('code'):
            return_code = format_data['code']
        if 'data' in format_data and format_data.get('data'):
            return_data = format_data['data']
        if 'message' in format_data and format_data.get('message'):
            return_message = format_data['message']
        if 'status' in format_data and format_data.get('status'):
            return_status = format_data['status']
        return_dict = {'return_code': return_code, 'data': return_data, 'message': return_message}
    return jsonify(return_dict), return_status
