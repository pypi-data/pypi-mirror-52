# Copyright (C) 2019 Intek Institute.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Intek Institute or one of its subsidiaries.  You shall not disclose
# this confidential information and shall use it only in accordance
# with the terms of the license agreement or other applicable
# agreement you entered into with Intek Institute.
#
# INTEK INSTITUTE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  INTEK
# INSTITUTE SHALL NOT BE LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY
# LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THIS
# SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.client.service.base_service import BaseService


class RouteService(BaseService):
    def get_route(self, route_id):
        """
        Return the Base64 string of the encrypted data of a route.


        :param route_id: Identification of a route.


        :raise InvalidArgumentException: If the route identification passed to
            this function is of an invalid format.

        :raise UndefinedObjectException: If no route has been found for the
            specified identification.
        """
        return self.send_request(
            http_method=self.HttpMethod.GET,
            path='/route/(route_id)',
            url_bits={
                'route_id': route_id
            },
            authentication_required=False,
            signature_required=True)
