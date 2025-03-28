# OSA: OPEN-SOURCE ADVISOR

---
## Overview

<overview>

OSA (Open-Source-Advisor) is a LLM-based tool for improving the quality of scientific open source projects and helping create them from scratch. 
It automates the generation of README, different levels of documentation, CI/CD scripts, etc. 
It also generates advices and recommendations for the repository.

OSA is currently under development, so not all features are implemented.
</overview>

---
## How it works?

Here is a short demo:

![Animation](./images/osa_demo.gif)

---

## Table of contents

- [Core features](#core-features)
- [Installation](#installation)
- [Getting started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Citation](#citation)

---

## Core features

<corefeatures>

1. **README file generation**: Automates the creation of a clear and structured README file for a repository, including projects based on research papers.

2. **Documentation generation**: Automatically generates docstrings for Python code.

3. **Automatic implementation of changes**: Clones the repository, creates a branch, commits and pushes changes, and creates a pull request with proposed changes.

4. **Various LLMs**: Use OSA with an LLM accessible via API (e.g., OpenAI, VseGPT), a local server, or try an [osa_bot](https://github.com/osa-bot) hosted on ITMO servers.

</corefeatures>

---

## Installation

Install Open-Source-Advisor using one of the following methods:

**Build from source:**

1. Clone the Open-Source-Advisor repository:
```sh
❯ git clone https://github.com/ITMO-NSS-team/Open-Source-Advisor
```

2. Navigate to the project directory:
```sh
❯ cd Open-Source-Advisor
```

3. Install the project dependencies:

**Using `pip`** &nbsp;
[<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```

**Using `poetry`** &nbsp;
[<img align="center" src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" />](https://python-poetry.org/)

```sh
❯ poetry install 
```

**Using `docker`** &nbsp;
[<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker build -f docker/Dockerfile -t {image-name} .
```

---

## Getting started

### Prerequisites

OSA requires Python 3.10 or higher.

File `.env` is required to specify GitHub token (GIT_TOKEN) and LLM API key (OPENAI_API_KEY or VSE_GPT_KEY)

### Usage

Run Open-Source-Advisor using the following command:

**Using `pip`** &nbsp;
[<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python main.py {repo_url} {api} {model_name}
```

**Using `docker`** &nbsp;
[<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker run --env-file .env {image-name} {repo_url} {api} {model_name}
```

---

## Examples

Examples of generated README files are available in [examples](https://github.com/ITMO-NSS-team/Open-Source-Advisor/tree/main/examples).

URL of the GitHub repository, LLM API service provider (*optional*) and Specific LLM model to use (*optional*) are required to use the generator.

Local Llama ITMO:
```sh
python main.py https://github.com/ITMO-NSS-team/Open-Source-Advisor
```  
OpenAI:
```sh
python main.py https://github.com/ITMO-NSS-team/Open-Source-Advisor openai gpt-3.5-turbo
```
VseGPT:
```sh
python main.py https://github.com/ITMO-NSS-team/Open-Source-Advisor vsegpt openai/gpt-3.5-turbo
```

---

## Documentation

Detailed description of OSA API is available [here](https://itmo-nss-team.github.io/Open-Source-Advisor/).

---

## Contributing

- **[Report Issues](https://github.com/ITMO-NSS-team/Open-Source-Advisor/issues )**: Submit bugs found or log feature requests for the Open-Source-Advisor project.

---

## License

This project is protected under the BSD 3-Clause "New" or "Revised" License. For more details, refer to the [LICENSE](https://github.com/ITMO-NSS-team/Open-Source-Advisor/blob/main/LICENSE) file.

---

## Acknowledgments

The project is supported as ITMO University Research Project in AI Initiative (RPAII).

OSA is tested by the members of [ITMO OpenSource](https://t.me/scientific_opensource) community. Useful content from community 
is available in [**Open-source-ops**](https://github.com/aimclub/open-source-ops)

Also, we thank [**Readme-ai**](https://github.com/eli64s/readme-ai) 
for their code that we used as a foundation for our own version of README generator.

---

## Citation

If you use this software, please cite it as below.

### APA format:

    ITMO, NSS Lab (2025). Open-Source-Advisor repository [Computer software]. https://github.com/ITMO-NSS-team/Open-Source-Advisor

### BibTeX format:

    @misc{Open-Source-Advisor,

        author = {ITMO, NSS Lab},

        title = {Open-Source-Advisor repository},

        year = {2025},

        publisher = {github.com},

        journal = {github.com repository},

        howpublished = {\url{https://github.com/ITMO-NSS-team/Open-Source-Advisor.git}},

        url = {https://github.com/ITMO-NSS-team/Open-Source-Advisor.git}

    }

---
