from mapper.loader import Loader


def test_get_files_to_load():
    l = Loader()
    files = l.get_local_map_file_names()
    assert len(files) == 1


def test_build_local_maps():
    l = Loader()
    m = l.build_local_maps()
    assert len(m) == 1
    assert m[0]['app_name'] == "Conta"


def test_build_remote_maps():
    l = Loader()
    m = l.build_remote_maps()
    assert len(m) == 1
    assert m[0]['app_name'] == "Conta"


def test_build_maps():
    l = Loader()
    m = l.build()
    assert len(m) == 2
