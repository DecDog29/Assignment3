from yowd.services.ids import IdGenerator
from yowd.storage.json_store import JsonStore


def test_store_roundtrip(tmp_path):
    store = JsonStore(tmp_path)
    assert store.load_list("deliveries") == []
    store.save("deliveries", [{"a": 1}])
    assert store.load_list("deliveries") == [{"a": 1}]


def test_ids_increment_and_persist(tmp_path):
    ids = IdGenerator(JsonStore(tmp_path))
    assert ids.next_id("YD") == "YD-0001"
    assert ids.next_id("YD") == "YD-0002"
    assert IdGenerator(JsonStore(tmp_path)).next_id("YD") == "YD-0003"
