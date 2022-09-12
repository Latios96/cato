# Cato

Cato is a visual regression testing tool intended for the development of final-frame renderers. The results can be
reviewed in a Browser interface.

![](docs/docs_banner.png)

<!-- TOC -->
* [Cato](#cato)
  * [Inspiration](#inspiration)
  * [How does it work?](#how-does-it-work)
    * [Features](#features)
      * [Developer Features](#developer-features)
  * [How to use it?](#how-to-use-it)
  * [Server Installation](#server-installation)
    * [Prerequisites](#prerequisites)
    * [Install](#install)
  * [Getting started for development](#getting-started-for-development)
  * [Architecture](#architecture)
  * [Design decisions](#design-decisions)
<!-- TOC -->

## Inspiration

Cato is inspired by a similar tool developed internally by Chaos, the developers of V-Ray.
The tool was demonstrated by Vlado Koylazov at "Total Chaos 2019" (see the video of the
presentation [here](https://youtu.be/UkvWdr_LhDo?t=2415), presentation
slided [here](https://docs.google.com/presentation/d/e/2PACX-1vQyTIC_VpILmmA7kXcXtZVuRKkSbdf0lf-tJYX6vudrRenAEStd-6lHZLjNk4igJDj7O72mneDmygO2/pub?slide=id.g578e9019e1_2_48))
.

I really liked the idea of the tool and was looking for something similiar for the development of my own
hobby-renderer [Crayg](https://github.com/Latios96/crayg). I couldn't find something similar, so Cato was born.

## How does it work?

A config file defines suites and tests. Each test specifies a command to execute, every command is expected to produce
some kind of image on the file system (output image). The `cato client` reads this config file, executes the tests and
uploads the output image and expected reference images to the `cato server`. The `cato server` compares the images
respecting a per-test threshold and returns the result of the comparison. The server stores the images and test results
for review. The user can inspect the test results in a web interface. Also, reference images can be updated using the
browser interface.

### Features

**Review results in Browser**

- View and compare images using A/B swiping
- View diff images visualizing the error distribution over the image
- View all channels of a multichannel OpenEXR file in the browser
- Inspect failed tests and log output of test command
- Filter tests by failure reason

**Edit tests in Browser**

- Update reference images and comparison settings in the browser
- Edits can be easily synced back locally using CLI, a command to do that can be generated in UI

**Support for relevant image formats**

- OpenEXR
- PNG
- JPEG

**Deduplicating File Storage**

Reference and output images (especially reference images) usually don't change that often over time. It's therefore
obvious to not store them multiple times.

**Easy config files with variable substitution**

See [How to use it?](#how-to-use-it) for an example

**Local and distributed test execution**

- Tests can be executed on a single machine, which is the default.
- It is also possible to distribute the execution using an external scheduler, for
  example [AWS Thinkbox Deadline](https://www.awsthinkbox.com/deadline).
- Currently, only Deadline is supported, but this could be extended to OpenCue for example.

#### Developer Features

- Fully automated build using Gradle
- High test coverage using Unit and Integration tests

## How to use it?

1. install client from your running instance using

```shell
pip install {your-instance-url}/static/cato-client-0.0.0-py3-none-any.whl
```

2. create config
requires oiiotool
```json
{
  "projectName": "oiiotool Demo",
  "serverUrl": "your-instance-url",
  "suites": [
    {
      "name": "Patterns",
      "variables": {
        "oiiotool_command": "oiiotool --pattern {{test_name}} 1280x720 3 -o {{image_output_png}}"
      },
      "tests": [
        {
          "name": "black",
          "command": "{{oiiotool_command}}"
        },
        {
          "name": "constant",
          "command": "{{oiiotool_command}}"
        },
        {
          "name": "fill",
          "command": "{{oiiotool_command}}"
        },
        {
          "name": "checker",
          "command": "{{oiiotool_command}}"
        },
        {
          "name": "noise",
          "command": "{{oiiotool_command}}"
        }
      ]
    }
  ]
}
```

3. run config:

4. Update reference images UI and CLI

- UI Screenshots

## Server Installation

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
virtualenv venv
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
- Cato Beat: schedule recurring tasks

## Design decisions

- Client / server architecture
  alternative: locally created html reports or something similar
  Reasons:
- distributed test execution
- central instance, possible to collect information over multiple runs
- use in CI: view results as they are produced

- why only `run command` tests
    - ws intended for rendering tests, most renderers have cli interface, spawning a new process for each test is small
      cost, since rendering task is expected to take longer
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
    - it's a complicated task (distribute load over multiple machines, restart failed tasks, ignore failing machines,
      run certain things only on one OS etc. ) Deadline was chosen because I had many experience with running Deadline
      and developing for it. Can be extended for example to use OpenCue
- why compare images on server (easier client, server side implementation needed anyway for editing reference images in
  Browser)
- why deduplicating file storage (images are often the same for multiple runs, reference images are always the same if
  not updated, output images are always the same if they don't involve noise. Save storage space and don't duplicate
  them). Howevr, current implementation has the issue, that it requires to run on a single machine, so it's currently
  not possible to run cato_server/cato_worker on different/multiple machines, which is a scaling/availability issue
- task queue for image processing: can be very slow
- Login using Keycloak / OIDC: Implementing a Login / user managment can be very hard and since it's critical for
  application security, this is also not a good idea. Keycloak is easy to integrate and advanced login features like two
  factor authentication etc. just need to be configured and don't need to be implemented 