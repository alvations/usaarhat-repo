Note: The following instructions work on Ubuntu 14.04 !!!! Type the commands LINE BY LINE

**Gitting the repository from github**

Go to your home directory, typing `cd` will automatically move you to the home directory:

```
cd
cd ~
```

Note that the `cd ~` brings you to the same home directory. The `~` is a shortcut for your home directory. It doesn't work in all circumstances so I normally avoid it when scripting.

Now see whether you have git on your machine, type the following on your machine:

```
cd
git
```
You should see the following lines to the instructions to use git:

```
usage: git [--version] [--help] [-C <path>] [-c name=value]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]

```
If you don't see the above type:

```
sudo apt-get install git
```

After installing git on your computer, do:

```
git clone https://github.com/alvations/usaarhat-repo.git
```

Then do:

```
ls
```

You will now see `usaarhat-repo` in the list of files/directories you have.

----

**Installing Moses on your machine**

The `momo.sh` file automatically installs Moses toolkit on an Ubuntu 14.04 machine. 

Type the following command to copy the `momo.sh` file to your home directory. But first go into the `usaarhat-repo` directory:

```
cd
cd usaarhat-repo
cp momo.sh ..
cd
ls
```

`cp momo.sh ..`  copies the `momo.sh` file to the parent directory in this case the parent directory is the home directory. Now you will see `momo.sh` in your home directory, i.e. `~`.

To install moses, simply type the following:

```
cd
momo.sh
```

Wait for the installation to end and you should see the following as the last two lines:

```
this is a small house
this is a small house
```

If you did not see the above lines at the end of installation. Go to http://www.statmt.org/moses/?n=Development.GetStarted and see whehter there is a solution to your problem, if not consult the Moses developers from the mailing list (http://www.statmt.org/moses/?n=Moses.MailingLists)

----

Move on to `Meet-Moses.md` : https://github.com/alvations/usaarhat-repo/blob/master/MeeT-Moses.md
