% Please be sure to run the compiler at least 3 times to have all correct placement for the different parts of this document. It is recommended to run the compiler more than 3 times. I compile for release at least 4 times (Line number, svg and images alignments, text formatting and biber, fonts etc.).

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{banko}[A document class called banko]

\RequirePackage{kvoptions}
\RequirePackage{datetime}

\DeclareStringOption[ieee]{bibstyle}        % Citation style
\DeclareStringOption[english]{language}     % Language
\DeclareBoolOption{unicode}                 % Unicode
\DeclareBoolOption{placeins}                % Prevent floats from skipping sections
\ProcessKeyvalOptions*\relax

% Pass unknown to article class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\ProcessOptions\relax

% Base class: article with two-column layout
\LoadClass[twocolumn]{article}

\RequirePackage{chemfig}


% Load required packages
\RequirePackage[table,svgnames]{xcolor}           % Color
\RequirePackage{fontspec}         % Font
\RequirePackage[bottom]{footmisc} % Footnotes
\RequirePackage{lastpage}         % Last page
% \RequirePackage{luacode} Disabled
\RequirePackage[                                        % Title settings
%explicit,
compact,
% nobottomtitles,
]{titlesec}  
\RequirePackage{svg}
\RequirePackage{tipa}
\RequirePackage{alphalph}
\RequirePackage{float}
\RequirePackage{microtype}
\RequirePackage{tikz}
\usetikzlibrary{cd}

\RequirePackage{mathrsfs}

% Math typesetting
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amstext}
\RequirePackage{amsfonts}
\RequirePackage{bm}
\RequirePackage[most]{tcolorbox}

% Math structures
\RequirePackage{array}                                  % Arrays
\RequirePackage{empheq}                                 % Grouped equations
\RequirePackage{amsthm}                                 % Theorems
\RequirePackage{thmtools}                               % List of theorems


% Math and scientific symbols and utilities
\RequirePackage{siunitx}                                % Units
\sisetup{detect-all}
\RequirePackage[                                        % Chemistry typesetting
version=4
]{mhchem}
\RequirePackage{extarrows}                              % Labelled arrows and signs
\RequirePackage{gensymb}                                % Generic symbols for text and math mode
\RequirePackage{latexsym}                               % Additional symbols
\RequirePackage{optidef}                                % Bolza problems

% Links and cross-references
\RequirePackage[                                        % Links and cross-references
colorlinks = false,
allcolors  = blue,
unicode    = true
]{hyperref} % Adding Autoref
\RequirePackage{xurl}

\RequirePackage{titling}

\RequirePackage{graphicx} % Required for inserting images
\RequirePackage{lipsum}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{contour}                                % Underlines
\RequirePackage[                                        % Underlines: normalem to avoid underlining all \emph'sized words (bibliography entries)
normalem
]{ulem}

% Bibliography
\RequirePackage[
backend=biber,
style=ieee, % \BPN@bibstyle
citestyle=numeric-comp
]{biblatex}                                             % Biblatex citation engine and style
\RequirePackage[capitalise]{cleveref}                   % Chained citations
\RequirePackage{csquotes}                               % Recommended addition for citations
\RequirePackage[bottom]{footmisc}                       % Footnotes
\RequirePackage{enotez}


\RequirePackage{chemformula}
\RequirePackage{mhchem}

\RequirePackage{booktabs}

%\RequirePackage[htt]{hyphenat}
\RequirePackage{caption}                                % Captions
\RequirePackage{fmtcount}  

\RequirePackage{xeCJK}

% Hauptschriftart für CJK: Koreanisch
\setCJKfallbackfamilyfont{\CJKrmdefault}{NotoSerifJP}[
	Path = ./fonts/,
	Extension = .ttf,
	UprightFont = *-Regular
]

\setCJKfallbackfamilyfont{}{NotoSerifKR}[
	Path = ./fonts/,
	Extension = .ttf,
	UprightFont = *-Regular
]


