import pytest

from xml.etree import ElementTree


@pytest.fixture(params=["lxml", "ElementTree"])
def etree(request):
    if request.param == "lxml":
        etree = pytest.importorskip("lxml.etree")
    else:
        etree = ElementTree
    return etree
