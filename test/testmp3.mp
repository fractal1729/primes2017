outputformat := "png";
outputtemplate := "%j.%o";
prologues:=3;
verbatimtex
%&latex
\documentclass{minimal}
\begin{document}
etex
beginfig(0);
draw (20,20)--(0,0)--(0,30)--(30,0)--(0,0);
endfig;
end