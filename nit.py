import json
import sys
import os
import platform
import requests

GITHUB_REPO_URL = 'https://diamondgotcat.github.io/HTI/packages.json'

def load_repository():
    response = requests.get(GITHUB_REPO_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"(×) Failed to fetch repository.json: {response.status_code}")
        sys.exit(1)

def package_info(package_name):
    repo = load_repository()
    package = repo['packages'].get(package_name)
    if package:
        print(f"(÷) Name: {package['name']}")
        print(f"(𝑓) Description: {package['description']}")
        print(f"(☯︎) Main URL: {package['main_url']}")
        for version, details in package['versions'].items():
            print(f"(☆) Version: {version}")
            print(f"  (☯︎) URL: {details['url']}")
            print(f"  (≑) Type: {details['type']}")
            print(f"  (∞) Platforms: {', '.join(details['platforms'])}")
        print(f"(−) Uninstall URL: {package['uninstall_url']}")
    else:
        print(f"(×) Package '{package_name}' not found.")

def install_package(package_name):
    repo = load_repository()
    package = repo['packages'].get(package_name)
    if package:
        system_platform = platform.system().lower()
        for version, details in package['versions'].items():
            if system_platform in [p.lower() for p in details['platforms']]:
                os.system(f"curl -LO {details['url']}")
                if details['type'] == 'binary':
                    os.system(f"chmod +x {os.path.basename(details['url'])}")
                    os.system(f"./{os.path.basename(details['url'])}")
                    os.remove(f"./{os.path.basename(details['url'])}")
                print(f"(+) Package '{package_name}' installed.")
                return
        print(f"(×) No compatible version found for platform '{system_platform}'.")
    else:
        print(f"(×) Package '{package_name}' not found.")

def uninstall_package(package_name):
    repo = load_repository()
    package = repo['packages'].get(package_name)
    if package:
        uninstall_url = package.get('uninstall_url')
        if uninstall_url:
            os.system(f"curl -LO {uninstall_url}")
            os.system(f"chmod +x {os.path.basename(uninstall_url)}")
            os.system(f"./{os.path.basename(uninstall_url)}")
            print(f"(+) Package '{package_name}' uninstalled.")
        else:
            print(f"(×) No uninstall URL found for package '{package_name}'.")
    else:
        print(f"(×) Package '{package_name}' not found.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python nit.py <command> <package>")
        sys.exit(1)
    
    command = sys.argv[1]
    package_name = sys.argv[2]
    
    try:

        if command == "info":
            package_info(package_name)
        elif command == "install":
            install_package(package_name)
        elif command == "uninstall":
            uninstall_package(package_name)
        else:
            print(f"(×) Unknown command '{command}'")

    except KeyError:
        pass
