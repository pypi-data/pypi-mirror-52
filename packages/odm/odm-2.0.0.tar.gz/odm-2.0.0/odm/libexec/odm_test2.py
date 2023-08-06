#!/usr/bin/env python

# This file is part of ODM and distributed under the terms of the
# MIT license. See COPYING.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import sys

import odm.cli

from odm import sharepointsession


def main():
    odm.cli.CLI.writer_wrap(sys)
    cli = odm.cli.CLI([])

    client = sharepointsession.SharepointSession(
        'https://{}.sharepoint.com/'.format(cli.config['microsoft']['tenant']),
        cli.config['microsoft'],
        60
    )

    result = client.post(
        '_api/SP.UserProfiles.ProfileLoader.GetProfileLoader/CreatePersonalSiteEnqueueBulk',
        json = {
            'emailIDs': [
                'admin-crm@umichdevelop.onmicrosoft.com',
            ]
        },
    )

    print(json.dumps(result.json(), indent = 2))


if __name__ == '__main__':
    main()
