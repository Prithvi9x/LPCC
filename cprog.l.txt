%{
#include<stdio.h>
%}

%%
"#include"              { printf("%s : Preprocessor Directive\n", yytext); }

\<[a-zA-Z0-9\.]+>       { printf("%s : Header File\n", yytext); }

(int|float|char|double|if|else|while|for|return|void) 	{ printf("%s : Keyword\n", yytext); }

[0-9]+                  { printf("%s : Number\n", yytext); }

[a-zA-Z_][a-zA-Z0-9_]*  { printf("%s : Identifier\n", yytext); }

(\+|\-|\*|\/|==|!=|<=|>=|=|<|>)  { printf("%s : Operator\n", yytext); }

(\(|\)|\{|\}|\;|\,) 	{ printf("%s : Delimiter\n", yytext); }

[ \t\n]+                ;
.                       { printf("%s : Unknown\n", yytext); }
%%

int main()
{
    printf("Enter C program:\n");
    yylex();
    return 0;
}

int yywrap()
{
    return 1;
}