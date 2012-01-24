#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by Dustin Keitel on 2012-01-24.
Copyright (c) 2012 ShopWiki. All rights reserved.
"""

def lazyproperty(fun):
    class Descriptor(property):
        def __get__(self, instance, owner):
            key = '%s_value' % fun.__name__
            if hasattr(instance, key):
                return getattr(instance,key)
            v = fun(instance)
            setattr(instance, key, v)
            return getattr(instance, key)
    return Descriptor()