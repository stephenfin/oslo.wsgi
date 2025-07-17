# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2010 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import routes.middleware
import webob


class Router:
    """WSGI middleware that maps incoming requests to WSGI apps."""

    def __init__(self, mapper):
        """Create a router for the given routes.Mapper.

        Each route in `mapper` must specify a 'controller', which is a
        WSGI app to call.  You'll probably want to specify an 'action' as
        well and have your controller be an object that can route
        the request to the action-specific method.

        >>> mapper = routes.Mapper()
        >>> sc = ServerController()

        >>> # Explicit mapping of one route to a controller+action
        >>> mapper.connect(None, '/svrlist', controller=sc, action='list')

        >>> # Actions are all implicitly defined
        >>> mapper.resource('server', 'servers', controller=sc)

        >>> # Pointing to an arbitrary WSGI app.  You can specify the
        >>> # {path_info:.*} parameter so the target app can be handed just
        >>> # that section of the URL.
        >>> mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())
        """
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(
            self._dispatch, self.map
        )

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.
        """
        return self._router

    @staticmethod
    @webob.dec.wsgify(RequestClass=webob.Request)
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app
