import os
import redivis
import redivis.classes.Table

os.environ["REDIVIS_API_TOKEN"] = 'ReplaceMe'


# dataset = redivis.user("user_name").dataset("dataset_name", version="next")

# Create a table on the dataset. Datasets may have multiple tables

def create_table(dataset, table_name, table_description) -> redivis.classes.Table.Table:
    table = (
        dataset
            .table("First-Table")
            .create(description="Some description")
    )
    return table


def upload_table(table, filename):
    upload = table.upload("data.csv")

    with open("data.csv", "rb") as file:
        upload.create(
            file,
            type="delmited",
            remove_on_fail=True,  # Remove the upload if a failure occurs
            wait_for_finish=True,  # Wait for the upload to finish processing
            raise_on_fail=True  # Raise an error on failure
        )


def create_dataset(organization_name, dataset_name):
    # Could also create a dataset under an organization:
    dataset = redivis.organization("EIDC").dataset("Demo Dataset")

    # public_access_level can be one of ('none', 'overview', 'metadata', 'sample', 'data')
    dataset.create(public_access_level="data")

# Upload a file to the table.
# You can create multiple uploads per table, in which case they'll be appended together.
