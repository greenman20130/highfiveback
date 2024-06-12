single_valid_payload = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "6",
    "data": {"data 1": "test data 1", "data 2": "test data 2"},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

single_invalid_object_item_payload = {
    "object_type": None,
    "name": "Object 1 Name",
    "object_code": "6",
    "data": {"data 1": "test data 1", "data 2": "test data 2"},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "ivalid_id",
}

single_invalid_account_id_payload = {
    "object_type": "object",
    "name": None,
    "object_code": "7",
    "data": {"data 1": "test data 1", "data 2": "test data 2"},
    "project_id": None,
    "account_id": "some_id",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

single_null_object_code_payload = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": None,
    "data": {"data 1": "test data 1", "data 2": "test data 2"},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

single_non_unique_object_code_payload = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "data": {"data 1": "test data 1", "data 2": "test data 2"},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

object1 = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "data": {"data 1": "test data 1", "data 2": "test data 2"},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

object2 = {
    "object_type": "object",
    "name": "Object 2 Name",
    "object_code": "2",
    "data": {"data 3": "test data 3", "data 4": "test data 4"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": None,
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

object3 = {
    "object_type": "different object",
    "name": "Object 3 Name",
    "object_code": "3",
    "data": {"data 5": "test data 5", "data 6": "test data 6"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": None,
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

object4 = {
    "object_type": "different object",
    "name": "Object 4 Name",
    "object_code": "4",
    "meta": {"status": "inactive", "flags": 254},
    "project_id": None,
    "account_id": None,
    "user_id": None,
    "object_item": None,
}

object5 = {
    "object_type": "object",
    "name": "Object 5 Name",
    "object_code": "1",
    "data": {},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": None,
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

valid_single_put = {
    "object_type": "different object",
    "name": "Object 1 Other Name",
    "object_code": "6",
    "meta": {"status": "active", "flags": 0, "internal_id": 1},
    "data": {"data 7": "test data 7", "data 8": "test data 8"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": None,
    "user_id": None,
    "object_item": None,
}

invalid_single_put = {
    "object_type": "different object",
    "name": "Object 1 Other Name",
    "object_code": "",
    "data": {"data 7": "test data 7", "data 8": "test data 8"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": None,
    "user_id": None,
    "object_item": None,
}

meta_payload_1 = {"object_type": "object", "name": "Object 1 Name", "object_code": "7", "meta": {}}

meta_payload_2 = {"object_type": "object", "name": "Object 1 Name", "object_code": "8", "meta": {"status": "inactive"}}

meta_payload_3 = {"object_type": "object", "name": "Object 1 Name", "object_code": "9", "meta": {"flags": 116}}

meta_payload_4 = {"object_type": "object", "name": "Object 1 Name", "object_code": "10", "meta": {"internal_id": 48}}

meta_payload_5 = {"object_type": "object", "name": "Object 1 Name", "object_code": "11"}

meta_payload_6 = {"object_type": "object", "name": "Object 1 Name", "object_code": "12"}

meta_payload_7 = {"object_type": "object", "name": "Object 1 Name", "object_code": "13"}

link_meta_payload_1 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

link_meta_payload_2 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "meta": {},
}

link_meta_payload_3 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "meta": {"status": "inactive"},
}

link_meta_payload_4 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "meta": {"flags": 116},
}

link_meta_payload_5 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "meta": {"internal_id": 48},
}

link_invalid_meta_payload = {"link_type": "O2O", "object1": None, "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}

meta_put_payload_1 = {
    "object_type": "object",
    "name": "Object 1",
    "object_code": "1",
    "data": {"data 1": "test data 1", "data 2": "test data 2", "digits": 12},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_put_payload_2 = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "meta": {},
    "data": {"data 1": "test data 1", "data 2": "test data 2", "digits": 12},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_put_payload_3 = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "meta": {"status": "inactive"},
    "data": {"data 1": "test data 1", "data 2": "test data 2", "digits": 12},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_put_payload_4 = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "meta": {"flags": 116},
    "data": {"data 1": "test data 1", "data 2": "test data 2", "digits": 12},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_put_payload_5 = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "meta": {"internal_id": 48},
    "data": {"data 1": "test data 1", "data 2": "test data 2", "digits": 12},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_put_payload_6 = {
    "object_type": "object",
    "name": "Object 1 Name",
    "object_code": "1",
    "meta": {"internal_id": 1, "status": "active", "flags": 0},
    "data": {"data 1": "test data 1", "data 2": "test data 2", "digits": 12},
    "project_id": None,
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_put_payload_1 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_put_payload_2 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "meta": {},
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_put_payload_3 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "meta": {"status": "inactive"},
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_put_payload_4 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "meta": {"flags": 116},
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_put_payload_5 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "meta": {"internal_id": 48},
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_invalid_put_payload = {
    "link_type": "O2O",
    "object1": None,
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}

meta_link_put_payload_6 = {
    "link_type": "O2O",
    "object1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object2": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "weight": 0.5,
    "direction": 1,
    "meta": {"internal_id": 1, "status": "active", "flags": 0},
    "data": {"additional": "data"},
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
}
