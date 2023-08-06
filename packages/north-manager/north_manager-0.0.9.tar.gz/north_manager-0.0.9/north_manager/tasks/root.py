import logging
from invoke import task
from north_manager.gui import main

logger = logging.getLogger(__name__)


@task
def ui(c):
    main.start()