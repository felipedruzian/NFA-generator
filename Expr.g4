grammar Expr;

prog: expr EOF ;

expr: atomic
    | expr expr
    | expr '|' expr
    | expr '*'
    ;

atomic: '(' expr ')'
      | symbol
      ;

symbol: '0'
      | '1'
      ;

WS: [ \t\r\n]+ -> skip;
