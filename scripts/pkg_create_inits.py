import os


def create_init_file_at_path(path: str, file_content: str) -> None:
    # Skip creating __init__.py if it already exists
    if os.path.exists(path):
        return

    # Create __init__.py if it doesn't exist
    with open(path, "w") as f:
        f.write(file_content)


def create_init_file(root: str, dir_name: str, file_content: str) -> None:
    init_file_path: str = os.path.join(root, dir_name, "__init__.py")
    create_init_file_at_path(path=init_file_path, file_content=file_content)


def create_init_files(root_dir_start: str, file_content: str) -> None:
    root_dir_start_init_path: str = os.path.join(root_dir_start, "__init__.py")
    root_dir_start_content: str = ""
    # root_dir_start_content: str = "\n".join([
    #     "import os",
    #     "import sys",
    #     "sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))",
    # ])
    create_init_file_at_path(
        path=root_dir_start_init_path,
        file_content=root_dir_start_content,
    )
    assert os.path.exists(root_dir_start_init_path)

    for root, dirs, _files in os.walk(root_dir_start):
        for dir_name in dirs:
            create_init_file(
                root=root,
                dir_name=dir_name,
                file_content=file_content,
            )


def main():
    # Set the directory you want to start from
    root_dir = 'nibiru_proto/nibiru'

    # Content to be written in each __init__.py file
    init_content = ''

    if not os.path.isdir(root_dir):
        raise Exception(
            f"directory {root_dir} is not visible from path: {os.getcwd()}",
        )

    create_init_files(root_dir, init_content)
    print("Successfully created __init__.py files!")


if __name__ == "__main__":
    main()
