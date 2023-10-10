# pgrpms (Aiven fork)

This repo contains Aiven's fork of ["The PostgreSQL RPMs Project"](https://git.postgresql.org/gitweb/?p=pgrpms.git;a=tree).

## Updating the fork

1. Add the upstream `pgrpms` repo to your remotes

        $ git remote add upstream git://git.postgresql.org/git/pgrpms.git

1. It should then be visible in your list of remotes

        $ git remote -v
        origin	git@github.com:aiven/pgrpms.git (fetch)
        origin	git@github.com:aiven/pgrpms.git (push)
        upstream	git://git.postgresql.org/git/pgrpms.git (fetch)
        upstream	git://git.postgresql.org/git/pgrpms.git (push)

1. Fetch changes from the upstream

        $ git fetch upstream

1. Merge `upstream/master` into `main`

        $ git checkout main && git rebase upstream/master

1. Push the changes to `origin/main`

        $ git push
