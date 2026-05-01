%{
#include<stdio.h>
%}

%%
(I|You|He|She|My|They|We)        { printf("%s : Pronoun\n", yytext); }
(a|an|the|The|A|An) 		 { printf("%s: Article\n", yytext); }
(run|eat|drive|write|read|play|walk)  { printf("%s : Verb\n", yytext); }
(big|small|happy|fast|beautiful)      { printf("%s : Adjective\n", yytext); }
(quickly|slowly|silently|well)        { printf("%s : Adverb\n", yytext); }
(and|or|but)                 { printf("%s : Conjunction\n", yytext); }
(in|on|at|under|over|with)   { printf("%s : Preposition\n", yytext); }
[A-Z][a-z]*                  { printf("%s : Proper Noun\n", yytext); }
(cat|dog|boy|girl|teacher|car|city|apple)   { printf("%s : Noun\n", yytext); }
[a-z]+                       { printf("%s : Unknown word\n", yytext); }
[ \t\n]+                     ;
.                            ;
%%

int main()
{
    printf("Enter a sentence:\n");
    yylex();
    return 0;
}

int yywrap()
{
    return 1;
}
