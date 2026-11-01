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
% Flower configuration. Keep placement, density, color and shape tuning here.
% Opacity range: 0.35-1.0; color tints: 0-100; line widths: 0.35pt-2pt.
% Start offsets: x=0.5-3cm from the right, y=0.5-2cm from the bottom.
% Keep vine/branch/flower placement y<=19.5cm from the start to clear the header.
% Leaf scale range: 0.6-1.4; flower scale range: 0.75-1.4.
% Petal width range: 0.04-0.12cm; length: 0.1-0.25cm; leaf width: 0.08-0.2cm.
% Leaf length range: 0.4-0.9cm; center radius: 0.025-0.07cm.
% Petal/leaf placement rotations currently range -55 to 48 degrees; x positions -14.2 to 0.5cm.
\definecolor{floralblue}{HTML}{2456C4}
\def\resumeFlowerOpacity{0.9}
\def\resumeFlowerPetalTint{35}
\def\resumeFlowerLeafTint{28}
\def\resumeFlowerVineTint{70}
\def\resumeFlowerBranchTint{65}
\def\resumeFlowerOutlineTint{65}
\def\resumeFlowerPetalOutlineTint{75}
\def\resumeFlowerCenterTint{70}
\def\resumeFlowerVineWidth{1.4pt}
\def\resumeFlowerBranchWidth{1.05pt}
\def\resumeFlowerOutlineWidth{0.55pt}
\def\resumeFlowerVeinWidth{0.4pt}
\def\resumeFlowerStartX{1.5cm}
\def\resumeFlowerStartY{1.2cm}
\def\resumeFlowerPetalWidth{0.07cm}
\def\resumeFlowerPetalLength{0.16cm}
\def\resumeFlowerPetalCenterY{0.62}
\def\resumeFlowerPetalY{0.74}
\def\resumeFlowerCenterRadius{0.045cm}
\def\resumeFlowerStemControlX{0.03}
\def\resumeFlowerStemControlOneY{0.15}
\def\resumeFlowerStemControlTwoY{0.3}
\def\resumeFlowerStemEndY{0.5}
\def\resumeFlowerSepalWidth{0.06cm}
\def\resumeFlowerSepalLength{0.14cm}
\def\resumeFlowerSepalOneAngle{-35}
\def\resumeFlowerSepalOneY{0.28}
\def\resumeFlowerSepalTwoAngle{35}
\def\resumeFlowerSepalTwoY{0.14}
\def\resumeFlowerLeafWidth{0.12cm}
\def\resumeFlowerLeafLength{0.68cm}
\def\resumeFlowerLeafControlOneY{0.22}
\def\resumeFlowerLeafControlTwoY{0.48}
\def\resumeFlowerLeafVeinEndY{0.61}
\def\resumeFlowerPetals{%
  \fill[rotate around={0:(0,\resumeFlowerPetalCenterY)}] (0,\resumeFlowerPetalY) ellipse [x radius=\resumeFlowerPetalWidth,y radius=\resumeFlowerPetalLength];
  \fill[rotate around={72:(0,\resumeFlowerPetalCenterY)}] (0,\resumeFlowerPetalY) ellipse [x radius=\resumeFlowerPetalWidth,y radius=\resumeFlowerPetalLength];
  \fill[rotate around={144:(0,\resumeFlowerPetalCenterY)}] (0,\resumeFlowerPetalY) ellipse [x radius=\resumeFlowerPetalWidth,y radius=\resumeFlowerPetalLength];
  \fill[rotate around={216:(0,\resumeFlowerPetalCenterY)}] (0,\resumeFlowerPetalY) ellipse [x radius=\resumeFlowerPetalWidth,y radius=\resumeFlowerPetalLength];
  \fill[rotate around={288:(0,\resumeFlowerPetalCenterY)}] (0,\resumeFlowerPetalY) ellipse [x radius=\resumeFlowerPetalWidth,y radius=\resumeFlowerPetalLength];
}
\def\resumeFlowerVinePath{%
  (0,0) .. controls (-1.2,2) and (-0.5,4) .. (-2.7,5.8)
  .. controls (-4.3,7.1) and (-2.8,9) .. (-5.6,10.6)
  .. controls (-8.2,12.2) and (-4.6,13.2) .. (-6.2,15.2)
  .. controls (-7.7,17.1) and (-10.2,17.2) .. (-10.8,19.1)
  .. controls (-11.6,19.3) and (-10.1,19.4) .. (-12.8,19.5)
}
\def\resumeFlowerBranchPaths{%
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-2.4,5.5) .. controls (-0.5,6.1) and (0.1,7.4) .. (-0.1,9.2);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-2.6,6) .. controls (-4.2,5.2) and (-5.8,4.9) .. (-7.6,5.2);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-4.8,9.8) .. controls (-3.1,10.9) and (-2.4,12.2) .. (-2.7,14);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-5.8,10.5) .. controls (-7.4,9.1) and (-9.1,8.8) .. (-11.2,9.4);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-6.2,14.9) .. controls (-4.5,15.7) and (-3.1,16.7) .. (-2.5,18.3);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-7.3,16.5) .. controls (-9.2,15.9) and (-11.2,16.1) .. (-13.3,17.2);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-10.7,18.8) .. controls (-9,19.1) and (-7.4,19.2) .. (-6.5,19.5);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-1.6,3.8) .. controls (-0.2,4.2) and (0.7,5.5) .. (0.5,6.8);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-3.7,8.4) .. controls (-5.1,7.5) and (-6.8,7.4) .. (-8.4,7.9);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-8.2,13.8) .. controls (-9.8,12.8) and (-11.7,12.7) .. (-13.2,13.4);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-8.5,17.5) .. controls (-7.2,18.2) and (-6.2,18.9) .. (-5.8,19.5);
  \draw[floralblue!\resumeFlowerBranchTint,line width=\resumeFlowerBranchWidth] (-11.5,19.2) .. controls (-12.4,19.1) and (-13.5,18.9) .. (-14.2,18.4);
}
\def\resumeFlowerLeaves{%
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
  \drawresumeLeaf{-9.3}{18.2}{-45}{0.95}
  \drawresumeLeaf{-12.1}{18.5}{42}{1.05}
  \drawresumeLeaf{-1.0}{4.5}{-45}{0.9}
  \drawresumeLeaf{-5.1}{7.9}{45}{1}
  \drawresumeLeaf{-9.6}{11.2}{-45}{1.1}
  \drawresumeLeaf{-3.3}{12.2}{48}{0.9}
  \drawresumeLeaf{-8.7}{15.1}{45}{1}
  \drawresumeLeaf{-12.8}{17.5}{-42}{0.95}
  \drawresumeLeaf{-5.4}{17.8}{-48}{1.05}
  \drawresumeLeaf{-2.4}{17}{40}{1}
}
\def\resumeFlowerHeads{%
  \begin{scope}[shift={(-0.1,6.8)},rotate=25]\drawfloral{1.2}\end{scope}
  \begin{scope}[shift={(-7.6,5.2)},rotate=-40]\drawfloral{1.05}\end{scope}
  \begin{scope}[shift={(-2.7,14)},rotate=5]\drawfloral{1.15}\end{scope}
  \begin{scope}[shift={(-11.2,9.4)},rotate=-35]\drawfloral{1.1}\end{scope}
  \begin{scope}[shift={(-2.5,18.3)},rotate=10]\drawfloral{1.2}\end{scope}
  \begin{scope}[shift={(-13.3,17.2)},rotate=-45]\drawfloral{1.15}\end{scope}
  \begin{scope}[shift={(-6.5,19.4)},rotate=15]\drawfloral{1.05}\end{scope}
  \begin{scope}[shift={(-12.8,19.5)},rotate=0]\drawfloral{1.25}\end{scope}
  \begin{scope}[shift={(0.5,4)},rotate=-20]\drawfloral{0.9}\end{scope}
  \begin{scope}[shift={(-8.4,7.9)},rotate=35]\drawfloral{1}\end{scope}
  \begin{scope}[shift={(-13.2,13.4)},rotate=-30]\drawfloral{1.05}\end{scope}
  \begin{scope}[shift={(-5.8,19.5)},rotate=15]\drawfloral{0.95}\end{scope}
}

