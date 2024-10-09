#!/bin/bash

autoflake --remove-all-unused-imports --recursive --in-place src/ --exclude=__init__.py

isort src/*

black src/*
