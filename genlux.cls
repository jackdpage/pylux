%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Copyright (c) 2015 Jack Page                                            %
%  Copyright (c) 2011 Trey Hunner                                          %
%                                                                          %
%  Permission is hereby granted, free of charge, to any person obtaining   %
%  a copy of this software and associated documentation files (the         %
%  "Software"), to deal in the Software without restriction, including     %
%  without limitation the rights to use, copy, modify, merge, publish,     %
%  distribute, sublicense, and/or sell copies of the Software, and to      %
%  permit persons to whom the Software is furnished to do so, subject to   %
%  the following conditions:                                               %
%                                                                          %
%  The above copyright notice and this permission notice shall be          %
%  included in all copies or substantial portions of the Software.         %
%                                                                          %
%  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         %
%  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF      %
%  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                   %
%  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE  %
%  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION  %
%  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION   %
%  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.         %
%                                                                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProvidesClass{genlux}

\LoadClass[12pt]{article}

\usepackage[a4paper,hmargin=0.79in,vmargin=0.79in]{geometry}
\usepackage[parfill]{parskip} % Do not indent paragraphs
\usepackage{longtable}

\pagestyle{empty} % No page numbers
\linespread{1.5} % Line spacing

\setlength{\doublerulesep}{\arrayrulewidth} % Double rules look like one thick one

% Start a new dimmer entry
\newcommand{\dimmer}[1]{
    \textbf{Dimmer: #1}
    \\
}

% Power counter
\newcounter{power} \newcounter{subpower}
\setcounter{power}{0} \setcounter{subpower}{0}

% Create the report table
\newenvironment{reportTable}{

    \newcommand{\fixture}[4]{%
         \addtocounter{power}{##4}%
             \addtocounter{subpower}{##4}%
         ##1 & ##2 & ##3 & ##4W
         \\
    }

    \newcommand{\subtotal}{
        \hline
        {\bf Dimmer Power} & & & {\bf \arabic{subpower}W}
        \setcounter{subpower}{0}
        \\*[1.5ex]
    }

    \renewcommand{\tabcolsep}{0.8ex}
    \setlength\LTleft{0pt}
    \setlength\LTright{0pt}
    \begin{longtable}{@{\extracolsep{\fill}\hspace{\tabcolsep}} l r r r }
    \hline
    {\bf Fixture Type} & \multicolumn{1}{c}{\bf DMX Address} & \multicolumn{1}{c}{\bf Circuit} & \multicolumn{1}{c}{\bf Power} \\*
    \hline\hline
    \endhead
}{
    \hline\hline\hline
    {\bf Total Power} & & & {\bf \arabic{power}W} \\
    \end{longtable}
}
