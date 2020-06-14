def load_file_as_set(path):
    with open(path, "r") as f:
        return set(map(lambda x: x.strip(), f.readlines()))