% Fallback für Chinesisch
\setCJKfallbackfamilyfont{}{NotoSerifTC}[
	Path = ./fonts/,
	Extension = .ttf,
	UprightFont = *-Regular
]

\setCJKfallbackfamilyfont{}{NotoSerifSC}[
Path = ./fonts/,
Extension = .ttf,
UprightFont = *-Regular
]

% Sans-serif und Monospace Schriftarten
%\setCJKsansfont[
%	Path = ./fonts/,
%	Extension = .ttf,
%	UprightFont = *-Regular
%]{NotoSansKR}

%\setCJKmonofont[
%	Path = ./fonts/,
%	Extension = .ttf,
%	UprightFont = *-Regular
%]{NotoSansMonoKR}


% Line spacing and compatibility
\linespread{1.1} % Adjust spacing for CJK text


\RequirePackage[overlap, CJK]{ruby}
% \renewcommand{\rubysize}{1}
\renewcommand{\rubysep}{0.1ex}

\RequirePackage[english]{babel}

% Programming
\RequirePackage{listings}


% Line Number
\usepackage[switch]{lineno}
\linenumbers
\modulolinenumbers[2]


% Macro
\newcommand*{\BPNyear}[1]{\def\BPN@year{#1}}\BPNyear{}
\newcommand*{\BPNlocation}[1]{\def\BPN@location{#1}}\BPNlocation{}
\newcommand*{\BPNdates}[1]{\def\BPN@dates{#1}}\BPNdates{}

\newcommand*{\BPNmode}[1]{%
	\ifx\relax#1\relax % Check if no argument is provided
	\def\BPN@mode{0}% Default value is 0
	\else
	\def\BPN@mode{#1}% Set provided value
	\fi
}\BPNmode{}


\newcommand{\BPNcopyright}[2]{\def\BPN@copyright{Copyright \copyright\,#1 by #2. All rights reserved.}}
\newcommand*{\BPNarchive}[1]{\def\BPN@archive{#1}}\BPNarchive{}
\newcommand*{\BPNundertitle}[1]{\def\BPN@undertitle{#1}}\BPNundertitle{}
\newcommand*{\BPNsubundertitle}[1]{\def\BPN@subundertitle{#1}}\BPNsubundertitle{}
\newcommand*{\BPNRevision}[1]{\def\BPN@revision{#1}}\BPNRevision{}
\newcommand*{\BPNVersion}[1]{\def\BPN@version{#1}}\BPNVersion{}
\newcommand*{\BPNLogo}[1]{\def\BPN@logo{#1}}\BPNLogo{}

\newcommand*{\BPNdoi}[1]{\def\BPN@doi{#1}}\BPNdoi{10.xxxx/xxxxx}

% Footers & Headers
\RequirePackage{fancyhdr} % Load the fancyhdr package

% Maketitle

\newcommand{\alignmentMode}[0]{%
	\ifnum\BPN@mode=0
	\centering
	\else\ifnum\BPN@mode=1
	\raggedright
	\else
	\raggedleft
	\fi\fi
}

\newcommand{\goDown}{%
	\ifnum\BPN@mode=0
	\\
	\fi
}

\newcommand{\spaceV}[0]{
	\ifnum\BPN@mode=0
	\vspace{1em}
	\else\ifnum\BPN@mode=1
	\vspace{0.3em}
	\else
	\vspace{0.3em}
	\fi\fi
}

\newcommand{\subundertitleFormat}{%
	\ifx\BPN@subundertitle\empty
	% Do nothing
	\else
	\\ \BPN@subundertitle
	\fi
}


\renewcommand{\abstract}[1]{
	\def\BPN@abstract{
		\vspace*{1 em} % Adjust the space before paragraphs
		{\alignmentMode
			\bfseries Abstract\\
		}
		\vspace*{0.2em} % Adjust the space after paragraphs
		\setlength{\parindent}{0.5cm} % Indent the first line of text
		\setlength{\parskip}{0pt} % Single spacing        
		\raggedright
%		\quad#1
		#1
	}
}

\newcounter{authcount}
\newcounter{contactauthor}
\NewDocumentCommand{\BPNauthor}{ s m m m }{%
	\stepcounter{authcount}%
	\csdef{BPN@author\theauthcount}{#2}%
	\csdef{BPN@affiliation\theauthcount}{#3}%
	\csdef{BPN@email\theauthcount}{#4}%
	\IfBooleanT{#1}{\setcounter{contactauthor}{\theauthcount}}%
}

\def\version{1.5.5 Beta}

% Define a custom title page style
\fancypagestyle{titlepage}{
	\fancyhf{} % Clear all header and footer fields
	\fancyhead[C]{{\footnotesize\color{gray} Banko Version: \version~\BPN@copyright}} % Custom header
	\renewcommand{\headrulewidth}{0pt} % Header line thickness
	\renewcommand{\footrulewidth}{0pt} % No footer line
	
	\fancyfoot[L]{}
	\fancyfoot[C]{}
	\fancyfoot[R]{{\footnotesize\color{gray}Page \thepage\ of \pageref{LastPage}}}
}

% Define the \maketitle command with the custom header and randomized title
\makeatletter
% Two-column document with single-column title section
\renewcommand\maketitle{\twocolumn[
	\begin{@twocolumnfalse}
		\begingroup
		\global\@topnum\z@   % Prevents figures from going at top of page.
		\@maketitle
		\@thanks
		\endgroup
	\end{@twocolumnfalse}
	]}
\def\@maketitle{%
	\begin{titlepage}
		\thispagestyle{titlepage}
		\alignmentMode
		{\huge \bfseries{\@title}\par}
		\spaceV
		{\Large \bfseries{\BPN@undertitle}  \bfseries{\large\subundertitleFormat{} }} {\goDown \itshape on \BPN@dates \space in \BPN@location}
		{Version \BPN@version \space Revision \BPN@revision \par}
		\vspace{1em}
		
		{\BPN@logo\par}
		
		{\centering Archive-ID: \BPN@archive \space DOI: \BPN@doi \par}
		
		% Author
		\begin{center}%
			\lineskip .5em%
			\newcounter{authnum}%
			\setcounter{authnum}{0}
			\whileboolexpr%
			{ test {\ifnumcomp{\value{authnum}}{<}{\theauthcount}} }%
			{%
				\stepcounter{authnum}%
				\mbox{
					\normalsize\textbf{\csuse{BPN@author\theauthnum}\textsuperscript{\alph{authnum}}}%
					\ifboolexpr%
					{ test {\ifnumcomp{\value{authnum}}{=}{\thecontactauthor}}}%
					{\textsuperscript{\kern-1pt$\conv$}}%
					{}%
					\ifboolexpr%
					{ test {\ifnumcomp{\value{authnum}}{<}{\theauthcount}}}%
					{,~}%
					{}%
				}
			}%
		\end{center}%
		
		% Author affiliations
		{\small\itshape\selectfont%
			\setcounter{authnum}{0}
			\whileboolexpr%
			{ test {\ifnumcomp{\value{authnum}}{<}{\theauthcount}} }%
			{%
				\stepcounter{authnum}%
				\parbox{0.75em}{\normalfont\selectfont\textsuperscript{\alph{authnum}}}\csuse{BPN@affiliation\theauthnum},~\uline{\csuse{BPN@email\theauthnum}}\par
			}%
			\parbox{0.75em}{\textsuperscript{*}}Corresponding Author
		}
		
		{\BPN@abstract\par}
		\vspace{3em}
	\end{titlepage}
}


% Set up the page style for fancyhdr
\pagestyle{fancy}

% Define custom header
\fancyhead[L]{{\footnotesize\color{gray} Banko Version: \version~\BPN@copyright}}
\fancyhead[R]{{\footnotesize\color{gray}\BPN@dates}} % Right-aligned header

% Define custom footer
\fancyfoot[L]{{\footnotesize\color{gray}Archive ID: \BPN@year--\BPN@archive \quad Title: \@title}}
\fancyfoot[C]{}
\fancyfoot[R]{{\footnotesize\color{gray}Page \thepage\ of \pageref{LastPage}}}

\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt} % To remove the footer line

% Roman Number for Pages
\newcommand{\romanPage}{
	\pagenumbering{roman}
}

\newcommand{\arabicPage}{
	\pagenumbering{arabic}
}


% Footnotes
\renewcommand*{\thefootnote}{\footnotesize\color{important}\Roman{footnote}}

% Prevent vertical streching
\raggedbottom

% Define custom fonts
\setmainfont{Times New Roman}%[Scale= 1.1] % Times New Roman, Scale = 1


%MATH
% Symbols
\let\@forall\forall
\renewcommand{\forall}{\ensuremath{\,\@forall\,}}
\DeclareRobustCommand{\vect}[1]{\vec{#1}}
\newcommand{\indep}{\ensuremath{\perp\!\!\!\perp}}

% Character definitions
\mathchardef\mathmul=\mathcode`*
\mathcode`*=\cdot

% Operators
\DeclareMathOperator{\E}{\mathbb{E}}
\DeclareMathOperator{\prob}{p}
\DeclareMathOperator{\tr}{tr}
\DeclareMathOperator{\diff}{\mathop{}\!{d}}
\DeclareMathOperator{\conv}{\ast}

% Equation spacing
\g@addto@macro\normalsize{%
	\setlength\abovedisplayskip{2.5pt}%
	\setlength\belowdisplayskip{7.5pt}%
	\setlength\abovedisplayshortskip{2.5pt}%
	\setlength\belowdisplayshortskip{7.5pt}%
}

% Format
\RequirePackage[
margin=2cm,
top=2.5cm,
headsep=1cm,
bottom=2.5cm
]{geometry}

\RequirePackage{calc}

% Section
\newcommand{\sectionfont}{\normalfont}

\titleformat{\section}[block]
{\normalfont\normalsize\bfseries\sectionfont}
{\thesection}{1em}{}
[\titlerule] % Add a rule under the section title

\titleformat{\subsection}[block]
{\normalfont\normalsize\itshape}
{\thesubsection}{1em}{}
[] % No rule after subsection

\titleformat{\subsubsection}[block]
{\normalfont\normalsize\itshape}
{\thesubsubsection}{1em}{}
[] % No rule after subsubsection

\titleformat{\part}[block]
{\normalfont\Large\bfseries}
{\thepart}{1em}{}
[\titlerule] % No rule after subsubsection

% Custom section command with hierarchical numbering style x.y.z
\renewcommand{\thesection}{\arabic{section}} % Section format: 1, 2, 3...
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}} % Subsection format: 1.1, 1.2, 1.3...
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}} % Subsubsection format: 1.1.1, 1.1.2, etc.


% Define custom colors
\definecolor{important}{HTML}{AB2341} % Default headline color (blood red)
\definecolor{slcolor}{HTML}{882B21}   % Custom secondary color (deep red)
\definecolor{tip}{HTML}{1A159B}   % Default Blue
\definecolor{result}{HTML}{6BBB4C}   % Default Blue

% Define a command to set the headline color dynamically
\newcommand{\setimportant}[1]{%
	\renewcommand{\important}{#1}%
}

% Custom section header with dynamic headline color
\newcommand{\importantsection}[1]{%
	\section{\textcolor{important}{#1}}%
}

\newcommand{\tipsection}[1]{%
	\section{\textcolor{tip}{#1}}%
}

\newcommand{\warningsection}[1]{%
	\section{\color{orange}{#1}}%
}

\newcommand{\examplesection}[1]{%
	\section{\itshape\color{blue}{#1}}%
}

\newcommand{\resultsection}[1]{%
	\section{\itshape\textcolor{result}{#1}}%
}

\newcommand{\questionsection}[1]{%
	\section{\itshape\color{gray}{#1}}%
}

% Boxes

\newcounter{ctrDefinition}
\newcounter{ctrExercise}
\newcounter{ctrIntroduction}
\newcounter{ctrSummary}

\newcommand{\formattingBoxNumber}[1]{%
	\ifnum\value{subsection}=0
	\ifnum\value{subsubsection}=0
	\thesection.#1
	\else
	\thesubsection.#1
	\fi
	\else
	\ifnum\value{subsubsection}=0
	\thesubsection.#1
	\else
	\thesubsubsection.#1
	\fi
	\fi
}


\newcommand{\definitionAN}[3]{ % Additional Notes
	\refstepcounter{ctrDefinition}
	\begin{tcolorbox}[title=\textbf{\formattingBoxNumber{\thectrDefinition}} Definition: #1,
		title filled=false,
		colback=black!3!white,
		colframe=black!75!black]
		#2
		\tcblower
		#3
	\end{tcolorbox}
}

\newcommand{\definition}[2]{
	\refstepcounter{ctrDefinition}
	\begin{tcolorbox}[title=\textbf{\formattingBoxNumber{\thectrDefinition}} Definition: #1,
		title filled=false,
		colback=black!3!white,
		colframe=black!75!black]
		#2
	\end{tcolorbox}
}

\newcommand{\exercise}[2]{ % Without Solution and Explanation
	\refstepcounter{ctrExercise}
	\begin{tcolorbox}[title=\textbf{\formattingBoxNumber{\thectrExercise}} Exercise: #1,
		title filled=false,
		colback=blue!3!white,
		colframe=blue!50!black]
		#2
	\end{tcolorbox}
}

\newcommand{\exerciseWS}[3]{ % With Solution and Explanation
	\refstepcounter{ctrExercise}
	\begin{tcolorbox}[title=\textbf{\formattingBoxNumber{\thectrExercise}} Exercise: #1,
		title filled=false,
		colback=blue!3!white,
		colframe=blue!50!black]
		#2
		\tcblower
		#3
	\end{tcolorbox}
}

\newcommand{\introduction}[2]{
	\refstepcounter{ctrIntroduction}
	\begin{tcolorbox}[title=\textbf{\formattingBoxNumber{\thectrIntroduction}} #1,
		title filled=false,
		colback=purple!3!white,
		colframe=purple!75!black]
		#2
	\end{tcolorbox}
}

\newcommand{\summary}[2]{
	\refstepcounter{ctrSummary}
	\begin{tcolorbox}[title=\textbf{\formattingBoxNumber{\thectrSummary}} #1,
		title filled=false,
		colback=green!3!white,
		colframe=green!40!black]
		#2
	\end{tcolorbox}
}

% Page layout and column.
\newif\iflayouttoggle
\layouttoggletrue 
% Toggle layout definition
\newcommand{\togglelayout}{%
	\clearpage % Ensure site correct layout
	\iflayouttoggle
	\onecolumn
	\layouttogglefalse
	\else
	\twocolumn
	\layouttoggletrue
	\fi
}

% Solution, Question etc.

\newcounter{problem}
\newcounter{solution}

\newcommand\Problem{%
	\stepcounter{problem}%
	\textbf{\theproblem.}~%
	\setcounter{solution}{0}%
}

\newcommand\TheSolution{%
	\textbf{Solution:}\\%
}

\newcommand\ASolution{%
	\stepcounter{solution}%
	\textbf{Solution \thesolution:}\\%
}

% Sidenotes

\RequirePackage{etoolbox}

% Counter for sidenotes and list storage
\newcounter{sidenote}
\newcommand{\sidenote@list}{} 

% Define sidenote command
\newcommand{\sidenote}[1]{%
	\refstepcounter{sidenote}% Increment counter
	\mbox{\textsuperscript{\color{important}\alph{sidenote}}}% Show reference in text
	\marginpar{\footnotesize\raggedright\strut
		\textsuperscript{\color{important}\alph{sidenote}} #1}% Display sidenote in margin
	% Store sidenote for Table of Sidenotes without repeating numbers
	\g@addto@macro\sidenote@list{%
		\item Sidenote:  #1%
	}
}

% Command to generate Table of Sidenotes
\newcommand{\sidenotestable}{%
	\newpage
	\section*{Table of Sidenotes}
	\begin{enumerate}
		\sidenote@list % Insert stored sidenotes
	\end{enumerate}
}

% Set margin width and spacing
\setlength{\marginparwidth}{.7in}
\setlength{\marginparsep}{.2in}
\reversemarginpar

\newcommand{\citeBlock}[2]{
	\itshape "#1" \hfill -- #2
}

\newcommand\elec{\mathrm{e^-}}
\newcommand\prot{\mathrm{p^+}}
\newcommand\neut{\mathrm{n^0}}

\newcommand{\appendices}{
	\clearpage
	\appendix
	\renewcommand{\thepart}{\Alph{part}} % Change part numbering to 
	\setcounter{part}{0} % Reset part counter to start from A
}

\newtcolorbox{twocolboxN}{
	colframe=white, colback=white,
	sharp corners, boxrule=0pt,
	width=\textwidth,
	before={\par\medskip}, after={\par\medskip},
}

% New command to create the two-column box
\newcommand{\twocolbox}[2]{
	\if@twocolumn
	\importantsection{Error in Alignment of Text 1:1}
	\textbf{\textcolor[HTML]{B22222}{Error}}: This document is in two-column mode. The two-column box is not compatible with this mode. 1:1. Content: \textbf{Column 1:} #1, \textbf{Column 2:} #2
	\else
	\begin{twocolboxN}
		\begin{minipage}[t]{0.48\textwidth}
			\textbf{Column 1:} #1
		\end{minipage}%
		\hfill
		\begin{minipage}[t]{0.48\textwidth}
			\textbf{Column 2:} #2
		\end{minipage}
	\end{twocolboxN}
	\fi
}

\newcommand{\twocolboxDWPL}[2]{
	\if@twocolumn
	\importantsection{Error in Alignment of Text 2:1 DWPL}
	\textbf{\textcolor[HTML]{B22222}{Error}}: This document is in two-column mode. The two-column box is not compatible with this mode. 2:1. Content: \textbf{Column 1:} #1, \textbf{Column 2:} #2
	\else
	\begin{twocolboxN}
		\begin{minipage}[t]{0.64\textwidth}
			\textbf{Column 1:} #1
		\end{minipage}%
		\hfill
		\begin{minipage}[t]{0.34\textwidth}
			\textbf{Column 2:} #2
		\end{minipage}
	\end{twocolboxN}
	\fi
}


\newcommand{\twocolboxDWPR}[2]{
	\if@twocolumn
	\importantsection{Error in Alignment of Text 1:2 DWPR}
	\textbf{\textcolor[HTML]{B22222}{Error}}: This document is in two-column mode. The two-column box is not compatible with this mode. 1:2. Content: \textbf{Column 1:} #1, \textbf{Column 2:} #2
	\else
	\begin{twocolboxN}
		\begin{minipage}[t]{0.34\textwidth}
			\textbf{Column 1:} #1
		\end{minipage}%
		\hfill
		\begin{minipage}[t]{0.64\textwidth}
			\textbf{Column 2:} #2
		\end{minipage}
	\end{twocolboxN}
	\fi
}

\newcommand{\twocolboxKWPL}[2]{
	\if@twocolumn
	\importantsection{Error in Alignment of Text 3:1 KWPL}
	\textbf{\textcolor[HTML]{B22222}{Error}}: This document is in two-column mode. The two-column box is not compatible with this mode. 3:1. Content: \textbf{Column 1:} #1, \textbf{Column 2:} #2
	\else
	\begin{twocolboxN}
		\begin{minipage}[t]{0.74\textwidth}
			\textbf{Column 1:} #1
		\end{minipage}%
		\hfill
		\begin{minipage}[t]{0.24\textwidth}
			\textbf{Column 2:} #2
		\end{minipage}
	\end{twocolboxN}
	\fi
}


\newcommand{\twocolboxKWPR}[2]{
	\if@twocolumn
	\importantsection{Error in Alignment of Text 1:3 KWPR}
	\textbf{\textcolor[HTML]{B22222}{Error}}: This document is in two-column mode. The two-column box is not compatible with this mode. 1:3. Content: \textbf{Column 1:} #1, \textbf{Column 2:} #2
	\else
	\begin{twocolboxN}
		\begin{minipage}[t]{0.24\textwidth}
			\textbf{Column 1:} #1
		\end{minipage}%
		\hfill
		\begin{minipage}[t]{0.74\textwidth}
			\textbf{Column 2:} #2
		\end{minipage}
	\end{twocolboxN}
	\fi
}

\definecolor{codered}{RGB}{220, 50, 47}

\definecolor{codebg}{RGB}{245, 245, 245}

\tcbset{
	mycodebox/.style={
		colback=codebg,
		colframe=black!30,
		boxrule=0.5pt,
		arc=2pt,
		outer arc=2pt,
		boxsep=5pt,
		left=5pt,
		right=5pt,
		top=5pt,
		bottom=5pt,
		enhanced,
		breakable,
		sharp corners,
	}
}

\newcommand{\code}[1]{%
	\begin{tcolorbox}[mycodebox]
		\textcolor{codered}{\texttt{#1}}
	\end{tcolorbox}
}

\definecolor{codered}{RGB}{220, 50, 47}
\definecolor{codebg}{RGB}{245, 245, 245}

\tcbset{highlight code inline/.style={
		enhanced,
		boxsep=0pt,
		sharp corners,
		colback=codebg,
		colframe=codebg,
		boxrule=0pt,
		borderline west={0pt}{0pt}{codebg},
		borderline east={0pt}{0pt}{codebg},
		frame empty,
		interior style={fill=codebg},
		overlay={},
		before upper={\let\item\@item},
		breakable,
		size=fbox,
		box align=base,
		halign=left,
		valign=center,
}}

% Makro für inline-Code mit Umbruch
\newtcbox{\codeIN}{highlight code inline,
	on line,
	left=2pt, right=2pt, top=1pt, bottom=1pt,
	nobeforeafter,
	coltext=codered,
	fontupper=\ttfamily\footnotesize,
}

\newfloat{scheme}{htbp}{los}
\floatname{scheme}{Scheme}
\newfloat{chart}{htbp}{loc}
\floatname{chart}{Chart}
\newfloat{graph}{htbp}{loh}
\floatname{graph}{Graph}
%\newcommand*\schemename{Scheme}
%\newcommand*\chartname{Chart}
%\newcommand*\graphname{Graph}
\floatplacement{table}{htbp}
\floatplacement{figure}{htbp}
\floatstyle{plaintop}
\restylefloat{table}

%\colorlet{structure@color}{black}
%
%\AtEndOfClass{%
%	\colorlet{tbrowcolor}{structure@color!10}
%	\colorlet{tbheadcolor}{structure@color!30}
%	\arrayrulecolor{structure@color}
%}
%
%
%\newcommand{\patchCUPtables}{%
%	\rowcolors*{1}{tbrowcolor}{tbrowcolor}%
%	\setlength{\aboverulesep}{0pt}%
%	\setlength{\belowrulesep}{0pt}%
%	\setlength{\extrarowheight}{.75ex}%
%}
%\AtBeginEnvironment{table}{\patchCUPtables}
%\AtBeginEnvironment{table*}{\patchCUPtables}



\makeatother