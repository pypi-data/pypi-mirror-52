# jira
CLI for jira for its dumb shenannigans

Built on: Python3 and Docker (alpine)<br>
Maintained by: Chris Lee [chris@indico.io]

## Installation

```bash
pip3 install git+ssh://git@github.com/IndicoDataSolutions/jira.git
```

## Using the CLI

#### Prerequisites
To use the CLI you need to install (see above) and add your JIRA_API_TOKEN to the environment.

Follow instructions to [generate an api token](https://confluence.atlassian.com/cloud/api-tokens-938839638.html).
Once you have the token, run the following with your token:

```bash
echo "<email>@indico.io:<token>" | base64
```

Save the output as JIRA_API_TOKEN in your environment.

#### CLI Usage
```bash
jira --help
```

## Getting Started
- Additional Python3 dependencies can be added to requirements.txt<br>
- Tests are located in ./tests <br>
- To run the docker container with the basic requirements, dependencies, and the package installed:
    ```bash
    $ docker-compose up
    ```
