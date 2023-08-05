import argparse
import getpass
import os
import shutil
import stashy
import sys
import tempfile
from termcolor import colored
import urllib

# fix the ascii error, from:
# http://mypy.pythonblogs.com/12_mypy/archive/1253_workaround_for_python_bug_ascii_codec_cant_encode_character_uxa0_in_position_111_ordinal_not_in_range128.html
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf8")

# read input parameters
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description="""
ROBOSTASH!

This tool was developed to provide and easy way to clone all of the repositories contained
within an Atlassian Bitbucket Project. In the future the ability to push multiple repositories
to an Atlassian Bitbucket Project will also be included. Other platforms (ex. GitHub, GitLab, etc)
may eventually be supported as well.

Currently robostash only supports "archive" mode which will create a tarball containing mirror
(bare) copies of all of the Git repositories contained within a single Bitbucket project. The tarball
will be created within your current working directory.

examples:
  Run the program to archive all of the repos in a Bitbucket project
    robostash archive -u thomas.magnum -p H1ggyBabby -k rmasters -u https://bitbucket.com
    
    robostash archive -u thomas.magnum -f ~/pass -k rmasters -u https://bitbucket.com
    
  Run the program to archive a list of repos
    robostash archive-list -r ~/repos -n githubrepos
    
  Run the program to display the version
    robostash -v
    
  Run the program with no arguments or the -h/--help option to display help 
    robostash -h

""")

# going to create our own groups so they show up in correct order in help
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')

# required arguments
required.add_argument('mode', type=str, help='Specify stashbot action. Valid actions: archive-bb, archive-list')

# optional arguments
# TODO: always update VERSION number, it is right ---------------------------->HERE!<
optional.add_argument('-v', '--version', action='version', version='robostash - v0.2.0 Higgins')
optional.add_argument('-p', '--password', help='Bitbucket password\n  example: H1ggyBabby')
optional.add_argument('-f', '--credfile', help='path to a Bitbucket password file\n')
optional.add_argument('-u', '--user', help='Bitbucket username\n  example: thomas.magnum')
optional.add_argument('-k', '--key', help='Bitbucket project key\n  example: rmasters')
optional.add_argument('-b', '--url', help='Bitbucket url\n  example: https://bitbucket.com')
optional.add_argument('-r', '--repolist',
                      help='File containting list of repositories to archive\n  example: /home/magnum/repos')
optional.add_argument('-n', '--aname', help='Filename to use when creating archive\n  example: github')

args = parser.parse_args()

# get the current working directory
os_path = os.getcwd()

