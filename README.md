### Hexlet tests and linter status:
[![Actions Status](https://github.com/danokp/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/danokp/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/02f37d7238f7b255e1aa/maintainability)](https://codeclimate.com/github/danokp/python-project-52/maintainability)
[![Github Actions Status](https://github.com/danokp/python-project-52/workflows/Python%20CI/badge.svg)](https://github.com/danokp/python-project-52/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/02f37d7238f7b255e1aa/test_coverage)](https://codeclimate.com/github/danokp/python-project-52/test_coverage)

# Task manager

Task Manager - a task management system that
allows you to create tasks, assign performers, and change their statuses. 
Registration and authentication are required to work with the system.

## Installation
To download and install this project use the following commands:
```bash
git clone https://github.com/danokp/python-project-52.git
cd python-project-52
```

## Usage
1. Make sure that Docker and Docker-compose are installed.
```bash
docker -v
docker compose version
```
2. Create `.env` file according to example (`.env.example`)
3. Run the application:
```bash
docker compose up # Create docker containers and run docker image.
```
4. Open the application in web browser at [http://localhost:8000](http://localhost:8000).
