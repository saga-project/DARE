"""Setup the DARE-HTHP application"""
import logging

from darehthp.config.environment import load_environment

log = logging.getLogger(__name__)
from darehthp.model.meta import Session, Base

#change this to work with new model error meta data
def setup_app(command, conf, vars):
    """Place any commands to setup darebioscope here"""
    # Don't reload the app if it was loaded under the testing environment
    load_environment(conf.global_conf, conf.local_conf)
    log.info("Creating tables")
    Base.metadata.drop_all(bind=Session.bind, checkfirst=True)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")