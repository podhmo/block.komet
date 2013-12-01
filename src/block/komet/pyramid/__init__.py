# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

def includeme(config):
    config.include("block.form")
    from block.form.validation.core import AppendListErrorControl
    config.block_set_error_control(AppendListErrorControl({}))
    config.include(".registering")
    config.include(".resources")
    config.include(".validation")

