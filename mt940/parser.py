# vim: fileencoding=utf-8:
'''

Format
---------------------

Sources:

.. _Swift for corporates: http://www.sepaforcorporates.com/\
    swift-for-corporates/account-statement-mt940-file-format-overview/
.. _Rabobank MT940: https://www.rabobank.nl/images/\
    formaatbeschrijving_swift_bt940s_1_0_nl_rib_29539296.pdf

 - `Swift for corporates`_
 - `Rabobank MT940`_

::

    [] = optional
    ! = fixed length
    a = Text
    x = Alphanumeric, seems more like text actually. Can include special
        characters (slashes) and whitespace as well as letters and numbers
    d = Numeric separated by decimal (usually comma)
    c = Code list value
    n = Numeric
'''

import os

import mt940
import re
import json

def parse(src, encoding=None):
    '''
    Parses mt940 data and returns transactions object

    :param src: file handler to read, filename to read or raw data as string
    :return: Collection of transactions
    :rtype: Transactions
    '''

    def safe_is_file(filename):
        try:
            return os.path.isfile(src)
        except ValueError:  # pragma: no cover
            return False

    if hasattr(src, 'read'):  # pragma: no branch
        data = src.read()
    elif safe_is_file(src):
        with open(src, 'rb') as fh:
            data = fh.read()
    else:  # pragma: no cover
        data = src

    if hasattr(data, 'decode'):  # pragma: no branch
        exception = None
        encodings = [encoding, 'utf-8', 'cp852', 'iso8859-15', 'latin1']

        for encoding in encodings:  # pragma: no cover
            if not encoding:
                continue

            try:
                data = data.decode(encoding)
                break
            except UnicodeDecodeError as e:
                exception = e
            except UnicodeEncodeError:
                break
        else:
            raise exception  # pragma: no cover
    accounts_list =[]
    splits = re.compile(
        r'{1:[^<>]*?-}',
        re.MULTILINE)
    split_matches = list(splits.finditer(data))
    # print(split_matches)
    for i, match in enumerate(split_matches):
        transactions = mt940.models.Transactions()
        transactions.parse(match.group(0))
        data = json.loads(json.dumps(transactions, indent=4,cls=mt940.JSONEncoder))
        accounts_list.append(data)


    # print(accounts_list)
    return accounts_list