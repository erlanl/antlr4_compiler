grammar Arithmetic;

// Regras do Parser
expr: term ( (PLUS | MINUS) term )* ;
term: factor ( (MUL | DIV) factor )* ;
factor: INT | LPAREN expr RPAREN | VAR ;
program: statement+ ;
statement: assignment | expr | commandCond | loopWhile | loopFor ;
assignment: VAR ASSIGN expr ;
commandCond: SE cond LBRACK program RBRACK (SENAO LBRACK program RBRACK)? ;
cond: expr (COMPARISON | DIFFERENT | BEQUAL | LEQUAL | SMALLER | BIGGER) expr ;
loopWhile: ENQUANTO cond LBRACK program RBRACK (SENAO LBRACK program RBRACK)? ;
loopFor: PARA VAR DE expr ATE expr LBRACK program RBRACK ;

// Regras do Lexer
PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
INT: [0-9]+ ;
LPAREN: '(' ;
RPAREN: ')' ;
LBRACK: '{' ;
RBRACK: '}' ;
WS: [ \t\r\n]+ -> skip ;
ASSIGN: '=' ;
SE: 'se' ;
SENAO: 'senao' ;
ENQUANTO: 'enquanto';
PARA: 'para';
ATE: 'ate';
DE: 'de';
COMPARISON: '==' ;
DIFFERENT: '!=' ;
BEQUAL: '>=' ;
LEQUAL: '<=';
SMALLER: '<';
BIGGER: '>' ;
VAR: [a-zA-Z]+;