#!/usr/bin/env python
from pathlib import Path

from cdktf import AssetType, TerraformAsset, TerraformOutput, TerraformStack
from cdktf_cdktf_provider_google import (
    CloudfunctionsFunction,
    CloudfunctionsFunctionIamBinding,
    GoogleProvider,
    StorageBucket,
    StorageBucketObject,
)
from constructs import Construct
from decouple import config
from imports.random import Id as RandomId
from imports.random import RandomProvider
from config import REGION, EnvData

APPLICATION_DIR = Path(__file__).resolve().parents[2] / "application"


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str, env_data: EnvData):
        super().__init__(scope, ns)
        self.env_data = env_data

        # define resources here

        RandomProvider(self, "random_provider")
        self.rid = RandomId(self, "rid", byte_length=4)

        GoogleProvider(
            self,
            self.env_name("google-provider"),
            region=REGION,
            zone=f"{REGION}-a",
            project=config("PROJECT_ID"),
        )

        storage_bucket = StorageBucket(
            self,
            "storage_bucket",
            name=self.env_name("sb"),
        )

        asset = TerraformAsset(
            self,
            "functions_asset",
            path=str(APPLICATION_DIR.absolute()),
            type=AssetType.ARCHIVE,
        )

        build_artifact_storage_object = StorageBucketObject(
            self,
            "storage_bucket_obj",
            name=f"{self.env_name('cf')}.zip",
            bucket=storage_bucket.name,
            source=asset.path,
        )

        cloud_function = CloudfunctionsFunction(
            self,
            "cloud_function",
            name=self.env_name("cf"),
            description="CDKTF Cloud Function",
            runtime="python38",
            entry_point="hello_http",
            source_archive_bucket=storage_bucket.name,
            source_archive_object=build_artifact_storage_object.name,
            trigger_http=True,
        )

        # iam entry to allow users invoke the function
        CloudfunctionsFunctionIamBinding(
            self,
            "cf_iam_binding",
            project=config("PROJECT_ID"),
            region=REGION,
            cloud_function=cloud_function.name,
            role="roles/cloudfunctions.invoker",
            members=["allUsers"],
        )

        TerraformOutput(
            self,
            "cloud_function_output",
            value=cloud_function.https_trigger_url,
        )
        TerraformOutput(self, "storage_bucket_output", value=storage_bucket.url)

    def env_name(self, name, no_dash=False):
        env_name = f"{self.env_data.env_name(name)}-{self.rid.hex}"
        return env_name.replace("-", "") if no_dash else env_name
