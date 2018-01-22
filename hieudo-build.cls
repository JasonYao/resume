% Intro Options
\ProvidesClass{hieudo-build}[2016/07/26 CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Package Imports
\usepackage[hmargin=1.5cm, vmargin=1.5cm]{geometry}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{babel}
\usepackage[UKenglish]{isodate}
\usepackage{fontspec,xltxtra,xunicode}
\usepackage{fontawesome}
\pagenumbering{gobble}
\usepackage{datetime2}

% Color definitions
\definecolor{date}{HTML}{000000}
\definecolor{primary}{HTML}{000000}
\definecolor{headings}{HTML}{0E0E0F}
\definecolor{subheadings}{HTML}{1A1C1E}

% Set main fonts
\defaultfontfeatures{Mapping=tex-text}
\setmainfont[Color=primary, Path = fonts/NiveauGrotesk/, Scale=1.09]{Niveau-Lig}
\newcommand{\custombold}[1]
{\color{subheadings}\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-ExtraLight}\selectfont #1 \normalfont}
\linespread{1.1}

% Date format
\DTMnewdatestyle{mylastupdate}{%
  \renewcommand*{\DTMdisplaydate}[4]{\DTMtwodigits{##2}.\DTMtwodigits{##3}.##1}\color{date}\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-ExtraLight}\fontsize{10pt}{10pt}\selectfont%
  \renewcommand*{\DTMDisplaydate}{\DTMdisplaydate}%
}

% Name command
\newcommand{\namesection}[2]{
	\hspace{-1.7em}\raggedright{\parbox[b]{30em}{\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Bol}\fontsize{58pt}{0cm}\selectfont #1}}
    \hfill
	% To increase the amount of space available for the links, increment the below's em value
    \raggedleft{\parbox[b]{13em}{\color{headings}\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Lig}\fontsize{11pt}{14pt}\selectfont #2}}
   	\vspace{2.2em}
}

% Section formatting
\titleformat{\section}{\color{headings}
\scshape\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-ExtraLight}\fontsize{18pt}{24pt}\selectfont \raggedright\uppercase}{} {0em}{}
\titlespacing{\section}{0pt}{0pt}{5pt}

% Subsection formatting
\titleformat{\subsection}{\color{subheadings}
\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Bol}\fontsize{14pt}{14pt}\selectfont\bfseries}{}{0em}{}
\titlespacing{\subsection}{0pt}{\parskip}{-\parskip}

% Subsubsection formatting
\titleformat{\subsubsection}{\color{subheadings}
\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Bol}\fontsize{12pt}{12pt}\selectfont\bfseries}{}{0em}{}
\titlespacing{\subsubsection}{0pt}{\parskip}{-\parskip}

% Grouped logic section formatting
\newcommand{\runsubsection}[1]{\color{subheadings}
\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Bol}\fontsize{12pt}{12pt}\selectfont\bfseries {#1} \normalfont}

% Old jobtitle command
%\newcommand{\workplace}[2]{
%\color{subheadings}\raggedright
%\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Bol}\fontsize{12pt}{12pt}\selectfont\bfseries {#1} \normalfont
%\hfill
%\color{subheadings}\raggedleft
%\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Reg}\fontsize{12pt}{12pt}\selectfont\bfseries {#2} \normalfont
%}

% Gives the years & months difference between two dates
% Initial base code from: https://tex.stackexchange.com/questions/14518/difference-between-two-dates/14519#14519
\usepackage{datenumber}
\usepackage{calc}

\newcounter{datetoday}
\newcounter{diffyears}
\newcounter{diffmonths}
\newcounter{diffdays}

\newcommand{\diffdates}[4]{%
      \setmydatenumber{datetoday}{#1}{#2}{01}%
      \setmydatenumber{diffdays}{#3}{#4}{01}%
      \addtocounter{diffdays}{-\thedatetoday}%
      \ifnum\value{diffdays}>0
        \def\diffbefore{in }%
        \def\diffafter{}%
      \else
        \def\diffbefore{}%
        \def\diffafter{ago}%
        \setcounter{diffdays}{-\value{diffdays}}%
      \fi
      \setcounter{diffyears}{\value{diffdays}/365}%
      \setcounter{diffdays}{\value{diffdays}-365*\value{diffyears}}%
      \setcounter{diffmonths}{\value{diffdays}/30}%
      \setcounter{diffdays}{\value{diffdays}-30*\value{diffmonths}}%
      %
      \ifnum\value{diffyears}=0
      \else
          \ifnum\value{diffyears}>1
              \thediffyears\space years,
          \else
              \thediffyears\space year,
          \fi
      \fi
      \ifnum\value{diffmonths}=0
      \else
        \ifnum\value{diffmonths}>1
            \thediffmonths\space months\else\thediffmonths\space month\fi
      \fi
}

% New jobtitle command
\newcommand{\workplace}[3]{
	\subsection{
    {#1}\hfill{\normalfont \bfseries #2 (#3)}
	}
}

% Old position command
%\newcommand{\position}[2]{	\color{subheadings}\raggedright\scshape\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Reg}\fontsize{11pt}{13pt}\selectfont {#1}\normalfont
%\hfill
%\color{subheadings}\raggedleft\scshape\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Reg}\fontsize{11pt}{13pt}\selectfont {#2\\}\normalfont
%}
%\titlespacing{\section}{0pt}{0pt}{3pt}

% New position command
\newcommand{\position}[2]{
	\subsubsection{
		{#1}\hfill{\normalfont \bfseries #2}
	}
}

% Suppresses the subsubsection numbering while keeping it in the ToC
\renewcommand\thesubsubsection{}

% Descriptors command
\newcommand{\descript}[1]{\color{subheadings}\raggedright\scshape\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Reg}\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location command
\newcommand{\location}[1]{\color{primary}\raggedright\fontspec[Path = fonts/NiveauGrotesk/]{Niveau-Reg}\fontsize{11pt}{12pt}\selectfont {#1\\} \normalfont}

% Section seperators command
\newcommand{\sectionsep}[0]{\vspace{8pt}}

% Bullet Lists with fewer gaps command
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}
