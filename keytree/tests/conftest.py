import pytest

from xml.etree import ElementTree


@pytest.fixture(params=["lxml", "ElementTree"])
def etree(request):
    if request.param == "lxml":
        etree = pytest.importorskip("lxml")
    else:
        etree = ElementTree
    return etree
