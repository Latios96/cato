def test_get_data_dict(fixed_api_token_str):
    assert fixed_api_token_str.data_dict() == {
        "createdAt": "2022-03-21T17:15:24.328633",
        "expiresAt": "2022-03-21T19:15:24.328633",
        "id": "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f",
        "name": "test",
    }
