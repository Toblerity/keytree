import xml.etree.ElementTree
import lxml.etree

import pytest


@pytest.fixture(params=[lxml.etree, xml.etree.ElementTree])
def etree(request):
    return request.param
