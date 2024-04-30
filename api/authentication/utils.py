def generate_name_from_username(username: str) -> str:
    return (
        username.replace("@", " ")
        .replace(".", " ")
        .replace("+", " ")
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )
