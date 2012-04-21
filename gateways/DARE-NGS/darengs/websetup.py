"""Setup the DARE-NGS application"""
import logging

from darengs.config.environment import load_environment

log = logging.getLogger(__name__)
from darengs.model.meta import Base, Session


def setup_app(command, conf, vars):
    """Place any commands to setup darebioscope here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)
    log.info("Creating tables")
    Base.metadata.drop_all(bind=Session.bind, checkfirst=True)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")

