PostgreSQL YUM repository:  Build Server Scripts
================================================

## global.sh

This is the core configuration script. All variables are here. Self
documented.

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

## packagebuild.sh:

This is used to build the packages except in non-free repos.
This script must be run with at least two parameters:
        [--beta] [--testing] package name, package version
        and optional: The actual package name to sign, and also the PostgreSQL
        version to build against.

So why do we need to pass two parameters? There are cases where the directory
or software name does not match the package name. A typical example is
`check_pgactivity`. That is the upstream name. However as the other Nagios
packages, it must start with nagios- prefix. So the package name is different.
Another example is PostgreSQL. For historical reasons the directory name is
`postgresql-XY` and the packages start with `postgresqlXY` prefix.
Same for psycopg3.

--beta is used for PostgreSQL's beta releases. --testing is used for upcoming
OS release (like new Fedora or RHEL or SLES release which we build before the
final release.

# gpg-setup-secure.sh: 

Secure GPG agent setup for automated signing. Must be run `once` on each
new build instance. Please follow the output of the script as if all goes well
you'll need to run a command to grab keygrip.

# gpg-bashrc.sh :

Copy this to ~/.bashrc or ~/.pgsql_profile. Make sure you edit it and replace
XXXX's with the actual keygrip.


# cleanbuilddirs.sh

Cleans BUILD and BUILROOT directories. RPM build procedure cleans it under
normal circumstances, but will fail to do so when builds fail. Run this when
there is no build is being done to avoid distruption.

# awsupdateindex.sh

This one utilises [s3indexbuilder.py](https://github.com/mhagander/s3indexbuilder)
to update index.html files on {dnf,zypp}-debuginfo and {dnf-zypp}-srpms repos.
They are served via S3, which does not support indexes, but this script
creates index.html to overcome that problem. Add to cron at 4am so that they
are updated regularly. However my usual best practice is running it manually
right after I finish running packagesync.sh. Since it updates dnf or zypp
sites, run on one RHEL/Fedora instance and another on one SLES instance.
Requires Python >= 3.10, so RHEL 10 and SLES 16 is good there for now.


## packagebuildnonfree.sh:

Same as `packagebuild.sh`, but only for non-free packages. The reason that
I did not unify them is avoid accidentally trying to build non-free packages
on "other" build instances.

## packagesync.sh

Latest version of the script became extremely capable. Run this script without
parameters and see all available options. A few examples:

packagesync.sh --sync="common 18" # Sync only common and v18 repos.
packagesync.sh --sync="pg" # Sync only v18 repos.
packagesync.sh --sync="all" # Sync all packages

packagesync.sh --testing --sync="18" # Sync packages in testing repos.

