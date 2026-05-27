import json
import requests
from copy import deepcopy

# Download latest official ESP32 package
url = "https://espressif.github.io/arduino-esp32/package_esp32_index.json"

response = requests.get(url)

original = response.json()

# Load board names
with open("boards.json", "r", encoding="utf-8") as f:
    board_config = json.load(f)

base_package = original["packages"][0]

final_output = {
    "packages": []
}

for board_name in board_config["boards"]:

    pkg = deepcopy(base_package)

    # Rename package
    pkg["name"] = board_name

    # Rename all platforms + dependencies
    for platform in pkg.get("platforms", []):

        platform["name"] = board_name

        for dep in platform.get("toolsDependencies", []):

            if dep.get("packager") == "esp32":
                dep["packager"] = board_name

    final_output["packages"].append(pkg)

# Save generated file
with open("../package_multi_esp32_index.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print("Generated successfully")