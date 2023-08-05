# Metal 🤘

Docker wrapper: Forget about your bare-metal and get started right away.

## Installation

Install [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/) before using metal. Once that's setup, install the metal cli running the following command:

`pip install metal-cli`

## Usage

Get detailed information running `metal --help`.

## Development

Run tests by using `python tests` command.

TODO: update /etc/hosts

### Add mysql user

```sh
metal shell --service="mysql"
mysql -u root --password="secret" -e "CREATE USER '{user}'@'%' IDENTIFIED BY '';"
mysql -u root --password="secret" -e "GRANT ALL PRIVILEGES ON *.* TO '{user}'@'%';"
mysql -u root --password="secret" -e "FLUSH PRIVILEGES;"
```

### Add mysql database

```sh
metal shell --service="mysql"
mysql -u root --password="secret" -e "CREATE DATABASE {database};"
```
