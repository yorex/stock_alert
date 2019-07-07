#!/bin/bash

ps aux | grep "/usr/bin/flask" | awk '{print $1}'
