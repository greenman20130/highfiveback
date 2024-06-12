capitalized_app_name = "chats".capitalize()

chats_single_create_request_example = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_type": "string",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_code": "string",
    "name": "string",
    "data": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    }
}

chats_single_create_response_example = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_date": "2023-06-29T08:58:09.300Z",
    "modified_date": "2023-06-29T08:58:09.300Z",
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_type": "string",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_code": "string",
    "name": "string",
    "meta": {
        "status": "active",
        "flags": 0,
        "internal_id": 33
    },
    "data": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    }
}

chats_single_retrieve_response_example = chats_single_create_response_example

chats_single_put_request_example = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    }

chats_single_put_response_example = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_date": "2023-06-29T08:58:09.300Z",
        "modified_date": "2023-06-30T11:45:18.234Z",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "meta": {
            "status": "active",
            "flags": 0,
            "internal_id": 33
        },
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    }

chats_single_patch_request_example = {
    "data": {
        "some_info": "string",
        "number": 15
      }
}

chats_single_patch_response_example = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_date": "2023-06-29T08:58:09.300Z",
    "modified_date": "2023-07-23T08:17:33.784Z",
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_type": "string",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_code": "string",
    "name": "string",
    "meta": {
        "status": "active",
        "flags": 0,
        "internal_id": 33
    },
    "data": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string",
        "some_info": "string",
        "number": 15
      }
}

chats_list_response_example = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "created_date": "2023-06-29T08:58:09.300Z",
    "modified_date": "2023-06-29T08:58:09.300Z",
    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_type": "string",
    "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "object_code": "string",
    "name": "string",
    "meta": {
        "status": "active",
        "flags": 0,
        "internal_id": 33
    },
    "data": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    }
}

chats_bulk_create_request_example = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    },
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    }
]

chats_bulk_create_response_example = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_date": "2023-06-29T08:58:09.300Z",
        "modified_date": "2023-06-29T08:58:09.300Z",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "meta": {
            "status": "active",
            "flags": 0,
            "internal_id": 33
        },
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    },
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_date": "2023-06-29T08:58:09.300Z",
        "modified_date": "2023-06-29T08:58:09.300Z",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "meta": {
            "status": "active",
            "flags": 0,
            "internal_id": 34
        },
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    }
]

chats_bulk_put_request_example = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    },
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    }
]

chats_bulk_put_response_example = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_date": "2023-06-29T08:58:09.300Z",
        "modified_date": "2023-06-30T11:45:18.234Z",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "meta": {
            "status": "active",
            "flags": 0,
            "internal_id": 33
        },
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    },
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_date": "2023-06-29T08:58:09.300Z",
        "modified_date": "2023-06-30T11:45:18.234Z",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_type": "string",
        "object_item": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
        "name": "string",
        "meta": {
            "status": "active",
            "flags": 0,
            "internal_id": 34
        },
        "data": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        }
    }
]

chats_bulk_patch_request_example = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
    },
   {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "object_code": "string",
    }
]

chats_bulk_patch_response_example = chats_bulk_create_response_example
