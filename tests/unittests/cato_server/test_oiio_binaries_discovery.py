from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscorvery


def test_is_available():
    oiio_binary_discovery = OiioBinariesDiscorvery()

    assert oiio_binary_discovery.binaries_are_available()


def test_is_not_available():
    oiio_binary_discovery = OiioBinariesDiscorvery()
    oiio_binary_discovery.get_oiiotool_executable = lambda: "testtesttest"

    assert not oiio_binary_discovery.binaries_are_available()
