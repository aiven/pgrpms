#!/usr/bin/bash
/usr/lib/rpm/pythondeps.sh $* | grep -v 'venv'|grep -v coffee
