#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The nsh-item Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
redis util

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/2/14
"""
import redis


class Redis(object):
    """
    redis class
    """

    def __init__(self, host, port, password, db=0):
        self.instance = redis.StrictRedis(host, port, db, password, socket_timeout=5)

    def ping(self):
        return self.instance.ping()

    def set(self, name, value, ex=None):
        return self.instance.set(name, value, ex)

    def get(self, name):
        return self.instance.get(name)

    def lrange(self, name, start, end):
        return self.instance.lrange(name, start, end)

    def producer(self, name, *values):
        return self.instance.rpush(name, *values)

    def consumer(self, name):
        return self.instance.lpop(name)

    def lpush(self, name, *values):
        return self.instance.lpush(name, *values)

    def queue_len(self, name):
        return self.instance.llen(name)

    def dbsize(self):
        return self.instance.dbsize()

    def setnx(self, name, value):
        return self.instance.setnx(name, value)

    def expire(self, name, ttl):
        return self.instance.expire(name, ttl)

    def pipeline(self):
        return self.instance.pipeline()


if __name__ == "__main__":
    re = Redis()
    re.ping()
