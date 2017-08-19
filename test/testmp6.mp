outputformat := "png";
outputformatoptions := "format=rgb";
outputtemplate := "%j-%c.%o";
beginfig(1);
fill (0,0)--(50,0)--(50,50)--(0,50)--cycle withcolor white;
fill fullcircle scaled 15 shifted (30,20) withcolor black;
endfig;
beginfig(2);
fill (0,0)--(50,0)--(50,50)--(0,50)--cycle withcolor white;
fill fullcircle scaled 15 shifted (30,20) withcolor black;
endfig;
end.