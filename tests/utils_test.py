def test_dict_must_be_deserialized():

    tests = [
        {
            "name": "happy path",
            "value": {
                "key_1": 100.1,
                "key_2": 100,
                "key_3": "asdlb",
                "key_4": "1000luna",
                "nested_dict": {
                    "key_1": 100.1,
                    "key_2": 100,
                    "key_3": "asdlb",
                    "key_4": "1000luna",
                },
            },
        },
        {
            "name": "string formatted float",
            "expected_raise": ValueError,
            "value": {
                "key_1": "100.1",
                "key_2": 100,
                "key_3": "asdlb",
                "key_4": "1000luna",
            },
        },
        {
            "name": "string formatted float in nested dict",
            "expected_raise": ValueError,
            "value": {
                "key_1": 100.1,
                "key_2": 100,
                "key_3": "asdlb",
                "key_4": "1000luna",
                "nested_dict": {
                    "key_1": "100.1",
                    "key_2": 100,
                    "key_3": "asdlb",
                    "key_4": "1000luna",
                },
            },
        },
        {
            "name": "weird object",
            "expected_raise": TypeError,
            "value": {
                "key_1": 100.1,
                "key_2": Exception,
                "key_3": "asdlb",
                "key_4": "1000luna",
                "nested_dict": {
                    "key_1": "100.1",
                    "key_2": 100,
                    "key_3": "asdlb",
                    "key_4": "1000luna",
                },
            },
        },
    ]

    for test in tests:
        if test.get("expected_raise") is not None:
            with raises(test["expected_raise"]):
                dict_must_be_deserialized(test["value"])

        else:
            dict_must_be_deserialized(test["value"])


if __name__ == '__main__':
    unittest.main()
