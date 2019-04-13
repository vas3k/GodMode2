from typing import List

from flask import Flask

from godmode import logging
from godmode.models.base import BaseAdminModel
from godmode.models.godmode_auth import GodModeAuthAdminModel
from godmode.models.godmode_log import GodModeLogAdminModel
from godmode.models.godmode_sessions import GodModeSessionsAdminModel
from godmode.models.godmode_users import GodModeUsersAdminModel
from godmode.models.utils import model_hash

log = logging.getLogger(__name__)

internal_model_classes = [
    GodModeUsersAdminModel,
    GodModeAuthAdminModel,
    GodModeSessionsAdminModel,
    GodModeLogAdminModel
]

models = []
model_map = {}


def init_internal_models(app: Flask):
    for internal_model_class in internal_model_classes:
        log.debug("Initializing internal model: '{}'".format(internal_model_class.__name__))
        model = internal_model_class(app=app)
        models.append(model)
        model_map[model_hash(model)] = model


def init_models(app: Flask, model_classes: List[BaseAdminModel]):
    for model_class in model_classes:
        log.debug("Initializing model: '{}'".format(model_class.__name__))
        model = model_class(app=app)
        models.append(model)
        model_map[model_hash(model)] = model
