import json
import sys
import os
import platform
import requests

GITHUB_REPO_URL = 'https://diamondgotcat.github.io/HTI/packages.json'

ColorCodes = {

    "Reset": "\033[0m",
    "Red": "\033[1m\033[31m",
    "Green": "\033[1m\033[32m",
    "Yellow": "\033[1m\033[33m",
    "Blue": "\033[34m",
    "Purple": "\033[35m",
    "Cyan": "\033[1m\033[36m",
    "Bold": "\033[1m"

}

def load_repository():
    response = requests.get(GITHUB_REPO_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{ColorCodes['Red']}(×) Failed to fetch repository.json: {response.status_code}{ColorCodes['Reset']}")
        sys.exit(1)

def package_info(package_name):
    repo = load_repository()
    package = repo['packages'].get(package_name)
    if package:
        print(f"{ColorCodes['Cyan']}(÷) Name: {package['name']}{ColorCodes['Reset']}")
        print(f"(𝑓) Description: {package['description']}")
        print(f"(☯︎) Main URL: {package['main_url']}")
        for version, details in package['versions'].items():
            print(f"(☆) V{version}")
            print(f"  (☯︎) URL: {details['url']}")
            print(f"  (≑) Type: {details['type']}")
            print(f"  (∞) Platforms: {', '.join(details['platforms'])}")
        print(f"(−) Uninstall URL: {package['uninstall_url']}")
    else:
        print(f"{ColorCodes['Red']}(×) Package '{package_name}' not found.{ColorCodes['Reset']}")

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
                elif details['type'] == 'python':
                    os.system(f"python3 {os.path.basename(details['url'])}")
                    os.remove(f"./{os.path.basename(details['url'])}")
                print(f"{ColorCodes['Green']}(+) Package '{package_name}' installed.{ColorCodes['Reset']}")
                return
        print(f"{ColorCodes['Red']}(×) No compatible version found for platform '{system_platform}'.{ColorCodes['Reset']}")
    else:
        print(f"{ColorCodes['Red']}(×) Package '{package_name}' not found.{ColorCodes['Reset']}")

def install_package_by_version(package_name,wantversion):
    repo = load_repository()
    package = repo['packages'].get(package_name)
    if package:
        system_platform = platform.system().lower()
        for version, details in package['versions'].items():

            if wantversion == version:

                if system_platform in [p.lower() for p in details['platforms']]:
                    os.system(f"curl -LO {details['url']}")
                    if details['type'] == 'binary':
                        os.system(f"chmod +x {os.path.basename(details['url'])}")
                        os.system(f"./{os.path.basename(details['url'])}")
                        os.remove(f"./{os.path.basename(details['url'])}")
                    print(f"{ColorCodes['Green']}(+) Package '{package_name}' installed.{ColorCodes['Reset']}")
                    return
            

        print(f"{ColorCodes['Red']}(×) No compatible version found for platform '{system_platform}'.{ColorCodes['Reset']}")
    else:
        print(f"{ColorCodes['Red']}(×) Package '{package_name}' not found.{ColorCodes['Reset']}")

def uninstall_package(package_name):
    repo = load_repository()
    package = repo['packages'].get(package_name)
    if package:
        uninstall_url = package.get('uninstall_url')
        if uninstall_url:
            os.system(f"curl -LO {uninstall_url}")
            os.system(f"chmod +x {os.path.basename(uninstall_url)}")
            os.system(f"./{os.path.basename(uninstall_url)}")
            print(f"{ColorCodes['Green']}(+) Package '{package_name}' uninstalled.{ColorCodes['Reset']}")
        else:
            print(f"{ColorCodes['Red']}(×) No uninstall URL found for package '{package_name}'.{ColorCodes['Reset']}")
    else:
        print(f"{ColorCodes['Red']}(×) Package '{package_name}' not found.{ColorCodes['Reset']}")

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

            i = 2
            while True:
                
                if ( len(sys.argv) ) > ( i + 1 ):
                    print(f"{ColorCodes['Cyan']}(#) install {sys.argv[i]} V{sys.argv[i+1]}{ColorCodes['Reset']}")
                    install_package_by_version(sys.argv[i],sys.argv[i+1])
                    i += 2
                else:
                    print(f"{ColorCodes['Cyan']}(#) install {sys.argv[i]}{ColorCodes['Reset']}")
                    install_package(sys.argv[i])
                    i += 1

                if i >= len(sys.argv):
                    break

        elif command == "uninstall":
            uninstall_package(package_name)
        else:
            print(f"{ColorCodes['Red']}(×) Unknown command '{command}'{ColorCodes['Reset']}")

    except KeyError:
        pass
