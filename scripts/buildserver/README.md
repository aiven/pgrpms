PostgreSQL YUM repository:  Build Server Scripts
================================================

## dailybuildalpha.sh: 

Add TERM=xterm to the top of the crontab until I add a guard the color definitions in global.sh.

TODO: 
```
if [ -t 1 ]; then
    green=$(tput setaf 2)
    red=$(tput setaf 1)
    blue=$(tput setaf 4)
    reset=$(tput sgr0)
else
    green=""
    red=""
    blue=""
    reset=""
fi
``` 
