# -*- coding: utf-8 -*-
"""
CRUD operation for solar model
"""
from DB.api import database
from DB import exception
from DB.models import Solar
from DB.api import dbutils as utils

RESP_FIELDS = ['id', 'resource', 'status', 'tiltpercentage', 'lcd_first', 'lcd_second', 'created_at']
SRC_EXISTED_FIELD = {'id': 'id',
                     # 'uuid': 'uuid',
                     'status': 'status',
                     'tiltpercentage': 'tiltpercentage',
                     'lcd_first': 'lcd_first',
                     'lcd_second': 'lcd_second',
                     'resource_id': 'resource_id',
                     'created_at': 'created_at'
                     }


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)
def new(session, src_dic, content={}):
    for k, v in SRC_EXISTED_FIELD.items():
        content[k] = src_dic.get(v, None)
    return utils.add_db_object(session, Solar, **content)


def _get_solar(session, resource_id, order_by=[], limit=None, **kwargs):
    if isinstance(resource_id, int):
        resource_ids = {'eq': resource_id}
    elif isinstance(resource_id, list):
        resource_ids = {'in': resource_id}
    else:
        raise exception.InvalidParameter('parameter uuid format are not supported.')
    return \
        utils.list_db_objects(session, Solar, order_by=order_by, limit=limit, resource_id=resource_ids, **kwargs)


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)  # wrap the raw DB object into dict
def get_solar_by_gateway_uuid(session, resource_id):
    return _get_solar(session, resource_id)


# get the latest status if exists
@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)      # wrap the raw DB object into dict
def get_latest_by_gateway_uuid(session, resource_id, ):
    solar = _get_solar(session, resource_id, order_by=[('id', True)], limit=1)
    return solar[0] if len(solar) else None


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)  # wrap the raw DB object into dict
def get_solar_by_time(session, start_time, end_time):
    return utils.list_db_objects(session, Solar, created_at={'ge': str(start_time), 'le': str(end_time)})
