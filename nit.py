import json
import sys
import os
import platform
import requests
import argparse
import time
from KamuJpModern import KamuJpModern

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

class Downloader:
    ONE_MB = 1024 * 1024

    def __init__(self):
        self.total_downloaded = 0
        self.progress_bar = KamuJpModern().modernProgressBar(
            total=0,
            process_name="Downloading",
            process_color=32
        )
        self.start_time = time.time()
        self.logger = KamuJpModern().modernLogging(process_name="Downloader")

    def get_file_size(self, url):
        try:
            response = requests.head(url, allow_redirects=True)
            response.raise_for_status()
            file_size = int(response.headers.get('Content-Length', 0))
            if file_size == 0:
                raise ValueError("Content-Length is zero or not provided.")
            return file_size
        except (requests.RequestException, ValueError):
            response = requests.get(url, stream=True)
            response.raise_for_status()
            file_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_size += len(chunk)
            return file_size

    def on_unit_downloaded(self, bytes_downloaded):
        elapsed_time = time.time() - self.start_time
        total_downloaded_mb = self.total_downloaded / self.ONE_MB
        elapsed_time_formatted = time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time))
        log_message = f"{total_downloaded_mb:.2f} MB downloaded in {elapsed_time_formatted}"
        self.progress_bar.logging(log_message)

    def download_file(self, url, output_path):
        file_size = self.get_file_size(url)
        if file_size == 0:
            print("Failed to get file size.")
            return
        unit_multiplier = self.ONE_MB
        total_units = file_size / unit_multiplier
        self.progress_bar.total = total_units
        self.progress_bar.start()
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error occurred during download: {e}")
            return
        downloaded = 0
        self.total_downloaded = 0 
        self.start_time = time.time()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    chunk_size = len(chunk)
                    downloaded += chunk_size
                    self.total_downloaded += chunk_size
                    self.on_unit_downloaded(downloaded)
                    self.progress_bar.update(downloaded / unit_multiplier)
                    downloaded = 0
            if downloaded > 0:
                self.on_unit_downloaded(downloaded)
        self.progress_bar.finish()

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
                downloader = Downloader()
                downloader.download_file(details['url'], output_path=os.path.basename(details['url']))
                if details['type'] == 'binary':
                    os.system(f"chmod +x {os.path.basename(details['url'])}")
                    os.system(f"./{os.path.basename(details['url'])}")
                    os.remove(f"./{os.path.basename(details['url'])}")
                elif details['type'] == 'python':
                    os.system(f"{sys.executable} {os.path.basename(details['url'])}")
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
                    downloader = Downloader()
                    downloader.download_file(details['url'], output_path=os.path.basename(details['url']))
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
            downloader = Downloader()
            downloader.download_file(uninstall_url, output_path=os.path.basename(uninstall_url))
            os.system(f"chmod +x {os.path.basename(uninstall_url)}")
            os.system(f"./{os.path.basename(uninstall_url)}")
            print(f"{ColorCodes['Green']}(+) Package '{package_name}' uninstalled.{ColorCodes['Reset']}")
        else:
            print(f"{ColorCodes['Red']}(×) No uninstall URL found for package '{package_name}'.{ColorCodes['Reset']}")
    else:
        print(f"{ColorCodes['Red']}(×) Package '{package_name}' not found.{ColorCodes['Reset']}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        
        command = input("mode(info|install|uninstall): ")
        package_name = input("package-name: ")
        
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
        
    else:
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
