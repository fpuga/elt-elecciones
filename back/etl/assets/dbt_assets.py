import os
from pathlib import Path

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets


dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "dbt_project").resolve()

# print(dbt_project_dir)

dbt_resource = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt_resource.cli(["--quiet", "parse"], target_path=Path("target"))
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")


# class CustomDagsterDbtTranslator(DagsterDbtTranslator):
#     @classmethod
#     def get_asset_key(cls, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
#         asset_key = super().get_asset_key(dbt_resource_props)

#         if dbt_resource_props["resource_type"] == "model":
#             asset_key = asset_key.with_prefix(["postgres", "prod"])
#         if dbt_resource_props["resource_type"] == "source":
#             asset_key = asset_key.with_prefix("postgres")

#         return asset_key


# , dagster_dbt_translator=CustomDagsterDbtTranslator()
@dbt_assets(manifest=dbt_manifest_path)
def dbt_project_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# candidatos = get_asset_key_for_model([dbt_project_assets], "candidatos")
