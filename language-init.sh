#!/bin/bash
pybabel extract . -o locales/shop-bot.pot
for Item in ru uz en;
  do
    pybabel init -i locales/shop-bot.pot -d locales -D shop-bot -l $Item
  done