from cato_common.domain.auth.api_token_str import ApiTokenStr

TOKEN_STR = ApiTokenStr(
    b"eyJuYW1lIjogInRlc3QiLCAiaWQiOiAiYWI1ZDIwMDA4YmIxZjI3YTE0NDJhNGRhMzk4YzAxNzEyYjQ4NThkMDYyMWJlZjA4NjAyYjc2ZjEwNGNlZjE2ZiIsICJjcmVhdGVkQXQiOiAiMjAyMi0wMy0yMVQxNjoyMzo0OS4yNjIxNTMiLCAiZXhwaXJlc0F0IjogIjIwMjItMDMtMjFUMTg6MjM6NDkuMjYyMTUzIn0=.YjiYhQ.9a86jRujda3vlV13aX6GPwRIO2M"
)


def test_get_data_dict():
    assert TOKEN_STR.data_dict() == {
        "createdAt": "2022-03-21T16:23:49.262153",
        "expiresAt": "2022-03-21T18:23:49.262153",
        "id": "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f",
        "name": "test",
    }
