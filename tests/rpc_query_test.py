import nibiru
from nibiru import Network


def test_websocket_listen(val_node: nibiru.Sdk, network: Network):
    """
    Open a position and ensure output is correct
    """
    assert isinstance(val_node.query.chain.last_block_height(), int)
    assert isinstance(val_node.query.chain.version(), str)