def main():
    if args.mode == "archive-bb":
        # fail if no user was provided
        if args.user is None:
            print (colored("You must specify user using -u or --user in archive-bb mode\n", 'red', attrs=['bold']))
            exit(1)

        # fail if no url was provided
        if args.url is None:
            print (colored("You must specify url using -b or --url in archive-bb mode\n", 'red', attrs=['bold']))
            exit(1)

        # fail if no key was provided
        if args.key is None:
            print (colored("You must specify key using -k or --key in archive-bb mode\n", 'red', attrs=['bold']))
            exit(1)

        # If a password or credfile path was not provided, prompt for password.
        if args.password is not None:
            stash_password = args.password
        elif args.credfile is not None:
            password_file = open(args.credfile, "r")
            password_line = (password_file.readline())
            stash_password = (password_line.split()[0])
            password_file.close()
        else:
            stash_password = getpass.getpass("Password: ")

        # create temporary directories and change working directory
        tmp_dir = tempfile.mkdtemp(prefix="rstash_", dir=os_path)
        arch_dir = os.path.join(tmp_dir, args.key)
        os.mkdir(arch_dir)
        os.chdir(arch_dir)

        # create a stash object
        print (colored("connecting to Bitbucket\n", 'white', attrs=['bold']))
        stash = stashy.connect(args.url, args.user, stash_password)
        try:
            stash.projects.list()
        except:
            print (colored("connecting to Bitbucket : ", 'white', attrs=['bold']) + colored("Failed\n", 'red',
                                                                                            attrs=['bold']))
            shutil.rmtree(tmp_dir, ignore_errors=True)
            exit(1)
        else:
            print (colored("connecting to Bitbucket : ", 'white', attrs=['bold']) + colored("Success\n", 'green',
                                                                                            attrs=['bold']))

        # query bitbucket api for a list of repos, iterate, and clone
        for repo in stash.projects[args.key].repos.list():
            for url in repo["links"]["clone"]:
                if url["name"] == "http":
                    print (colored("cloning : ", 'white', attrs=['bold']) + colored(repo["name"], 'blue',
                                                                                    attrs=['bold']))
                    url = url["href"][:8] + args.user + ':' + urllib.quote(stash_password, safe='') + \
                        '@' + url["href"][8:]
                    try:
                        os.system("git clone --mirror {0}".format(url))
                    except:
                        print (colored("cloning : ", 'white', attrs=['bold']) + colored("Failed\n", 'red',
                                                                                        attrs=['bold']))
                        break
                    else:
                        print (colored("cloning : ", 'white', attrs=['bold']) + colored("Success\n", 'green',
                                                                                        attrs=['bold']))
                    break

        # compress project
        print (colored("creating archive\n", 'white', attrs=['bold']))
        arch_name = args.key + '.tar.gz'
        os.chdir(tmp_dir)
        os.system("tar -czf {0} {1}".format(arch_name, args.key))
        os.rename(os.path.join(tmp_dir, arch_name), os.path.join(os_path, arch_name))
        print (colored("creating archive : ", 'white', attrs=['bold']) + colored("Success\n", 'green', attrs=['bold']))

        # remove temporary directory
        print (colored("cleaning up\n", 'white', attrs=['bold']))
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except:
            print (colored("cleaning up : ", 'white', attrs=['bold']) + colored("Failed\n", 'red', attrs=['bold']))
        else:
            print (colored("cleaning up : ", 'white', attrs=['bold']) + colored("Success\n", 'green', attrs=['bold']))

    elif args.mode == "archive-list":
        # fail if no repolist was provided
        if args.repolist is None:
            print (colored("You must specify a repolist using -r or --repolist in archive-list mode\n", 'red',
                           attrs=['bold']))
            exit(1)

        # fail if no archive name was provided
        if args.aname is None:
            print (colored("You must specify an archive name using -a or --aname in archive-list mode\n", 'red',
                           attrs=['bold']))
            exit(1)

        # create temporary directories and change working directory
        tmp_dir = tempfile.mkdtemp(prefix="rstash_", dir=os_path)
        arch_dir = os.path.join(tmp_dir, args.aname)
        os.mkdir(arch_dir)
        os.chdir(arch_dir)

        with open(args.repolist) as f:
            for line in f:
                print (colored("cloning : ", 'white', attrs=['bold']) + colored(line, 'blue', attrs=['bold']))
                try:
                    os.system("git clone --mirror {0}".format(line))
                except:
                    print (colored("cloning : ", 'white', attrs=['bold']) + colored("Failed\n", 'red', attrs=['bold']))
                    break
                else:
                    print (colored("cloning : ", 'white', attrs=['bold']) + colored("Success\n", 'green',
                                                                                    attrs=['bold']))

        # compress project
        print (colored("creating archive\n", 'white', attrs=['bold']))
        arch_name = args.aname + '.tar.gz'
        os.chdir(tmp_dir)
        os.system("tar -czf {0} {1}".format(arch_name, args.aname))
        os.rename(os.path.join(tmp_dir, arch_name), os.path.join(os_path, arch_name))
        print (colored("creating archive : ", 'white', attrs=['bold']) + colored("Success\n", 'green',
                                                                                 attrs=['bold']))

        # remove temporary directory
        print (colored("cleaning up\n", 'white', attrs=['bold']))
        try:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except:
            print (colored("cleaning up : ", 'white', attrs=['bold']) + colored("Failed\n", 'red',
                                                                                attrs=['bold']))
        else:
            print (colored("cleaning up : ", 'white', attrs=['bold']) + colored("Success\n", 'green',
                                                                                attrs=['bold']))

    else:
        print (colored(args.mode + " is not a valid command", 'red',
                       attrs=['bold']))

if __name__ == "__main__":
    main()
