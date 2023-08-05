# robostash

This tool was developed to provide and easy way to clone all of the repositories contained
within an Atlassian Bitbucket Project. In the future the ability to push multiple repositories
to an Atlassian Bitbucket Project will also be included. Other platforms (ex. GitHub, GitLab, etc)
may eventually be supported as well.

Currently robostash supports "archive-bb" mode which will create a tarball containing mirror
(bare) copies of all of the Git repositories contained within a single Bitbucket project. The tarball
will be created within your current working directory.

Robostash also supports "archive-list" mode which will create a tarball containing mirror 
(bare) copies of all of the Git repositories listed in a file. The file should be formatted with the
URLs of the repositories to be cloned, one repository per line. This mode currently does not support
providing credentials for cloning the repos. It is assumed they are publicly accessible, ssh keys
or a git-credential store has already been configured. 

## Requirements

* Robostash only supported on Linux
* `python` and `git` installed on the machine that will run `robostash`

## Assumptions

* At this point there is very little error handling. It is up to the user ensure there is sufficient
disk space within the current working directory for cloning and archiving all of the repositories
within the chosen Bitbucket project.

* The created tarball will be named `[project_key].tar.gz` and placed in the current working directory

* If an existing tarball named `[project_key].tar.gz` exists, it will be overwritten without prompt

## Installation

Robostash is on [PyPi](https://pypi.python.org/pypi/robostash)

```bash
pip install robostash
```

## Command-line Arguments

| Argument | Description | Type | Default Value |
|---|---|---|---|
| `-u`,`--user` | Bitbucket username | string | None |
| `-p`,`--password` | Bitbucket password | string | None |
| `-f`,`--credfile` | path to a Bitbucket password file | string | None |
| `-k`,`--key` | Bitbucket project key | string | None |
| `-b`,`--url` | Bitbucket url | string | None |
| `-v`,`--version` | Display program version | N/A | None |
| `-h`,`--help` | Display program help | N/A | None |

## Examples

### Program Invocation

Run the program to archive all of the repos in a Bitbucket project

    robostash archive-bb -u thomas.magnum -p H1ggyBabby -k rmasters -u https://bitbucket.com
    
    robostash archive-bb -u thomas.magnum -f ~/pass -k rmasters -u https://bitbucket.com
    
Run the program to archive a list of repos

    robostash archive-list -r ~/repos -n githubrepos

Run the program to display the version

    robostash -v

Run the program with no arguments or the -h/--help option to display help

    robostash
    robostash -h

## License

MIT

## Contributing

 * Fork it
 * Create your feature branch (`git checkout -b my-new-feature`)
 * Commit your changes (`git commit -am 'Add some feature'`)
 * Push to the branch (`git push origin my-new-feature`)
 * Create new Pull Request

## Building and Distributing
Make sure version numbers are updated in:
 * \_\_init__.py
 * robostash/cli.py
 * setup.py
 * VERSION.md


```bash
virtualenv ~/venv_robostash
source ~/venv_robostash/bin/activate
pip install twine stashy termcolor
git clone https://github.com/dinohead/robostash.git
cd robostash
python setup.py clean
python setup.py check
python setup.py build
python setup.py sdist
twine upload dist/*
```

## Authors

| Author | E-mail | Note |
|---|---|---|
|Derek Halsey|derek@dinohead.com|The OG Jinja Ninja|
