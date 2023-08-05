============
pristine-lfs
============

----------------------------------
store pristine tarballs in Git LFS
----------------------------------

:Author: Andrej Shadura <andrew.shadura@collabora.co.uk>
:Date:   2019-06-26
:Version: 20190626.0
:Manual section: 1
:Manual group: Git

SYNOPSIS
========

**pristine-lfs** [-h]

**pristine-lfs** [OPTIONS] **commit** [OPTIONS] (--auto | `tarball`) [`upstream`]

**pristine-lfs** [OPTIONS] **import-dsc** [OPTIONS] `dsc`

**pristine-lfs** [OPTIONS] **checkout** `tarball` [`outdir`]

**pristine-lfs** [OPTIONS] **list** `tarball`

DESCRIPTION
===========

pristine-lfs can store pristine upstream tarballs in Git leveraging Git LFS. Instead of storing the potentially large tarballs within the Git repository as blobs, Git LFS only stores specially prepared metadata in the repository, while storing the actual file contents out of band on a Git LFS server.

Using pristine-lfs allows Debian packages to be built entirely using sources in version control, without the need to keep copies of upstream tarballs.

pristine-lfs supports tarballs compressed with gzip, bzip2, lzma and xz.

Tarball signatures (any files ending with `.asc`) are committed as they are, without utilising the Git LFS mechanisms.

COMMANDS
========

**pristine-lfs commit** [-b `BRANCH`] [-m `MESSAGE`] [--force-overwrite] `tarball` [`upstream`]
   **pristine-lfs commit** stores the specified `tarball` using Git LFS, and commits its metadata to version control.
   The **pristine-lfs checkout** command can later be used to recreate the original tarball based on the information
   stored in Git LFS. The data are not submitted to the server until **git push** command is issued.
   
   The `upstream` parameter is ignored and is supported for compatibility with **pristine-tar**.
   
   If tarball with a different hash has already been committed, it will only be overwritten if `--force-overwrite` is specified.

**pristine-lfs import-dsc** [-b `BRANCH`] [-m `MESSAGE`] [--force-overwrite] [--full] `path-to-dsc`
   Import tarballs and their signatures from a `.dsc` file of a Debian source package.
   
   If `--full` is specified, also imports the Debian packaging and the `.dsc` file itself.
   
   If tarball with a different hash has already been committed, it will only be overwritten if `--force-overwrite` is specified.

**pristine-lfs checkout** [-b `BRANCH`] [-o `outdir`] (--auto | [--full] `tarball`)
   This regenerates a copy of the specified tarball using information previously saved in version control by **pristine-lfs commit**.
   
   By default, the tarball is placed in the current directory. If `outdir` is specified, the file is created in that directory.
   
   If `--auto` is specified, pristine-lfs will consult a file named `debian/changelog`, and if it exists, will check out all tarballs associated with the latest version the changelog mentions.
   
   If `--full` is specified and a `.dsc` file is requested, also checks the Debian packaging and the `.dsc` file itself.

**pristine-lfs list** [-b `BRANCH`]
   This lists tarballs that pristine-lfs is able to checkout from version control.

OPTIONS
=======

-m MESSAGE, --message=MESSAGE  Use the given `MESSAGE` as the commit message for the metadate commits. Applies to **commit** and **import-dsc** commands. `%s` in the commit message is replaced by a comma-separated list of files committed.
-b BRANCH, --branch BRANCH     Branch to store Git LFS metadata on.
-v, --verbose            Be more verbose.
--debug                  Show all sorts of debugging information. Implies ``--verbose``.
-h                       Show this help message and exit.

ENVIRONMENT
===========

**TMPDIR**
    Specifies a location to place temporary files, other than the default.

SEE ALSO
========

**git-lfs**\(1), **pristine-tar**\(1)
