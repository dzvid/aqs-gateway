# Air Quality Monitoring System using a Delay and Disruption Tolerant Network 
<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->

<br />
<p align="center">
  <p align="center">
    Backend module
    <br />
    <a href="https://github.com/dzvid/aqs-gateway"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://tukno-aqs-gateway.herokuapp.com/">View Demo</a>
    · -->
    <a href="https://github.com/dzvid/aqs-gateway/issues">Report bug</a>
    ·
    <a href="https://github.com/dzvid/aqs-gateway/issues">Request feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Air Quality Monitoring System using a Delay and Disruption Tolerant Network](#air-quality-monitoring-system-using-a-delay-and-disruption-tolerant-network)
  - [Table of Contents](#table-of-contents)
  - [About the project](#about-the-project)
  - [Built With](#built-with)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
  - [Information about `aqs-ibrdtn` service](#information-about-aqs-ibrdtn-service)
    - [Installation](#installation)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## About the project

Degraded air quality is prejudicial to economy, nature and human lives.  Air quality monitoring is an important task to be performed to alleviate the effects of poor air quality, e.g.: it allows governments to take action on events of high level air pollutants in the atmosphere. It also allows to verify if the actions performed were effective.
Altough important, air quality monitoring is usually neglected, because it is costly, demanding a lot of resources (material, infrastructural, financial and human) to be performed. 
Due to its cost, it is necessary to look for cost-effective options.

<!--
Degraded air quality is prejudicial to economy, nature and human lives.  Air quality monitoring is an important task to be performed to alleviate the effects of poor air quality, but it demands a lot of resources (material, infrastructural , financial and human) to be performed, so its necessary to look for cost-effective options.
Continuous air quality monitoring allows governments to take action on events of high level air pollutants in the atmosphere. It also allows to verify if the actions performed were effective. 
Open access to air monitored data is another important issue necessary to be addressed, it allows population to be aware about the current levels of pollutants and possible effects of it in their lives.
 -->
This repository contains the gateway module of a proposed air quality monitoring system. The gateway module is responsible by convert sensor nodes readings received via DTN and forward it to the REST API. 

Gateway module is composed by two services: 
- `aqs-gateway`: A Python script to get messages received by IBRDTN and forward it to the REST API. It is similar to the work made in the project `fog-over-dtn` ([Fog Node/Gateway DTN-MQTT](https://github.com/netgroup-polito/fog-over-dtn/tree/master/Fog%20Node/Gateway%20DTN-MQTT)), where they implemented a DTN to MQTT gateway. In our case, the code was adapted to a DTN to HTTP gateway and ported to Python `3.6.9`;   
- `aqs-ibrdtn`: IBRDTN service handle communication with the DTN network, receiving messages sent by sensor nodes, these messages are delivered by mules.

Docker Compose is used to create and start both services. 

## Built With

Main technologies, libraries and CLI tools used to built the API:

- [Python](https://www.python.org/): Python is an interpreted, high-level and general-purpose programming language that lets you work quickly;
- [psf/Requests](https://github.com/psf/requests): A simple, yet elegant Python HTTP library;
- [Docker](https://www.docker.com/): Docker containers wrap up software and its dependencies into a standardized unit for software development that includes everything it needs to run: code, runtime, system tools and libraries. This guarantees that your application will always run the same way and makes collaboration as simple as sharing a container image;
- [Docker Compose](https://docs.docker.com/compose/): Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration;

To manage the code style, linting and formatting:

- [black](https://github.com/eslint/eslint)
- [flake8](https://github.com/prettier/prettier)
- [EditorConfig](https://editorconfig.org/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites
 - **Host machine settings**:
    - A host computer running following operational system: `Linux Ubuntu 18.04.5 LTS` or greater; 

      or

    - If deploying services in a Raspberry Pi, use the following operational system: `Raspberry Pi OS (32-bit) Lite, version August 2020 release date 2020-08-20, kernel version 5.4`; 
- **Git**: Git is a free and open source distributed version control system. [Check git download page to get instructions on how to install it](https://git-scm.com/download/linux);
- **Install Docker**: Follow the official [tutorial](https://docs.docker.com/install/). Docker version used in this project: `v19.03.13, build 4484c46d9d`;
- **Install Docker Compose**: Follow the official [tutorial](https://docs.docker.com/compose/). Docker Compose version used in this project: `v1.27.4, build 40524192`.

## Information about `aqs-ibrdtn` service
This service adopts `./ibrdtn/config/flooding/ibrdtn.conf` as configuration for IBRDTN. In this file we defined to store bundles persistently (not in volatile memory) and register logs. Due to these two configurations its necessary to create custom IBRDTN directory on a suitable volume on your host system to mount the volumes defined inside the container.

Make sure that the directories `./ibrdtn/config`, `./ibrdtn/bundles`, `./ibrdtn/log` exists and have correct directory permissions and other security mechanisms on the host system are set up correctly. `aqs-ibrdtn` mounts the following volumes: 
  - `./ibrdtn/config/flooding/ibrdtn.conf:/ibrdtn/config/ibrdtn.conf`: At the moment, `flooding` routing algorithm is adopted in this project. This volume mounts the custom IBRDTN flooding configuration in host to the volume configuration volume in the container;
  - `./ibrdtn/bundles:/ibrdtn/bundles`: custom IBRDTN bundles directory on a suitable volume on your host system to store bundles received from DTN nodes;
  - `./ibrdtn/log:/ibrdtn/log`: custom IBRDTN log directory on a suitable volume on your host system to register logs generated by IBRDTN.
 
### Installation

Docker Compose will be used to install the project:

1. Clone the repository and navigate to the project directory:

   ```sh
   Using ssh:

   git clone git@github.com:dzvid/aqs-gateway.git
   cd aqs-gateway

   Or using https:

   git clone https://github.com/dzvid/aqs-gateway.git
   cd aqs-gateway
   ```

2. Create the `.env` file for the environment variables of the application. Run the following command to create `.env` file using `.env.example` as a template:
    ```sh
    cp .env.example .env
    ```

    In the .env file, set a value for the following environment variables:
   - `API_URL`: URL of the API with the port where the service is running, e.g: `http://127.0.0.1:3000`. It is a required value to be informed so that the Python script can forward data to the API.

   :warning: Make sure values were declared, they are used in the `docker-compose.yml` file to create the services.

3. Create and start the containers using Docker Compose. Open a terminal window and run the following command:

   ```sh
   docker-compose up
   ```

You are done with configuration! I hope everything is alright and the gateway module is running! :tada:

<!-- USAGE EXAMPLES -->

<!-- ## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_ -->

<!-- ROADMAP -->

<!-- ## Roadmap

See the [open issues](https://github.com/dzvid/aqs-gateway/issues) for a list of proposed features (and known issues). -->

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the dev branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

David Oliveira - oliveiradavid.dev@gmail.com

Project Link: [https://github.com/dzvid/aqs-gateway](https://github.com/dzvid/aqs-gateway)

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [Choose an Open Source License](https://choosealicense.com)
- [Img Shields](https://shields.io)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/dzvid/aqs-gateway.svg?style=flat-square
[contributors-url]: https://github.com/dzvid/aqs-gateway/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dzvid/aqs-gateway.svg?style=flat-square
[forks-url]: https://github.com/dzvid/aqs-gateway/network/members
[stars-shield]: https://img.shields.io/github/stars/dzvid/aqs-gateway.svg?style=flat-square
[stars-url]: https://github.com/dzvid/aqs-gateway/stargazers
[issues-shield]: https://img.shields.io/github/issues/dzvid/aqs-gateway.svg?style=flat-square
[issues-url]: https://github.com/dzvid/aqs-gateway/issues
[license-shield]: https://img.shields.io/github/license/dzvid/aqs-gateway.svg?style=flat-square
[license-url]: https://github.com/dzvid/aqs-gateway/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/dzvid