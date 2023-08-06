import os
from pathlib import Path
from rikki.template.environment import environment_template
from rikki.template.feature import feature_template


def behave_init():
    features_folder_name = "features"
    if not os.path.exists(Path(features_folder_name)):
        os.makedirs(Path(features_folder_name))

    steps_folder_path = Path("{0}/steps".format(features_folder_name))

    if not os.path.exists(steps_folder_path):
        os.makedirs(steps_folder_path)

    with open(Path("features/environment.py"), "w") as environment:
        environment.write(environment_template)

    with open(Path("features/steps/example.feature"), "w") as example_feature:
        example_feature.write(feature_template)
