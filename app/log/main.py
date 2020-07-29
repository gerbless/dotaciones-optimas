import moment
from app.log.entities.logs import Elogs
from app.log.models.logs import add
from app.helpers.util import *


def log(data: tuple):
    add(Elogs(data[0], data[1], data[2], moment.now().format(ff_hh)))