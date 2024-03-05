# OpenAPI

## Overview

The API/SDK team is working to standardize OpenAPI as the way we spec APIs at Smartsheet.  Our goal is to create a single source of truth for all API information in a standard format.  We will be building tooling on top of these specs starting with API reference document generation but potentially including more in the future.

This page outlines the recommended tools and process for authoring OpenAPI specs at Smartsheet. Please send any feedback or questions to the [#askus-openapi](https://smartsheet.slack.com/archives/CSNLSQE8J) Slack channel.

## Resources

| Resource | Location |
| :---------| :----------- |
| OpenAPI 3.0.3 Specification | https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md |
| Mirror spec (with TOC/ more usable | https://swagger.io/specification/ |
| Examples | https://github.com/OAI/OpenAPI-Specification/tree/master/examples/v3.0 |
| Redoc (overall project) | https://github.com/Redocly/redoc |
| Redoc cli | https://github.com/Redocly/redoc/blob/master/cli/README.md |
| Tooling | https://github.com/OAI/OpenAPI-Specification/blob/master/IMPLEMENTATIONS.md |

## Authoring Tools Recommendations

OpenAPI Specs are standard YAML files. As such, any text editor can be used to author them. Many ideas have plugins that will help author YAML files and/or OpenAPI Spec files specifically. 

Currently, we recommend the following for authoring:

* IntelliJ IDEA (Paid or Free Community Edition)
  * [OpenAPI Editor plugin by semonte](https://plugins.jetbrains.com/plugin/12887-openapi-editor) (30 day Trial then $25/year)
* Visual Studio Code
  * [OpenAPI (Swagger) Editor plugin by 42Crunch](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) (Free)

Please note that our CI/CD pipeline applies many additional modifications to our OpenAPI spec that these preview editors will not display.


## OpenAPI Spec Repo Information

### Repo

Make a branch off Develop in this repo to add new content.

### File Layout

To facilitate re-use of components our OpenAPI spec is broken up into multiple files. This also makes it easy to identify the exact object or path that needs editing updating without going through a file that is several thousand lines long.

* openapi/openapi.yaml - This is the root OpenAPI file that links to everything else.  Our tools will start by processing this file and will follow references to pull everything else in. Do not add files to this folder.
* openapi/paths/* - Each file here represents a set of operations (API Calls) against a specific endpoint. An endpoint is defined by the URL that would receive the API call without any query parameters. Examples: /webhooks, /webhooks/&lt;id&gt;, /webhooks/&lt;id&gt;/resetsharedsecret. Each file should define a unique path with all operations (GET / POST / PUT / DELETE) for that endpoint defined in that file. Files should be named <path>.yaml. To avoid issues with invalid characters in file names: "/" character should be replaced with "~1"; parameters in paths should be surrounded with braces "{}"; example: The file containing the path: "webhooks/<webhookId>" would be called "webhooks~1{webhookId}"
* openapi/components/* - This folder contains other folders which define schema objects (resources, parameters, properties, etc.). Do not add files to this folder.
* openapi/components/schemas - This folder contains definitions for the Objects exposed by our APIs. In general, it is one Object per file.  Exceptions may include creating an array of the Object for later reuse. File should be named for the Object it defines.
* openapi/components/parameters - This folder contains definitions for shared parameters - parameters that are used across multiple paths and methods. Each file contains a single parameter definition and is named for the parameter.	
* openapi/components/properties - This folder contains definitions for shared properties - properties that are used across multiple objects.  Each file contains a single property definition and is named for the property.

## Authoring Guidance

Many tools that consume or author OpenAPI specs only support a single monolithic yaml file. Because out API is so extensive, this is not desirable from an authoring/maintenance standpoint. Our solution is to treat each individual yaml file as a standalone OpenAPI specification, and then using tooling to merge these specs together into a single monolith for external consumption. This does create some extra overhead, but allows for an easier authoring experience overall.

### File Naming

Use camel-case when naming component files. For Objects, start with an Uppercase letter, lowercase for parameters and properties:

* schemas (objects) - Object.yaml
* parameters - parameterName.yaml
* properties - propertyName.yaml

When naming path files the file name should be the path replacing "`/`" with "`~1`" and "`()`" with  "`{}`" (omit the leading "`/`"):

* objects~1{objectId}~1subObject

For images, use the word "external" or "internal" in the image name to get it to the correct place. External images will display in both external and internal documents. Internal images will only display in internal documents. 

### Info Section

OpenAPI specs must have an `info` section to be valid. Because each file is treated as its own spec, this info section must be filled out for each file. However, when the full spec is compiled, only the root info folder will be used (that is, the section found in the core openapi.yaml file will be shown, the sub-file info sections will be omitted). This allows us to provide team ownership and other details about the component.

Please provide the following properties in each `info` section:
* **title** - A title that makes organizational sense for your team
* **description**: A brief summary of the function this file provides.
* **version**: Major.Minor.Revision format version number. Note that while our full API is currently pegged to 2.0.0, your component can follow its own version scheming. It is suggested you start with 1.0.0.
* **x-smar-ownership**: The team or pillar responsible for ownership of this component. (This is a custom extension, your IDE will not warn you if this is missing. It is, however, required.)

### Versioning

All files should target the latest stable version of OpenAPI: 3.0.3

### Easier Cross-File Schema Referencing

Not necessary but a tip.

If you are referencing components from other components or paths, consider "double referencing."  Declare the remote file reference once in the "components" section and then in the rest of the file to locally reference it. This means if the referenced file ever changes you only need to update one remote reference instead of all of them. 

See /paths/webhooks.yaml for an example of this.

### Writing Good Component Files

Some tips for getting it done fast and well:

* Declare property names and types first - that's the minimum you need for a valid file.
  - Add them in alphabetical order please
* Go back and add details for types:
  - Default values wherever you know it, especially for boolean
  - Min/Max values if you know it
  - Format if it has it- https://swagger.io/specification/#data-types
* Finally, add description and examples
  - Copy description from existing docs; markdown works in description if needed
  - Add an example if it improves the auto-generated one by Redoc/SwaggerUI

### Verifying Correctness

If you're able to do this please do.

Smartsheet has never had any automation between code and documentation, so we'll need to do the following:

* Verify default settings (are booleans preset in an object, are there min/max values allowed)
* Validate the object against code (is what's in the documentation actually what you get in a Postman call)

### Copy Other's Work

Check out the Webhooks files for decent examples of how to get started.

## Docker

A Docker configuration is provided for you to easily setup and manage the Speccy linter and ReDoc CLI. There are also
IntelliJ Run Configurations provided which will launch a script to deploy your current file revisions to the Docker 
container and launch the build pipeline with various options. The Docker container contains a Flask development web 
server so that you can view the finished product directly in a browser. The Flask server will be available at 
http://localhost:8000/ once the API documentation has been built.

To use Docker:

1. Open a Terminal Window and navigate to the root directory of the OpenAPI repository.
2. Launch the container with `docker-compose -f docker-compose.yml up -d`. NOTE if you are setup to develop app-core 
use the `-f docker-compose.yml` argument so that `docker-compose` operates against the compose file in the OpenAPI 
repository (not the one in the app-core repository). The first launch will take some time (about 5 minutes) to pull 
container images and install the pipeline components.
3. Do one of the following:
   * If you have Bash, make your edits and then select the `Docker - Full Build & Deploy` run configuration from IntelliJ. If all goes well 
   you should see output such as example below indicating that the finished product is accessible via the browser. If your 
   script contains errors, you will see the error output from the linter.
   * If you don't have Bash, you can manually run the script with 'scripts/docker_deploy.sh'
5. You can stop the Docker container with `docker-compose -f docker-compose.yml down`.

If port 8000 is already in use, define the `REDOC_PORT` environment variable to the port you'd like to use.

### Successful Deploy
```bash
Specification is valid, with 0 lint errors
Resolved to speccy_openapi.yaml
Prerendering docs

🎉 bundled successfully in: redoc-static.html (22049 KiB) [⏱ 2.531s]
OK
Prerendering docs

🎉 bundled successfully in: redoc-static.html (22049 KiB) [⏱ 2.586s]
OK
View Smartsheet API documentation here: http://localhost:8000

Process finished with exit code 0
```

### Unsuccessful Deploy

```bash
Specification schema is invalid.

#/info
expected Object {
  title: 'Smartsheet API Reference',
  versison: '2.0.0',
  contact: Object { email: 'admin@smartsheet.com' }
} to have key version
	missing keys: version
Specification has errors

Process finished with exit code 1
```
