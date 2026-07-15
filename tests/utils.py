# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#    _  m
#  ,`.\/'>
#  (`\<_/`
#    `<<
#
# Author: Johan Hanekom
# Date: March 2026
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~


import re


def get_test_name(
    node_name: str,
) -> str:
    # add the "request: pytest.FixtureRequest" fixture
    # get the name via "str(request.node.name)"

    p = r"^(?P<test_name>.*)\[.*\]$"
    m = re.match(p, node_name)
    if m:
        return m.group("test_name")

    # Then it's probably not a parameterized test
    return node_name
