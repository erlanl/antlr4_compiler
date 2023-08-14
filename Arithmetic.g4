grammar Arithmetic;

// Regras do Parser
expr: term ( (PLUS | MINUS) term )* ;
term: factor ( (MUL | DIV) factor )* ;
factor: INT | LPAREN expr RPAREN | VAR ;

// Novas Regras do Parser
program: statement+ ;
statement: assignment | expr | commandCond | loopWhile | loopFor;
assignment: VAR ASSIGN expr ;

// Bônus:
commandCond: SE cond ENTAO program (SENAO program)? ;
cond: expr (COMPARISON | DIFFERENT | BEQUAL | LEQUAL | SMALLER | BIGGER) expr ;
loopWhile: ENQUANTO cond ENTAO program (SENAO program)? ;
loopFor: PARA VAR DE expr ATE expr ENTAO program (SENAO program)? ;
function: FUNC VAR ENTAO program ;

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

// Novas Regras do Lexer
ASSIGN: '=' ;

// Bônus
SE: 'se' ;
ENTAO: 'entao' ;
SENAO: 'senao' ;
ENQUANTO: 'enquanto';
PARA: 'para';
ATE: 'ate';
DE: 'de';
FUNC: 'funcao';
COMPARISON: '==' ;
DIFFERENT: '!=' ;
BEQUAL: '>=' ;
LEQUAL: '<=';
SMALLER: '<';
BIGGER: '>' ;
VAR: [a-zA-Z]+;