# LoadBalancer

This repository contains a simple load balancer implementation in Python using the Flask web framework. It was created to solve the "Load Balancer" coding challenge from [https://codingchallenges.fyi/challenges/challenge-load-balancer](https://codingchallenges.fyi/challenges/challenge-load-balancer) by John Crickett

# Overview
The goal of this project is to implement a load balancer that can distribute incoming requests across a set of target servers. The main components are:

`be.py`: This script simulates a backend server that can be targeted by the load balancer. Multiple instances of this script can be run to represent a group of target servers.

`lb.py`: This script implements the load balancer logic using Flask. It receives incoming requests and forwards them to the target servers in a round-robin fashion.

## How To Run

1. Install `virtualenv`:

```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:

```
$ virtualenv env
```

3. Then run the command (inside the project directory falcon-challenge/):

```
$ source env/bin/activate
```

4. Then install the dependencies:

```
$ (env) pip install -r requirements.txt
```
