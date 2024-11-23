#!/bin/sh

cd ./src

taskiq worker common.broker:broker --fs-discover
