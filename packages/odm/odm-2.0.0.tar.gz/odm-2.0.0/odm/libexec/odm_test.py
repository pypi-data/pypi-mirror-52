#!/usr/bin/env python

# This file is part of ODM and distributed under the terms of the
# MIT license. See COPYING.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import sys

import odm.cli


def main():
    odm.cli.CLI.writer_wrap(sys)
    cli = odm.cli.CLI([])

    payload = {
        'displayName': 'ezekielh Test',
        'mailEnabled': True,
        'mailNickname': 'ezekielh-test',
        'securityEnabled': False,
        'groupTypes': [
            'Unified',
        ],
        'visibility': 'Private',
    }

    result = cli.client.msgraph.post('/groups', json = payload)
    print(json.dumps(result.json(), indent = 2))


if __name__ == '__main__':
    main()
