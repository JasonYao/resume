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
\definecolor{resumeEducation}{HTML}{56B4E9}
\definecolor{resumeProgramming}{HTML}{009E73}
\definecolor{resumeGeneral}{HTML}{CC79A7}
\definecolor{resumePosition}{HTML}{E69F00}
\providecommand{\resumeFlowerLayerPdf}{florilegium_layer.pdf}
\def\resumeFlowerClipHeight{5.05cm}
\def\resumeFlowerVerticalOffset{-0.3cm}
\def\resumeFlowerSeedInset{0.3cm}
\def\resumeFlowerSeedBoxSize{1cm}
\def\resumeFlowerTotoroPadding{0.2cm}
\tikzset{resumePreviewBox/.style={draw=red,line width=0.5pt}}
\newcommand{\resumeDrawPreviewBounds}[1]{%
  \ifx\resumeLayerPreview\resumeCompositeLayer\else
    \draw[red,line width=0.5pt] #1;
  \fi
}
\newcommand{\resumeDrawFlowerBounds}{%
  \ifx\resumeLayerPreview\resumeCompositeLayer\else
    \draw[orange,line width=0.5pt] (current page.south west) rectangle ([yshift=\resumeFlowerClipHeight]current page.south east);
    \draw[orange,line width=0.75pt]
      ([xshift=-\dimexpr\resumeFlowerSeedInset+\resumeFlowerSeedBoxSize\relax,yshift=\resumeFlowerSeedInset]current page.south east)
      rectangle
      ([xshift=-\resumeFlowerSeedInset,yshift=\dimexpr\resumeFlowerSeedInset+\resumeFlowerSeedBoxSize\relax]current page.south east);
    \coordinate (resumeFlowerCenter) at ([xshift=\dimexpr\paperwidth/2\relax,yshift=\dimexpr\resumeFlowerClipHeight/2\relax]current page.south west);
    \foreach \corner in {
      (current page.south west),
      (current page.south east),
      ([yshift=\resumeFlowerClipHeight]current page.south west),
      ([yshift=\resumeFlowerClipHeight]current page.south east)
    } {
      \draw[orange,->] (resumeFlowerCenter) -- node[midway,fill=white,inner sep=1pt,font=\scriptsize,text=orange] {11.1 cm} \corner;
    }
  \fi
}
\newcommand{\resumePreviewName}[1]{%
  \ifx\resumeLayerPreview\resumeCompositeLayer
    #1%
  \else
    \tikz[baseline=(resumeName.base)]\node[draw=green,line width=0.5pt,inner sep=0pt,outer sep=0pt] (resumeName) {#1};
  \fi
}
\newcommand{\resumePreviewLinks}[1]{%
  \ifx\resumeLayerPreview\resumeCompositeLayer
    #1%
  \else
    \tikz[baseline=(resumeLinks.base)]\node[draw=blue,line width=0.5pt,inner sep=0pt,outer sep=0pt] (resumeLinks) {#1};
  \fi
}
\newcommand{\resumePreviewContentBox}[3]{%
  \ifx\resumeLayerPreview\resumeColumnsLayer
    \begingroup
      \setbox#2=\vbox{\hsize=\linewidth\color{primary}#3}%
      \hbox{\copy#2\smash{\rlap{\tikz[baseline=0pt]{%
        \draw[#1,line width=0.5pt] (-\wd#2,-\dp#2) rectangle (0,\ht#2);%
      }}}}%
    \endgroup
  \else
    #3%
  \fi
}
\newsavebox{\resumeHeaderBox}
\newsavebox{\resumeColumnsBox}
\newsavebox{\resumeTotoroBox}
\newsavebox{\resumeEducationPreviewBuffer}
\newsavebox{\resumeProgrammingPreviewBuffer}
\newsavebox{\resumeGeneralPreviewBuffer}
\newsavebox{\resumePositionPreviewBuffer}
\newsavebox{\resumeNameContentBox}
\newsavebox{\resumeLinksContentBox}
\newcommand{\resumeForegroundContent}{}
\newcommand{\resumecompose}[2]{%
  \sbox{\resumeTotoroBox}{\includegraphics[width=2.75cm]{watermarks/totoro}}%
  \sbox{\resumeHeaderBox}{\begin{minipage}{\textwidth}#1\end{minipage}}%
  \sbox{\resumeColumnsBox}{%
    \begin{minipage}{\textwidth}%
      \vspace*{\dimexpr\ht\resumeHeaderBox+\dp\resumeHeaderBox+1em\relax}%
      \noindent#2%
    \end{minipage}%
  }%
  \ifx\resumeLayerPreview\resumeCompositeLayer
    \def\resumePreviewBoxStyle{}%
  \else
    \def\resumePreviewBoxStyle{resumePreviewBox}%
  \fi
  \begin{tikzpicture}[remember picture,overlay]
    \begin{pgfonlayer}{resumeBackground}
      \resumeiflayer{\resumeBackgroundLayer}{%
        \resumeDrawPreviewBounds{(current page.south west) rectangle (current page.north east)}%
      }
    \end{pgfonlayer}
    \begin{pgfonlayer}{resumeHeader}
      \resumeiflayer{\resumeHeaderLayer}{%
        \begin{scope}
          \clip (current page.south west) rectangle ([yshift=\resumeFlowerClipHeight]current page.south east);
          \node[anchor=south west,inner sep=0pt] at ([yshift=\resumeFlowerVerticalOffset]current page.south west) {
            \includegraphics[angle=90]{\resumeFlowerLayerPdf}};
        \end{scope}
        \fill[white]
          ([xshift=\dimexpr0.75cm+0.17\textwidth-\wd\resumeTotoroBox/2-\resumeFlowerTotoroPadding\relax,yshift=\dimexpr1.5cm-\resumeFlowerTotoroPadding\relax]current page.south west)
          rectangle
          ([xshift=\dimexpr0.75cm+0.17\textwidth+\wd\resumeTotoroBox/2+\resumeFlowerTotoroPadding\relax,yshift=\dimexpr1.5cm+\ht\resumeTotoroBox+\resumeFlowerTotoroPadding\relax]current page.south west);
        \resumeDrawFlowerBounds
        \node[anchor=north west,inner sep=0pt,\resumePreviewBoxStyle] at ([xshift=1.5cm,yshift=-1.5cm]current page.north west) {\usebox{\resumeHeaderBox}};
        \node[anchor=south,inner sep=0pt,\resumePreviewBoxStyle] at ([xshift=\dimexpr0.75cm+0.17\textwidth\relax,yshift=1.5cm]current page.south west) {\usebox{\resumeTotoroBox}};
      }
    \end{pgfonlayer}
    \begin{pgfonlayer}{resumeColumns}
      \resumeiflayer{\resumeColumnsLayer}{%
        \node[anchor=north west,inner sep=0pt,\resumePreviewBoxStyle] at ([xshift=1.5cm,yshift=-1.5cm]current page.north west) {\usebox{\resumeColumnsBox}};
      }
    \end{pgfonlayer}
    \begin{pgfonlayer}{resumeForeground}
      \resumeiflayer{\resumeForegroundLayer}{%
        \resumeForegroundContent
        \resumeDrawPreviewBounds{(current page.south west) rectangle (current page.north east)}%
      }
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
\newcommand{\namesection}[2]{%
    \sbox{\resumeNameContentBox}{\resumePreviewName{\fontspec[Path = fonts/IM_Fell_French_Canon_SC/]{IMFeFCsc28P}\fontsize{58pt}{0cm}\selectfont \MakeUppercase{#1}}}%
    \sbox{\resumeLinksContentBox}{%
	% To increase the amount of space available for the links, increment the below's em value
    \raggedleft{\resumePreviewLinks{\parbox[b]{15em}{\color{headings}\fontspec[Path = fonts/IM_Fell_Great_Primer/]{IMFeGPrm28P}\fontsize{11pt}{14pt}\selectfont #2}}}}%
    \noindent\hspace*{\dimexpr(\textwidth-\wd\resumeLinksContentBox-\wd\resumeNameContentBox-1.5cm)/2\relax}%
    \raisebox{\dimexpr(\ht\resumeLinksContentBox+\dp\resumeLinksContentBox-\ht\resumeNameContentBox-\dp\resumeNameContentBox)/2+0.4em\relax}{\usebox{\resumeNameContentBox}}%
    \hfill\usebox{\resumeLinksContentBox}%
    \vspace{1em}%
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
