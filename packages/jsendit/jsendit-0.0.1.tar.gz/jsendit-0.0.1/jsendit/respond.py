#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 9/18/19 by Pat Blair
"""
.. currentmodule:: respond
.. moduleauthor:: Pat Blair <pblair@geo-comm.com>

This module contains helper functions that help you model your API responses
consistently using the `JSend <https://labs.omniti.com/labs/jsend>`_
specification.
"""
from enum import Enum
from typing import Dict


class JSendStatus(Enum):
    """
    :cvar SUCCESS: All went well and (usually) some data is returned (200).
    :cvar FAIL: There was a problem with the data submitted or some
        pre-condition of the API wasn't satisfied (400).
    :cvar ERROR: An error occurred in processing the request (500).
    """
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'

    @staticmethod
    def http_code(status: 'JSendStatus') -> int:
        """
        Get the default `HTTP code <https://restfulapi.net/http-status-codes/>`_
        that corresponds to a `JSendStatus`.

        :param status: the status
        :return: the HTTP code
        """
        return {
            JSendStatus.SUCCESS: 200,
            JSendStatus.FAIL: 400,
            JSendStatus.ERROR: 500
        }.get(status)


def response(
        status: JSendStatus or int,
        message: str = None,
        data: Dict = None):
    """
    Construct a `JSend <https://labs.omniti.com/labs/jsend>`_ response message.

    :param status: the general status or
        `HTTP code <https://www.restapitutorial.com/httpstatuscodes.html>`_
    :param message: the response message
    :param data: additional response data
    :return: the response message
    """
    _code = (
        JSendStatus.http_code(status)
        if isinstance(status, JSendStatus)
        else int(status)
    )
    return {
        k: v for k, v in {
            'message': message,
            **(data if data is not None else {})
        }.items() if v
    }, _code
