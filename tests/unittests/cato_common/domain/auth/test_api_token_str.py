from cato_common.domain.auth.api_token_str import ApiTokenStr


def test_get_data_dict(api_token_str):
    assert api_token_str.data_dict() == {
        "createdAt": "2022-03-21T16:23:49.262153",
        "expiresAt": "2022-03-21T18:23:49.262153",
        "id": "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f",
        "name": "test",
    }
