#!/bin/sh
# -*- mode: sh; coding: utf-8 -*-

DB_DIR=/tmp/dummy-is-db

rm -fr "$DB_DIR"
mkdir -p  "$DB_DIR"
icebox --Ice.Config=icestorm.cfg



