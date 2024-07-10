import subprocess
import time
import os


def update_pip_requirements():
    # Check if requirements.in exists
    if not os.path.exists("requirements.in"):
        print("Error: requirements.in not found in the current directory")
        return 1

    # Store the current list of installed packages
    old_packages = subprocess.check_output(["pip", "freeze"]).decode().splitlines()

    # Run pip-compile
    subprocess.run(["pip-compile", "requirements.in"])

    # Wait for the file to be updated
    time.sleep(2)

    # Install packages from the updated requirements.txt
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

    # Get the new list of required packages
    with open("requirements.txt", "r") as f:
        new_packages = [
            line.split("==")[0]
            for line in f
            if not line.startswith("#") and line.strip()
        ]

    # Uninstall packages that are no longer in requirements.txt
    for package in old_packages:
        package_name = package.split("==")[0]
        if package_name not in new_packages:
            subprocess.run(["pip", "uninstall", "-y", package_name])


if __name__ == "__main__":
    update_pip_requirements()
