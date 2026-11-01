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
\usepackage[dvipsnames]{xcolor}
\usepackage{titlesec}
\usepackage[unicode=true,pdfpagelabels=false]{hyperref}
\usepackage{bookmark}
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{babel}
\usepackage[UKenglish]{isodate}
\usepackage{fontspec,xltxtra,xunicode}
\usepackage{fontawesome7}
\pagestyle{empty}
\usepackage{datetime2}
\usepackage{graphicx} % Used to render company logos
\usepackage{tikz}
\pgfdeclarelayer{resumeBackground}
\pgfdeclarelayer{resumeHeader}
\pgfdeclarelayer{resumeColumns}
\pgfdeclarelayer{resumeForeground}
\pgfsetlayers{resumeBackground,resumeHeader,resumeColumns,main,resumeForeground}
\providecommand{\resumeLayerPreview}{composite}
\def\resumeCompositeLayer{composite}
\def\resumeBackgroundLayer{background}
\def\resumeHeaderLayer{header}
\def\resumeColumnsLayer{columns}
\def\resumeForegroundLayer{foreground}
\newcommand{\resumeiflayer}[2]{%
  \ifx\resumeLayerPreview\resumeCompositeLayer
    #2%
  \else
    \ifx\resumeLayerPreview#1 #2\fi
  \fi
}
\graphicspath{{assets}}

% Color definitions
\definecolor{date}{HTML}{669999}
\definecolor{primary}{HTML}{000000}
\definecolor{headings}{HTML}{0E0E0F}
\definecolor{subheadings}{HTML}{1A1C1E}
\definecolor{floralblue}{HTML}{2456C4}

