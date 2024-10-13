import argparse
import requests
import sys
import os

def download_vexos(platform, version=None, output_path=None, output_name=None):
    base_url = f"https://content.vexrobotics.com/vexos/public/{platform}"
    catalog_url = f"{base_url}/catalog.txt"

    try:
        response = requests.get(catalog_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching catalog.txt: {e}")
        sys.exit(1)

    latest_version = response.text.strip()

    if version:
        vexos_name = version + ".vexos"
    else:
        vexos_name = latest_version + ".vexos"

    vexos_url = f"{base_url}/{vexos_name}"

    if output_name:
        filename = output_name
    else:
        filename = vexos_name

    if output_path:
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, filename)
    else:
        file_path = filename

    try:
        print(f"Downloading {vexos_name}...")
        r = requests.get(vexos_url, stream=True)
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {vexos_name} to {file_path}")
    except requests.RequestException as e:
        print(f"Error downloading {vexos_name}: {e}")
        sys.exit(1)


def list_vexos_versions(platform):
    base_url = f"https://content.vexrobotics.com/vexos/public/{platform}"
    catalog_url = f"{base_url}/catalog.txt"

    try:
        response = requests.get(catalog_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching catalog.txt: {e}")
        sys.exit(1)

    latest_version = response.text.strip()
    print(f"Latest VEXos version for {platform}: {latest_version}")


def download_sdk(
    platform,
    language,
    version=None,
    output_path=None,
    output_name=None,
    download_all=False,
):
    languages = ["cpp", "python"] if language == "both" else [language]
    for lang in languages:
        base_url = (
            f"https://content.vexrobotics.com/vexos/public/{platform}/vscode/sdk/{lang}"
        )
        manifest_url = f"{base_url}/manifest.json"

        try:
            response = requests.get(manifest_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching manifest.json for {lang}: {e}")
            continue

        manifest = response.json()
        latest_version = manifest["latest"]
        catalog = manifest["catalog"]

        versions_to_download = []

        if download_all:
            versions_to_download = catalog
        else:
            if version:
                if version in catalog:
                    versions_to_download = [version]
                else:
                    print(f"Version {version} not found in catalog for {lang}.")
                    continue
            else:
                versions_to_download = [latest_version]

        for ver in versions_to_download:
            sdk_name = ver + ".zip"
            sdk_url = f"{base_url}/{sdk_name}"

            if output_name:
                filename = output_name
            else:
                filename = sdk_name

            if output_path:
                os.makedirs(output_path, exist_ok=True)
                file_path = os.path.join(output_path, filename)
            else:
                file_path = filename

            try:
                print(f"Downloading {sdk_name} for {lang}...")
                r = requests.get(sdk_url, stream=True)
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded {sdk_name} to {file_path}")
            except requests.RequestException as e:
                print(f"Error downloading {sdk_name}: {e}")


def list_sdk_versions(platform, language):
    languages = ["cpp", "python"] if language == "both" else [language]
    for lang in languages:
        base_url = (
            f"https://content.vexrobotics.com/vexos/public/{platform}/vscode/sdk/{lang}"
        )
        manifest_url = f"{base_url}/manifest.json"

        try:
            response = requests.get(manifest_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching manifest.json for {lang}: {e}")
            continue

        manifest = response.json()
        latest_version = manifest["latest"]
        catalog = manifest["catalog"]

        print(f"Available SDK versions for {platform} ({lang}):")
        for v in catalog:
            print(f"- {v}")
        print(f"Latest version: {latest_version}\n")


def download_all_vexos(platform, output_path=None):
    print(
        f"Downloading all available VEXos versions for {platform} is not supported via catalog.txt."
    )
    print("Downloading the latest version instead.")
    download_vexos(platform, output_path=output_path)


def main():
    parser = argparse.ArgumentParser(description="VEX Downloader Script")
    parser.add_argument(
        "-p",
        "--platform",
        required=True,
        choices=["V5", "IQ2", "EXP"],
        help="Platform to download for (V5, IQ2, or EXP)",
    )
    parser.add_argument(
        "-t",
        "--target",
        required=True,
        choices=["os", "sdk"],
        help="Target to download (os or sdk)",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=["python", "cpp", "both"],
        help="Programming language (python, cpp, or both). Required if target is sdk.",
    )
    parser.add_argument("-v", "--version", help="Specify a version to download")
    parser.add_argument("--list", action="store_true", help="List available versions")
    parser.add_argument("-o", "--output", help="Specify output directory or file name")
    parser.add_argument(
        "--all", action="store_true", help="Download all available versions"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    platform = args.platform
    target = args.target
    language = args.language
    version = args.version
    output = args.output
    download_all = args.all

    output_path = None
    output_name = None

    if output:
        if os.path.isdir(output):
            output_path = output
        else:
            output_path = os.path.dirname(output)
            output_name = os.path.basename(output)
            if output_path == "":
                output_path = None

    if target == "sdk" and not language:
        parser.error("Language must be specified when target is sdk.")

    if args.list:
        if target == "os":
            list_vexos_versions(platform)
        elif target == "sdk":
            list_sdk_versions(platform, language)
    else:
        if target == "os":
            if download_all:
                download_all_vexos(platform, output_path=output_path)
            else:
                download_vexos(platform, version, output_path, output_name)
        elif target == "sdk":
            download_sdk(
                platform, language, version, output_path, output_name, download_all
            )


if __name__ == "__main__":
    main()
