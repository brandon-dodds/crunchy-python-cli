# Crunchy Python CLI
This is going to be a Crunchyroll API application written in python. This isn't going to be a big project so far. You will have to run this in a Linux or Windows command line.

## Prerequisites

In order to get the program running you will need to install these packages.

```
tlslite
requests
youtube-dl
cfscrape
node.js
```
The Python packages can be installed with the following command (delete the "sudo" on Windows):

```
sudo pip3 install -r requirements.txt
```
You will also need to download the crunchyroll API; this can be done with the following command:
```
git clone https://github.com/aheadley/python-crunchyroll && cd python-crunchyroll && python3 setup.py install
```

Node-JS is also needed and can be installed on Debian-based distros with this:
```
sudo apt update
sudo apt install nodejs
```
It can also be installed on Solus with the following command:
```
sudo eopkg update
sudo eopkg install nodejs
```

## Getting Started

In order to get started git clone this project in a directory using the command:
```
git clone https://github.com/subpanda101/CrunchyPythonCLI/
```
You will need to install the packages written in the [requirements.](https://github.com/subpanda101/CrunchyPythonCLI/blob/master/requirements.txt) After you have installed the requirements you can run the base [program.](https://github.com/subpanda101/CrunchyPythonCLI/blob/master/src/mainFunctions.py)

You should open the program with:

```
python3 mainFunctions.py
```

## Command line arguments

When  running the program, certain command line arguments can be passed to obtain different features.
In order to use a command line argument, here is how you would do it in a terminal:
```
crunchypythonapi --(commandLineArgument)
```
If you want to do multiple command line arguments, you would do them as follows:
```
crunchypythonapi --(firstArgument) --(secondArgument)
```

The avaliable command line arguments are:
```
--simulate
```
Program will skip the downloading the file. Used for debugging and testing

```
--auth
```
Will allow user to login with their Crunchyroll accounts to use their queue and gain premium privledges (1080p, Simulcasts, etc.)

```
--queue
```
** Requires --auth be used aswell **
Displays the users Crunchyroll queue (Work in progress)

## Contributors

* **Mar2ck** - *Creator of the project.* - [Mar2ck](https://github.com/Mar2ck)

* **Brandon - Lee Dodds** - *Cool contributor.* - [subpanda101](https://github.com/subpanda101)



See also the list of [contributors](https://github.com/subpanda101/CrunchyPythonCLI/graphs/contributors) who participated in this project.

## Contribution

If you are looking to contribute; remember to read the [contribution file.](https://github.com/subpanda101/CrunchyPythonCLI/blob/master/CONTRIBUTING.md)

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](https://github.com/subpanda101/CrunchyPythonCLI/blob/master/LICENSE) file for details
