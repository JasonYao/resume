# Resume | Jason Yao
[![Build Status](https://travis-ci.org/JasonYao/resume.svg?branch=source)](https://travis-ci.org/JasonYao/resume)

By [Jason Yao](https://github.com/jasonyao/)

> Spending too much time automating the creation of a pretty resume

This repo contains my resume, along with any
necessary files to generate it.

Currently, [LaTeX](https://www.latex-project.org)
is used due to its readability, ease-of-change,
and aesthetic final output.

The LaTeX engine in use is [Xe(La)TeX](http://xetex.sourceforge.net/),
used for its UTF-8 goodness and implicit access to
system-wide fonts.

## Link to Resume
To see the resume, please click the image below:
[![Even this thumbnail is automatically generated](https://www.jasonyao.com/resume/Resume_Jason_Yao.png)
](https://www.jasonyao.com/resume/Resume_Jason_Yao.pdf)

## Install (macOS)
```sh
# Installs pdf generation dependencies
brew cask install mactex
brew tap caskroom/fonts
brew cask install font-fontawesome

# [OPTIONAL] Installs a good pdf viewer and IDE
brew cask install texmaker
```

## Usage
To generate the pdf from the command-line:
```sh
bin/build
# OR
xelatex Resume_Jason_Yao.tex
```

## License
This repo is licensed under the terms of the MIT license,
a copy of which may be found [here](LICENSE)
