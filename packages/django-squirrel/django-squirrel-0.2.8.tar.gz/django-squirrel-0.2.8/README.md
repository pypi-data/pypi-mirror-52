Squirrel
---

+ **CodeName**: `Katana`
+ **Current version**: `0.2.8.katana.15092019`

**ToC**

+ [Pre-installation](#pre-installation)
    - [Required packages](#required-packages)
    - [RabbitMQ Installation](#install-rabbitmq-server)
    - [RabbitMQ Usage](#rabbitmq-usage)
+ [Installation](#install)
+ [Usage](#usage)
    + [Development](#development)
    + [Production](#production)
+ [Credits](#credits)

# Pre installation 

## Required Packages

```bash
sudo apt update -y && sudo apt install wget git
```
## Install RabbitMQ-Server

Require `Ubuntu 18+`

```bash
# Add repository to repo list
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list

# Add signing-key
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

# Update apt caches and install RabbitMQ-Server 
sudo apt update && sudo apt install rabbitmq-server -y 
```

## RabbitMQ Usage

**Service Management**

```bash
# Enable RabbitMQ Server service
sudo systemctl enable rabbitmq-server

# Start|Stop|Restart RabbitMQ Server service 
sudo systemctl {start|stop|restart} rabbitmq-server

# Disable RabbitMQ Server service
sudo systemctl disable rabbitmq-server
```

_Need more help?, Please see [RabbitMQ OD](https://www.rabbitmq.com/install-debian.html)_

# Install

1) Install Pip Squirrel package 

```
(pyenv) $ pip install django-squirrel
```

2) Install app on django

```python
# /project_name/settings.py

INSTALLED_APPS = [
    '...'
    'squirrel',
]
```

# Usage
## Development

Running `squirrel's workers` development mode

```
# Squirrel run server
python manage.py run_server -v3
```

## Production

Running `squirrel's workers` production mode 

### `run_server` command optional arguments

|   Argument         |     type     |  Description                       |
|:-------------------|:------------:|:-----------------------------------|
| `--port`           | Int          | RabbitMQ Custom Port               |
| `--hostname`       | String       | RabbitMQ Custom Host               |
| `--username`       | String       | RabbitMQ Custom username           |
| `--password`       | String       | RabbitMQ Custom password           |
| `--virtual-host`   | String       | RabbitMQ Custom virtual-host       |
| `--incoming-queue` | String       | RabbitMQ Custom Incoming queue     |
| `--outgoing-queue` | String       | RabbitMQ Custom Outgoing queue     |
| `-v {0,1,2,3}, --verbosity {0,1,2,3}` | *Flag | Logs Verbosity         |

__*__ About Logs: 

+ Minimal: `-v0`
+ Warnings: `-v1` 
+ Information: `-v2` 
+ Debug: `-v3` 

```
# Squirrel run drone
python manage.py run_server [OPTIONAL ARGUMENTS]
```

# Credits

_TODO!_


