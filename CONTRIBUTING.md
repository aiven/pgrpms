# pgrpms (Aiven fork)

This repo contains Aiven's fork of ["The PostgreSQL RPMs Project"](https://git.postgresql.org/gitweb/?p=pgrpms.git;a=tree).

See also
- [RPM Packaging](https://wiki.postgresql.org/wiki/RPM_Packaging)
- [PostgreSQL Yum Repository](https://yum.postgresql.org/)
- [PGDG-RPMs Github mirror](https://github.com/pgdg-packaging/pgdg-rpms/)

## Creating a new pgrpms release

1. **Add the upstream `pgrpms` repo to your remotes**

   ```shell
   git remote add upstream https://git.postgresql.org/git/pgrpms.git
   ```

1. **`upstream` should be visible in your list of remotes**

   ```shell
   git remote -v
   ```

   ```console
   origin  git@github.com:aiven/pgrpms.git (fetch)
   origin  git@github.com:aiven/pgrpms.git (push)
   upstream        https://git.postgresql.org/git/pgrpms.git (fetch)
   upstream        https://git.postgresql.org/git/pgrpms.git (push)
   ```

1. **Fetch changes from origin and upstream**

   ```shell
   git fetch -p --multiple origin upstream
   ```

   ```console
   Fetching origin
   Fetching upstream
   From https://git.postgresql.org/git/pgrpms
    * [new branch]          master     -> upstream/master
   ```

1. **Inspect latest commits from `upstream/master` and choose one commit to release**

   ```shell
   git log --graph --oneline --decorate=short -n5 upstream/master
   ```

   ```console
   * 8190165bc (upstream/master, upstream/HEAD) pg_hint_plan: Adjust license type
   * 1471249b7 pg_cron: Adjust license type
   * 50bae1988 PROJ 9.8: Initial packaging
   * 5e2d1ab2c ODBC: Update to 17.00.0008
   * 22685a0e1 pgdg-srpm-macros: Update to 1.0.53 per changes described at https://github.com/pgdg-packaging/pgdg-srpm-macros/releases/tag/1.0.53
   ```

1. **Create release branch for upstream commit**

   For our running example we use upstream commit `8190165bc` for the
   release.

   ```shell
   git switch -c user.name-release-8190165bc origin/main
   ```

   ```console
   branch 'user.name-release-8190165bc' set up to track 'origin/main'.
   Switched to a new branch 'user.name-release-8190165bc'
   ```

1. **Merge upstream commit into release branch**

   In this step, we will merge upstream commit `8190165bc` into
   release branch `user.name-release-8190165bc`.

   ```shell
   git merge --signoff --compact-summary --no-edit --no-ff 8190165bc
   ```

   ```console
   Merge made by the 'ort' strategy.
   ...
   6935 files changed, 21945 insertions(+), 16960 deletions(-)
   ```

1. **Inspect release branch and confirm that everything is alright**

   Expect that `8190165bc` was merged into
   `user.name-release-8190165bc`:

   ```shell
   git log --graph --oneline --decorate=short -n5
   ```

   ```console
   *   fb0bedacd (HEAD -> user.name-release-8190165bc) Merge commit '8190165bc' into user.name-release-8190165bc
   |\
   | * 8190165bc (upstream/master, upstream/HEAD) pg_hint_plan: Adjust license type
   | * 1471249b7 pg_cron: Adjust license type
   | * 50bae1988 PROJ 9.8: Initial packaging
   | * 5e2d1ab2c ODBC: Update to 17.00.0008
   ```

   Double-check that no files were touched in the merge-commit that
   were previously changed:

   ```shell
   git log --graph --oneline --stat --decorate=short --author="@aiven.io" -m
   ```

   ```
   * fb0bedacd (HEAD -> user.name-release-8190165bc) Merge commit '8190165bc' into user.name-release-8190165bc
   ...
   * a29a36472 Fix pgrpms release runbook
   |  CONTRIBUTING.md | 128 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------
   |  1 file changed, 113 insertions(+), 15 deletions(-)
   * 869d927f4 misc: add aiven readme
   |  CONTRIBUTING.md | 29 +++++++++++++++++++++++++++++
   |  1 file changed, 29 insertions(+)
   * e66a895c7 Revert "misc: add aiven readme"
   |  README.md | 29 -----------------------------
   |  1 file changed, 29 deletions(-)
   * e1c243473 (origin/main, origin/HEAD, main) Merge pull request #2 from aiven/kmichel-allow-group-rx
   * ae0e060ca allow group read/execute in /var/lib/pgsql
      rpm/redhat/main/non-common/postgresql-18/main/postgresql-18-tmpfiles.d | 2 +-
      rpm/redhat/main/non-common/postgresql-19/main/postgresql-19-tmpfiles.d | 2 +-
      2 files changed, 2 insertions(+), 2 deletions(-)
   * 50cdc49f7 misc: add aiven readme
      README.md | 29 +++++++++++++++++++++++++++++
      1 file changed, 29 insertions(+)
   * b898b15ce misc: add aiven readme
      README.md | 29 +++++++++++++++++++++++++++++
      1 file changed, 29 insertions(+)
   ```

   If this were the case, we may need to cherry-pick or replay a
   previous patch again. This could be circumvented with clever tricks
   like patch queues and whatnot, but for now we will depend on human
   intervention.

1. **Push release branch to origin**

   Once the release branch is OK, we push the release branch
   `user.name-release-8190165bc` to remote `origin`.

   ```shell
   git push -u origin user.name-release-8190165bc
   ```

   ```console
   Enumerating objects: 5, done.
   Counting objects: 100% (5/5), done.
   Delta compression using up to 8 threads
   Compressing objects: 100% (4/4), done.
   Writing objects: 100% (4/4), 1.84 KiB | 1.84 MiB/s, done.
   Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
   remote: Resolving deltas: 100% (2/2), completed with 1 local object.
   remote:
   remote: Create a pull request for 'user.name-release-8190165b' on GitHub by visiting:
   remote:      https://github.com/aiven/pgrpms/pull/new/user.name-release-8190165b
   remote:
   To github.com:aiven/pgrpms.git
    * [new branch]          user.name-release-8190165b -> user.name-release-8190165b
   branch 'user.name-release-8190165b' set up to track 'origin/user.name-release-8190165b'.
   ```

1. **Create Github PR**

   Use https://github.com/aiven/pgrpms/pull/new/user.name-release-8190165b

1. **Get a review and let reviewer merge the PR as usual**
