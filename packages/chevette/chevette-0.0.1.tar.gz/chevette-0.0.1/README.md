Version 0.1.0

# Chevette

Chevette is a static blog engine written in Python. It presently only supports version 3.5 and up.
There are currently no plans to add compatibility to previous versions although efforts from other contributors are most welcome.


_Note: the project is currently an alpha release._
_There are still tests that need to be performed so certain functionality might not be fully stable._

## Installation
Installation is fairly straightforward. Make sure you have either `pip` or `pipenv` installed on your system and run the following command:

```bash
pip install chevette
# or if you are using pipenv
pipenv install chevette
```
---

## Basic Usage

Installing chevette will give you access to a command line utility to help you with your needs.

### Create a blog

It's a simple as executing

```bash
chevette new <path/to/your/project/directory>
```

This will generate a basic boilerplate project for your site (Including template files).

### Build the blog

To build your blog (ie: convert all your markdown posts to html):

1. Navigate to the project directory (if you're not already there)

```bash
cd /path/to/your/project/directory
```
2. Run the `build` command
```bash
chevette build
```
This will generate all the necessary html files (including pages and other assets) and place them in a directory called `public` within the project directory.


### Launch a server
Chevette comes with a very simple http server to help you track the changes you make to your blog.

1. In a new terminal session, navigate to the `public` folder inside of your project directory (see the previous section)

```bash
cd /path/to/your/project/directory/public
```

2. Run the `serve` command
```bash
chevette serve
```

A server will be launched which will be accessible at `localhost:9310`

---

## Roadmap
As I've mentioned in the beginning of this README, chevette is still in its infancy and is very much a work in progress. There are many features I would like to implement, including the following:

* Code syntax highlighting in posts
* A drafts / unpublished mechanism
* Better logging, error messages
* More robust tests
* Add more options to the CLI commands
* Various performance tweakings
* A `publish` command as can be seen in projects like hyde or hugo
* Tidying up the codebase
* Compilation of css and javascript assets
* many more as we think of them


---

## Issues and contributing

If you come across this project and you either feel inclined to add your contribution or simply want to report a bug, the best way to so is through github issues.



