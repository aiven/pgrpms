#!/bin/sh

/usr/lib/rpm/perl.req $* | grep -v perl|grep -v python
