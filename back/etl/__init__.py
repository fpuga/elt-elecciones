from dagster import Definitions, FilesystemIOManager, load_assets_from_package_module

from . import assets  # noqa: TID252:


io_manager = FilesystemIOManager(
    base_dir="data3"  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=load_assets_from_package_module(assets), resources={"io_manager": io_manager}
)