\newcommand{\drawfloral}[1]{%
  \begin{scope}[scale=#1,draw=floralblue!75,fill=floralblue!32]
    \foreach \angle in {0,72,144,216,288} {
      \fill[rotate around={\angle:(0,0.62)}] (0,0.74) ellipse [x radius=0.07cm,y radius=0.16cm];
    }
    \fill[floralblue!70] (0,0.62) circle [radius=0.045cm];
    \draw[line width=0.65pt] (0,0) .. controls (0.03,0.15) and (-0.03,0.3) .. (0,0.5);
    \fill[rotate around={-35:(0,0.28)}] (0,0.28) ellipse [x radius=0.06cm,y radius=0.14cm];
    \fill[rotate around={35:(0,0.14)}] (0,0.14) ellipse [x radius=0.06cm,y radius=0.14cm];
  \end{scope}
}

\newcommand{\drawresumeLeaf}[4]{%
  \begin{scope}[shift={(#1,#2)},rotate=#3,scale=#4]
    \path[fill=floralblue!28,draw=floralblue!65,line width=0.45pt]
      (0,0) .. controls (0.12,0.22) and (0.12,0.48) .. (0,0.68)
      .. controls (-0.12,0.48) and (-0.12,0.22) .. cycle;
    \draw[floralblue!65,line width=0.35pt] (0,0) -- (0,0.61);
  \end{scope}
}

\newcommand{\drawresumeFlowers}{%
  \begin{scope}[shift={([xshift=-1.5cm,yshift=1.2cm]current page.south east)}]
    \draw[floralblue!70,line width=1.15pt]
      (0,0) .. controls (-1.2,2) and (-0.5,4) .. (-2.7,5.8)
      .. controls (-4.3,7.1) and (-2.8,9) .. (-5.6,10.6)
      .. controls (-8.2,12.2) and (-4.6,13.2) .. (-6.2,15.2)
      .. controls (-7.7,17.1) and (-10.2,17.2) .. (-10.8,19.1)
      .. controls (-11.6,21) and (-10.1,22.2) .. (-12.8,23.3);

    \draw[floralblue!65,line width=0.9pt] (-2.4,5.5) .. controls (-0.5,6.1) and (0.1,7.4) .. (-0.1,9.2);
    \draw[floralblue!65,line width=0.9pt] (-2.6,6) .. controls (-4.2,5.2) and (-5.8,4.9) .. (-7.6,5.2);
    \draw[floralblue!65,line width=0.9pt] (-4.8,9.8) .. controls (-3.1,10.9) and (-2.4,12.2) .. (-2.7,14);
    \draw[floralblue!65,line width=0.9pt] (-5.8,10.5) .. controls (-7.4,9.1) and (-9.1,8.8) .. (-11.2,9.4);
    \draw[floralblue!65,line width=0.9pt] (-6.2,14.9) .. controls (-4.5,15.7) and (-3.1,16.7) .. (-2.5,18.3);
    \draw[floralblue!65,line width=0.9pt] (-7.3,16.5) .. controls (-9.2,15.9) and (-11.2,16.1) .. (-13.3,17.2);
    \draw[floralblue!65,line width=0.9pt] (-10.7,18.8) .. controls (-9,19.1) and (-7.4,20.1) .. (-6.5,21.8);

    \drawresumeLeaf{-0.5}{2.4}{-48}{1}
    \drawresumeLeaf{-1.6}{3.5}{42}{0.9}
    \drawresumeLeaf{-2.8}{5.9}{-55}{1.1}
    \drawresumeLeaf{-4.3}{6.9}{40}{0.95}
    \drawresumeLeaf{-3.9}{8.9}{-42}{1.05}
    \drawresumeLeaf{-6.6}{10.8}{47}{1}
    \drawresumeLeaf{-7.2}{12.3}{-50}{1.1}
    \drawresumeLeaf{-4.9}{13.5}{40}{0.95}
    \drawresumeLeaf{-7.8}{15.8}{-45}{1}
    \drawresumeLeaf{-10.4}{17.1}{48}{1.1}
    \drawresumeLeaf{-9.3}{19.8}{-45}{0.95}
    \drawresumeLeaf{-12.1}{21.2}{42}{1.05}

    \foreach \x/\y/\angle/\scale in {
      -0.1/9.2/25/1.2,
      -7.6/5.2/-40/1.05,
      -2.7/14/5/1.15,
      -11.2/9.4/-35/1.1,
      -2.5/18.3/10/1.2,
      -13.3/17.2/-45/1.15,
      -6.5/21.8/15/1.05,
      -12.8/23.3/0/1.25
    } {
      \begin{scope}[shift={(\x,\y)},rotate=\angle]
        \drawfloral{\scale}
      \end{scope}
    }
  \end{scope}
}

\newsavebox{\resumeHeaderBox}
\newsavebox{\resumeColumnsBox}
\newcommand{\resumeForegroundContent}{}
\newcommand{\resumecompose}[2]{%
  \sbox{\resumeHeaderBox}{\begin{minipage}{\textwidth}#1\end{minipage}}%
  \sbox{\resumeColumnsBox}{%
    \begin{minipage}{\textwidth}%
      \vspace*{\dimexpr\ht\resumeHeaderBox+\dp\resumeHeaderBox+1em\relax}%
      \noindent#2%
    \end{minipage}%
  }%
  \begin{tikzpicture}[remember picture,overlay]
    \begin{pgfonlayer}{resumeBackground}
      \resumeiflayer{\resumeBackgroundLayer}{%
      }
    \end{pgfonlayer}
    \begin{pgfonlayer}{resumeHeader}
      \resumeiflayer{\resumeHeaderLayer}{%
        \drawresumeFlowers
        \node[anchor=north west,inner sep=0pt] at ([xshift=1.5cm,yshift=-1.5cm]current page.north west) {\usebox{\resumeHeaderBox}};
        \node[anchor=south west,inner sep=0pt] at ([xshift=1.5cm,yshift=1.5cm]current page.south west) {\includegraphics[width=2.75cm]{watermarks/totoro}};
      }
    \end{pgfonlayer}
    \begin{pgfonlayer}{resumeColumns}
      \resumeiflayer{\resumeColumnsLayer}{%
        \node[anchor=north west,inner sep=0pt] at ([xshift=1.5cm,yshift=-1.5cm]current page.north west) {\usebox{\resumeColumnsBox}};
      }
    \end{pgfonlayer}
    \begin{pgfonlayer}{resumeForeground}
      \resumeiflayer{\resumeForegroundLayer}{\resumeForegroundContent}
    \end{pgfonlayer}
  \end{tikzpicture}
  \null\vfill\clearpage
}

% Set main fonts
\defaultfontfeatures{Mapping=tex-text}
\setmainfont[
  AutoFakeSlant=0.2,
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
    \vspace{1em}
}

% Section formatting
\titleformat{\section}{\color{headings}
\fontspec[Path = fonts/Arbutus_Slab/]{ArbutusSlab-Regular}\fontsize{18pt}{24pt}\selectfont \raggedright\uppercase}{} {0em}{}[{\titlerule[0.8pt]}]
\titlespacing{\section}{0pt}{0pt}{5pt}

% Subsection formatting
\titleformat{\subsection}{\color{subheadings}
\fontspec[Path = fonts/Lora/]{Lora-Bold}\fontsize{14pt}{14pt}\selectfont}{}{0em}{}
\titlespacing{\subsection}{0pt}{\parskip}{-\parskip}

% Subsubsection formatting
\titleformat{\subsubsection}{\color{subheadings}
\fontspec[Path = fonts/Lora/]{Lora-Bold}\fontsize{12pt}{12pt}\selectfont}{}{1em}{}
\titlespacing{\subsubsection}{0pt}{\parskip}{-\parskip}

% Grouped logic section formatting
\newcommand{\runsubsection}[1]{\color{subheadings}
\fontspec[Path = fonts/Lora/]{Lora-Bold}\fontsize{12pt}{12pt}\selectfont {#1} \normalfont}

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
		\texorpdfstring{{#1}\hfill{\normalfont #2}}{#1 -- #2}
	}
}

% Suppresses the subsubsection numbering while keeping it in the ToC
\renewcommand\thesubsubsection{}

% Descriptors command
\newcommand{\descript}[1]{\color{subheadings}\raggedright\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location command
\newcommand{\location}[1]{\color{primary}\raggedright\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{11pt}{12pt}\selectfont {#1\\} \normalfont}

% Section seperators command
\newcommand{\sectionsep}[0]{%
  \vspace{8pt}
}

% Bullet Lists with fewer gaps command
\newenvironment{tightemize}{\vspace{-\topsep}\begin{itemize}\raggedright\itemsep1pt \parskip0pt \parsep0pt}{\end{itemize}\vspace{-\topsep}}

% Sets up hyperlink coloring
\hypersetup{colorlinks=true,urlcolor=blue} % Turns the hyperlinks blue
