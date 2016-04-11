import contextpy

def test_layerstack_unique():
    l1 = contextpy.layer("l1")
    l2 = contextpy.layer("l2")
    s1 = contextpy.layerstack([l1, l2])
    s2 = contextpy.layerstack([l1, l2])
    assert s1 is s2
