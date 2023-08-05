# Blender Web Assets
Blender Web Assets is a front-end framework which provides design and interactivity components for official [Blender.org websites](http://www.blender.org).

## Install and usage
### Software you need
* **[git](http://git-scm.com)** To clone and contribute to this repository you need Git. Install from here: http://git-scm.com/downloads.
* **[Sass](http://sass-lang.com)** Our CSS preprocessor is SASS. If you don't have it installed, follow the step by step guide on their website: http://sass-lang.com/install.
* **[NODE.JS](http://nodejs.org)** We use Node.js to power gulp to run repetitive tasks like prefixing CSS. Make sure, that you have Node.js installed on your system. Download from here: http://nodejs.org/download or install via a package manager: http://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager.

### Setup
1. Open up your terminal.
2. Clone this repository with `git clone git://git.blender.org/blender-web-assets.git`.
3. Navigate to this project using `cd /path/to/blender-web-assets`.
4. Do `npm install -g gulp` to install gulp globally (you maybe have to run this command as root).
5. Run `npm install`
6. `gulp` will compile and prefix the Sass. Additionally, `gulp watch` will keep gulping when there are changes in the source files.

## Usage
Now you can type `gulp` in the terminal every time you need the Sass compiled to `css/main.css`. Open [index.html](index.html) to review your changes.

### As a git submodule
The whole concept of Blender Web Assets is to be shared between official Blender projects.

Clone, initalize, and update:
1. `git clone git://git.blender.org/blender-web-assets.git`
2. `git submodule init`
3. `git submodule update --remote`

Then in each project you can just `import` via Sass the components you need from BWA.

Each project must have a working gulp pipeline (`package.json` and `gulpfile.js`), most dependencies are covered in BWA's `package.json`.

## Demo
See BWA in action:

* [blender.org](https://www.blender.org)
* [code.blender.org](https://code.blender.org) (extending the blender.org theme)
* [Blender ID](https://id.blender.org)
* [Blender Conference](https://www.blender.org/conference)
* [Blender Open Data](https://opendata.blender.org/)
* [Blender My Data](https://mydata.blender.org/)


## Authors
[Pablo Vazquez](http://developer.blender.org/p/pablovazquez)
[Niklas Ravnsborg-Gjertsen](http://developer.blender.org/p/niklasravnsborg)

## Copyright and license
This project is licensed under [the GPL license](LICENSE) copyright © 2019 Blender Foundation.
