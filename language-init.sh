#!/bin/bash

pybabel extract . -o locales/testbot.pot
for Item in ru uz;
  do
    pybabel init -i locales/testbot.pot -d locales -D testbot -l $Item
  done