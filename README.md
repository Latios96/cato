# Cato
Cato is a visual regression testing tool intended for the development of final-frame renderers. Tests produce images, which are compared to pre-defined reference images. The results can be reviewed in a Browser interface:

![](docs/docs_banner.png)

<!-- TOC -->
* [Cato](#cato)
  * [Inspiration](#inspiration)
  * [How does it work?](#how-does-it-work)
    * [Features](#features)
  * [How to use it?](#how-to-use-it)
  * [Installation](#installation)
    * [Prerequisites](#prerequisites)
    * [Install](#install)
  * [Getting started for development](#getting-started-for-development)
  * [Architecture](#architecture)
  * [Design decisions](#design-decisions)
<!-- TOC -->

## Inspiration
Cato is inspired by a similar tool developed internally by Chaos, the developers of V-Ray.
The tool was demonstrated by Vlado Koylazov at "Total Chaos 2019" (see the video of the presentation [here](https://youtu.be/UkvWdr_LhDo?t=2415), presentation slided [here](https://docs.google.com/presentation/d/e/2PACX-1vQyTIC_VpILmmA7kXcXtZVuRKkSbdf0lf-tJYX6vudrRenAEStd-6lHZLjNk4igJDj7O72mneDmygO2/pub?slide=id.g578e9019e1_2_48)).

I really liked the idea of the tool and was looking for something similiar for the development of my own hobby-renderer [Crayg](https://github.com/Latios96/crayg). I couldn't find something similar, so Cato was born.  

## How does it work?
- local config file defining suites and tests
- cato client reads config file, executes tests and uploads the output image and expected reference images to server
- server compares images, returns result
- images and test results are stored on the server for review
- user can inspect test results in browser and compare with reference image, update reference images if needed
### Features

- supports relevant image formats like OpenEXR, PNG or JPEG
- review results in Browser
  - view and compare images using A/B swiping and diff images
  - view all channels of a multichannel OpenEXR file in the browser
  - inspect failed tests and log output of test command
  - filter tests by failure reason
- Edit tests in Browser 
  - Update reference images and comparison settings in the browser
  - edits can be easily synced back locally using CLI, a command to do that can be generated in UI
- distributed test execution on many machines (utilizing external scheduler, currently only Deadline is supported)
- deduplicating file storage (reference and output images are expected to be the same for multiple test runs. Don't store them multiple times)
- Login using Keycloak / OIDC
- Fully automated build using Gradle
- high test coverage using unit and integration tests, also install tests

## How to use it?
1. install client from your running instance using
```shell
pip install {your-instance-url}/static/cato-client-0.0.0-py3-none-any.whl
```
2. create config
3. run config:

- UI Screenshots

## Installation
### Prerequisites
Installation on Linux is recommended

- Postgres DB
- RabbitMq
- Keycloak
- OpenImageIO's `oiiotool` and `iinfo`. Install on Ubuntu with `apt-get -y install openimageio-tools`

### Install
First, grab the Cato server wheel from [Github Releases](https://github.com/Latios96/cato/releases).

After that, you can install the server
```shell
virtualenvn venv
source venv/bin/activate
pip install cato-server-{version}-py3-none-any.whl
# create a server config from template
cato_server_admin config-template
# (edit config and add db connection etc.)
cato_server_admin migrate-db
# start server
cato_server
# in other terminals, start cato_worker: 
cato_worker
# in other terminals, start cato_beat:
cato_beat
```

## Getting started for development 
Backend: Python/ FastAPI
Frontend: Typescript/React

```shell
.\gradlew.bat build
```

## Architecture
![](docs/cato-system-diagramm.svg)

- Cato client: local test execution, reporting to server
- Cato server: Rest API
- Cato Worker: offloaded Image Processing
- Cato Beat: schedule recuring tasks
## Design decisions
- why only `run command` tests
  - ws intended for rendering tests, most renderers have cli interface, spawning a new process for each test is small cost, since rendering task is expected to take longer
- why Gradle
  - fully automated build, just execute build task to
    - install Python deps
    - install Typescript deps
    - run Python Unittests
    - run Typescript Unittests
    - build React app
    - run integration tests
    - build different python wheels for client and server
  - task dependencies
  - cached and multithreaded execution
- Why FastApi?
  - originally flask, but main development on windows
- why rely on external scheduler like Deadline?
  - it's a complicated task (distribute load over multiple machines, restart failed tasks, ignore failing machines, run certain things only on one OS etc. ) Deadline was chosen because I had many experience with running Deadline and developing for it. Can be extended for example to use OpenCue
- why compare images on server (easier client, server side implementation needed anyway for editing reference images in Browser)
- why deduplicating file storage (images are often the same for multiple runs, reference images are always the same if not updated, output images are always the same if they don't involve noise. Save storage space and don't duplicate them). Howevr, current implementation has the issue, that it requires to run on a single machine, so it's currently not possible to run cato_server/cato_worker on different/multiple machines, which is a scaling/availability issue 
- task queue for image processing: can be very slow
- Login using Keycloak / OIDC: Implementing a Login / user managment can be very hard and since it's critical for application security, this is also not a good idea. Keycloak is easy to integrate and advanced login features like two factor authentication etc. just need to be configured and don't need to be implemented 