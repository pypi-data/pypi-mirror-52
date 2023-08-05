import pytest
rbc_omnisci = pytest.importorskip('rbc.mapd')


def omnisci_is_available():
    """Return True if OmniSci server is accessible.
    """
    omnisci = rbc_omnisci.RemoteMapD()
    client = omnisci.make_client()
    try:
        version = client(MapD=dict(get_version=()))['MapD']['get_version']
    except Exception as msg:
        return False, 'failed to get OmniSci version: %s' % (msg)
    print(version)
    if version >= '4.6':
        return True, None
    return False, 'expected OmniSci version 4.6 or greater, got %s' % (version)


is_available, reason = omnisci_is_available()
pytestmark = pytest.mark.skipif(not is_available, reason=reason)


def test_version():
    pass
