from dagster import Definitions, FilesystemIOManager, load_assets_from_package_module

from . import assets  # noqa: TID252
from .assets.dbt_assets import dbt_resource


io_manager = FilesystemIOManager(
    base_dir="data3"  # Path is built relative to where `dagster dev` is run
)

resources = {
    "io_manager": io_manager,
    # this resource is used to execute dbt cli commands
    "dbt": dbt_resource,
}

defs = Definitions(assets=load_assets_from_package_module(assets), resources=resources)
