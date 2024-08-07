# OpenFlightMaps downloader

A simple utility to download maps from [OpenFlightMaps](https://www.openflightmaps.org/), based on [Docker](https://www.docker.com/) with [Python 3.9.7 slim buster](https://hub.docker.com/_/python), [Selenium](https://selenium-python.readthedocs.io/index.html) and [ChromeDriver](https://chromedriver.chromium.org/).

# License

View [the LICENSE file](LICENSE).

# Usage

## Build the Docker image

After having cloned or downloaded this repository, in Powershell, cd the project's root directory, then launch:

    docker build -t starnutoditopo/openflightmapsdownloader:1.0.0 .

## Run

After having built the Docker image, in your working folder, create a folder called Output, then launch:

    docker run -it --rm -v "${PWD}/Output:/Output" starnutoditopo/openflightmapsdownloader:1.0.0

**Find the downloaded files in ./Output.**

To get help about other options, specify the **--help** switch:

    > docker run -it --rm starnutoditopo/openflightmapsdownloader:1.0.0 --help
    Usage:
       OpenFlightMapsDownloader.py [-p <partial files directory>] [-o <output directory>] [-t <timeout in seconds>]
          -p <partial files directory> (default: /PartialFiles)
          -o <output directory> (default: /Output)
          -t <timeout in seconds> (default: 120)

### How does it work

This script accesses the [OpenFlightMaps](https://www.openflightmaps.org/) site and emulates a user clicking on all "Download" buttons for maps.
Partial files being downloaded are stored in the /PartialFiles folder. Once each download has finished, the file is moved to its region folder under /Output.

# Develop and debug

This project contains a .devcontainer folder, configured to create a Docker container to be used with Visual Studio Code: just launch VSC and open this folder in container.

For your convenience, create a .vscode/launch.json file with a content like this:

    {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "/workspaces/OpenFlightMapsDownloader/OpenFlightMapsDownloader.py",
                "console": "integratedTerminal",
                "args": [
                    "-o", "./Output"
                ]
            }
        ]
    }

Open the OpenFlightMapsDownloader.py file and press the F5 key to start debugging.
