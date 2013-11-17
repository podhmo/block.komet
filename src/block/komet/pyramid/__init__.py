# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

def includeme(config):
    config.include(".registering")
    config.include(".resources")
    config.include(".validation")

