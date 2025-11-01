class Description:
    class User:
        username: str = "Tên người dùng"
        email: str = "Email người dùng"
        password: str = "Mật khẩu 8 ký tự"


class Example:
    class User:
        username: list[str] = ["namtitak", "emnamit"]
        email: list[str] = ["thanhnamak@gmail.com"]
        password: list[str] = ["12345678"]