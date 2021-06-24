from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery


def test_is_available():
    oiio_binary_discovery = OiioBinariesDiscovery()

    assert oiio_binary_discovery.binaries_are_available()


def test_is_not_available():
    oiio_binary_discovery = OiioBinariesDiscovery()
    oiio_binary_discovery.get_oiiotool_executable = lambda: "testtesttest"

    assert not oiio_binary_discovery.binaries_are_available()
