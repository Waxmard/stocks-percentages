import subprocess
import time
import os


def update_pip_requirements():
    if not os.path.exists("requirements.in"):
        print("Error: requirements.in not found in the current directory")
        return 1

    old_packages = subprocess.check_output(["pip", "freeze"]).decode().splitlines()

    subprocess.run(["pip-compile", "requirements.in"])

    time.sleep(2)

    subprocess.run(["pip", "install", "-r", "requirements.txt"])

    with open("requirements.txt", "r") as f:
        new_packages = [
            line.split("==")[0]
            for line in f
            if not line.startswith("#") and line.strip()
        ]

    # Read packages from requirements.in
    with open("requirements.in", "r") as f:
        required_packages = [
            line.split("#")[0].strip()
            for line in f
            if not line.startswith("#") and line.strip()
        ]

    # Uninstall packages that are no longer in requirements.txt,
    # but don't uninstall packages listed in requirements.in
    for package in old_packages:
        package_name = package.split("==")[0]
        if package_name not in new_packages and package_name not in required_packages:
            subprocess.run(["pip", "uninstall", "-y", package_name])


if __name__ == "__main__":
    update_pip_requirements()
