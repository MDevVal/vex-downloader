# VEX Downloader

A Python script to download the latest or specific versions of VexOS firmware and SDKs for VEX robotics platforms (V5, IQ2, and EXP).

## Features

- **Download VexOS Firmware:**
  - Download the latest or specific version.
  - Supports platforms: V5, IQ2, EXP.
- **Download SDKs:**
  - Download the latest or specific versions.
  - Supports downloading Python, C++, or both.
  - Option to download all available versions.
- **List Available Versions:**
  - List all available versions for firmware and SDKs.

```
usage: vex-downloader.py [-h] -p {V5,IQ2,EXP} -t {os,sdk} [-l {python,cpp,both}] [-v VERSION] [--list] [-o OUTPUT] [--all]

VEX Downloader Script

options:
  -h, --help            show this help message and exit
  -p {V5,IQ2,EXP}, --platform {V5,IQ2,EXP}
                        Platform to download for (V5, IQ2, or EXP)
  -t {os,sdk}, --target {os,sdk}
                        Target to download (os or sdk)
  -l {python,cpp,both}, --language {python,cpp,both}
                        Programming language (python, cpp, or both). Required if target is sdk.
  -v VERSION, --version VERSION
                        Specify a version to download
  --list                List available versions
  -o OUTPUT, --output OUTPUT
                        Specify output directory or file name
  --all                 Download all available Versions
```
