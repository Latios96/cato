def validate_name(name):
    if not name:
        raise ValueError("Test name can not be empty!")

    for c in name:
        if c in [" ", "/", ",", ".", "\\", '"', "'"]:
            raise ValueError(f"Test name {name} contains not allowed character: {c}")