\newcommand{\drawfloral}[1]{%
  \begin{scope}[scale=#1,draw=floralblue!\resumeFlowerPetalOutlineTint,fill=floralblue!\resumeFlowerPetalTint]
    \resumeFlowerPetals
    \fill[floralblue!\resumeFlowerCenterTint] (0,\resumeFlowerPetalCenterY) circle [radius=\resumeFlowerCenterRadius];
    \draw[line width=\resumeFlowerOutlineWidth] (0,0) .. controls (\resumeFlowerStemControlX,\resumeFlowerStemControlOneY) and (-\resumeFlowerStemControlX,\resumeFlowerStemControlTwoY) .. (0,\resumeFlowerStemEndY);
    \fill[rotate around={\resumeFlowerSepalOneAngle:(0,\resumeFlowerSepalOneY)}] (0,\resumeFlowerSepalOneY) ellipse [x radius=\resumeFlowerSepalWidth,y radius=\resumeFlowerSepalLength];
    \fill[rotate around={\resumeFlowerSepalTwoAngle:(0,\resumeFlowerSepalTwoY)}] (0,\resumeFlowerSepalTwoY) ellipse [x radius=\resumeFlowerSepalWidth,y radius=\resumeFlowerSepalLength];
  \end{scope}
}

\newcommand{\drawresumeLeaf}[4]{%
  \begin{scope}[shift={(#1,#2)},rotate=#3,scale=#4]
    \path[fill=floralblue!\resumeFlowerLeafTint,draw=floralblue!\resumeFlowerOutlineTint,line width=\resumeFlowerOutlineWidth]
      (0,0) .. controls (\resumeFlowerLeafWidth,\resumeFlowerLeafControlOneY) and (\resumeFlowerLeafWidth,\resumeFlowerLeafControlTwoY) .. (0,\resumeFlowerLeafLength)
      .. controls (-\resumeFlowerLeafWidth,\resumeFlowerLeafControlTwoY) and (-\resumeFlowerLeafWidth,\resumeFlowerLeafControlOneY) .. cycle;
    \draw[floralblue!\resumeFlowerOutlineTint,line width=\resumeFlowerVeinWidth] (0,0) -- (0,\resumeFlowerLeafVeinEndY);
  \end{scope}
}

\newcommand{\drawresumeFlowers}{%
  \begin{scope}[shift={([xshift=-\resumeFlowerStartX,yshift=\resumeFlowerStartY]current page.south east)},opacity=\resumeFlowerOpacity]
    \draw[floralblue!\resumeFlowerVineTint,line width=\resumeFlowerVineWidth] \resumeFlowerVinePath;
    \resumeFlowerBranchPaths
    \resumeFlowerLeaves
    \resumeFlowerHeads
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
