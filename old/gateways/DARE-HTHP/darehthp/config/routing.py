"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    
    map.connect('dare-hthp', '/', controller='hthpmd', action='index')
    map.connect('dare-hthp','/job_submit_md', controller='hthpmd', action='job_submit_md')
    map.connect('dare-hthp','/job_delete', controller='hthpmd', action='job_delete')
    map.connect('dare-hthp','/output_download', controller='hthpmd', action='output_download')
    map.connect('job_table_view','/job_table_view', controller='hthpmd', action='job_table_view')
    map.connect('dare-hthp','/download', controller='hthpmd', action='download')
    map.connect('dare-hthp','/contact', controller='hthpmd', action='contact')
    map.connect('dare-hthp','/job_status_update', controller='hthpmd', action='job_status_update')

    return map
