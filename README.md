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

Find the downloaded files in ./Output.

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

## Buy Me A Coffee! :coffee:

If you can contribute or you want to, feel free to do it at [__Buy me a coffee! :coffee:__](https://www.buymeacoffee.com/starnutoditopo), I will be really thankfull for anything even if it is a coffee or just a kind comment towards my work.

:blush:

**Be careful and donate just if it is within your possibilities, because there is no refund system. And remember that you don't need to donate, it is just a free choice for you. Thank you!**
