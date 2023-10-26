%%
% Resume | Jason Yao
%
% References:
% 		Debarghya Das (http://debarghyadas.com)
% %

% Intro Options
\ProvidesClass{two-column-resume}[]
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
\usepackage{titlesec}
\usepackage[unicode=true]{hyperref}
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{babel}
\usepackage[UKenglish]{isodate}
\usepackage{fontspec,xltxtra,xunicode}
\usepackage{fontawesome}
\pagenumbering{gobble}
\usepackage{datetime2}
\usepackage{graphicx} % Used to render company logos
\graphicspath{{assets}}

% Color definitions
\definecolor{date}{HTML}{669999}
\definecolor{primary}{HTML}{000000}
\definecolor{headings}{HTML}{0E0E0F}
\definecolor{subheadings}{HTML}{1A1C1E}

% Set main fonts
\defaultfontfeatures{Mapping=tex-text}
\setmainfont[
  Color=primary,
  Path = fonts/IM_Fell_Great_Primer/,
  Scale=1.09,
  BoldFont={../Lora/Lora-Bold} % Relative path hack to get bolds to show
]{IMFeGPrm28P}

% Last updated format
\DTMnewdatestyle{mylastupdate}{%
  \renewcommand*{\DTMdisplaydate}[4]{\DTMtwodigits{##2}.\DTMtwodigits{##3}.##1}\color{date}\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{12pt}{12pt}\selectfont%
  \renewcommand*{\DTMDisplaydate}{\DTMdisplaydate}%
}

% Name command
\newcommand{\namesection}[2]{
	\hspace{-1.7em}\raggedright{\parbox[b]{30em}{\fontspec[Path = fonts/IM_Fell_French_Canon_SC/]{IMFeFCsc28P}\fontsize{58pt}{0cm}\selectfont \MakeUppercase{#1}}}
    \hfill
	% To increase the amount of space available for the links, increment the below's em value
    \raggedleft{\parbox[b]{15em}{\color{headings}\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{11pt}{14pt}\selectfont #2}}
   	\vspace{2.2em}
}

% Section formatting
\titleformat{\section}{\color{headings}
\scshape\fontspec[Path = fonts/Arbutus_Slab/]{ArbutusSlab-Regular}\fontsize{18pt}{24pt}\selectfont \raggedright\uppercase}{} {0em}{}[{\titlerule[0.8pt]}]
\titlespacing{\section}{0pt}{0pt}{5pt}

% Subsection formatting
\titleformat{\subsection}{\color{subheadings}
\fontspec[Path = fonts/Lora/]{Lora-Bold}\fontsize{14pt}{14pt}\selectfont\bfseries}{}{0em}{}
\titlespacing{\subsection}{0pt}{\parskip}{-\parskip}

% Subsubsection formatting
\titleformat{\subsubsection}{\color{subheadings}
\fontspec[Path = fonts/Lora/]{Lora-Bold}\fontsize{12pt}{12pt}\selectfont\bfseries}{}{1em}{}
\titlespacing{\subsubsection}{0pt}{\parskip}{-\parskip}

% Grouped logic section formatting
\newcommand{\runsubsection}[1]{\color{subheadings}
\fontspec[Path = fonts/Lora/]{Lora-Bold}\fontsize{12pt}{12pt}\selectfont\bfseries {#1} \normalfont}

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
	      \ifnum\value{diffmonths}=0
		     Current month start\fi
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

% Workplace display command
\newcommand{\workplace}[4]{
	\subsection{
    \texorpdfstring{{\includegraphics[width=1.25em]{#1}}\thickspace{#2}\hfill{\normalfont #3 (#4)}}{#1}
	}
}

% New position command
\newcommand{\position}[2]{
	\subsubsection{
		{#1}\hfill{\normalfont #2}
	}
}

% Suppresses the subsubsection numbering while keeping it in the ToC
\renewcommand\thesubsubsection{}

% Descriptors command
\newcommand{\descript}[1]{\color{subheadings}\raggedright\scshape\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location command
\newcommand{\location}[1]{\color{primary}\raggedright\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{11pt}{12pt}\selectfont {#1\\} \normalfont}

% Section seperators command
\newcommand{\sectionsep}[0]{\vspace{8pt}}

% Bullet Lists with fewer gaps command
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}

% Sets up hyperlink coloring
\hypersetup{colorlinks=true,urlcolor=blue} % Turns the hyperlinks blue
