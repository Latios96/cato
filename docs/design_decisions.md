
## Design Decisions

### Client / Server Architecture

A Client / Server Architecture was chosen for the following reasons. An alternative would have been a locally created HTML report os something similar.

- Editing of reference images / comparison settings
  - Would also be possible with a local solution, but this would also require some kind of backend 
- Distributed test execution
  - easy to collect results using a central instance.
- Easily collect information over multiple runs
- Run tests in CI: view results as they are produced
- Easily share run results (just copy link)

### Serving the Frontend from Cato Server

Serving the Frontend from `cato server` means that only one Python wheel needs to be installed and started, which greatly simplifies deployment.

### Gradle

While Gradle is quite common in the Java world, not many people would expect that in a Python / Typescript project. However, I wanted a fully automated build. Executing the build task will do:
    - install Python deps
    - install Typescript deps
    - run Python Unittests
    - run Typescript Unittests
    - build React app
    - run Integration tests
    - build different Python wheels for client and server

With Gradle, it's possible to define dependencies between tasks, so all dependent tasks are also executed when executing one task. The task results are also cached and when no inputs to the task changes, the task is not executed again. Also, the tasks are executed in parallel if possible.


### Why relying on external scheduler like Deadline

Developing a scheduler is a complicated task with many challenges, for example:
- a system that scales to _many_ machines
- distribute load over multiple machines
- restart failed tasks
- ignore failing machines
- run certain things only on one OS

Deadline was chosen because I had many experience with running Deadline and developing for it. There are no restrictions to extended Cato to use OpenCue, for example.

### Comparing Images on Server

Images are compared on the server to make the client smaller and easier to distribute. Otherwise, this would currently require to install OpenImageIO on any client machine, which is challenging, since there are no public Windows builds available. Also, a server side implementation was needed anyway for editing reference images in Browser.

### Deduplicating File Storage

Images are often the same for multiple runs:
- Reference images are always the same if not updated
- output images are most of the time the same, they are only different if a test fails or they involve some kind of noise

To save storage space, they are deduplicated by checksum and only stored once.

### Using a task queue for image processing

Image processing can be quite slow, which can lead to HTTP request timeouts otherwise.

### Login using Keycloak / OIDC

Implementing a Login / user managment can be very hard and since it's critical for application security, this is also
not a good idea. Keycloak is ready to use and easy to integrate. Advanced login features (for example Two-Factor-Authentication) just need to be configured and don't need to be implemented. 