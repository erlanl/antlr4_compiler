from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:	
    data_variables = dict()

    def visit(self, ctx):	
        if isinstance(ctx, ArithmeticParser.ExprContext):	
            return self.visitExpr(ctx)	
        elif isinstance(ctx, ArithmeticParser.TermContext):	
            return self.visitTerm(ctx)	
        elif isinstance(ctx, ArithmeticParser.FactorContext):	
            return self.visitFactor(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            self.visitAssignment(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.ProgramContext):
            self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.CondContext):
            return self.visitCond(ctx)
        elif isinstance(ctx, ArithmeticParser.CommandCondContext):
            self.visitCommandCond(ctx)
        elif isinstance(ctx, ArithmeticParser.LoopWhileContext):
            self.visitLoopWhile(ctx)
        elif isinstance(ctx, ArithmeticParser.LoopForContext):
            self.visitLoopFor(ctx)
        
    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i*2-1).getText() == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i*2-1).getText() == '*':
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.data_variables:
                return int(self.data_variables[var_name])
            else:
                raise NameError(f"Variable '{var_name}' is not defined")
        else:
            return self.visit(ctx.expr())

    def visitAssignment(self, ctx):
        name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.data_variables[name] = value
        
    def visitStatement(self, ctx):
        if ctx.assignment():
            self.visit(ctx.assignment())
        elif ctx.commandCond():
            self.visit(ctx.commandCond())
        elif ctx.loopWhile():
            self.visit(ctx.loopWhile())
        elif ctx.loopFor():
            self.visit(ctx.loopFor())
        else:
            value = self.visit(ctx.expr())
            print(value)
    
    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)
    
    def visitCond(self, ctx):
        exp1 = self.visit(ctx.expr()[0])
        op = ctx.getChild(1)
        exp2 = self.visit(ctx.expr()[1])
        return eval(f"{exp1} {op} {exp2}")
    
    def visitCommandCond(self, ctx):
        if self.visit(ctx.cond()):
            self.visit(ctx.program()[0])
        elif (ctx.SENAO()):
            self.visit(ctx.program()[1])     
    
    def visitLoopWhile(self, ctx):
        if self.visit(ctx.cond()):
            self.visit(ctx.program()[0])
            self.visitLoopWhile(ctx)
        elif (ctx.SENAO()):
            self.visit(ctx.program()[1])

    def visitLoopFor(self, ctx, recursion=False):
        name_variable = ctx.VAR().getText()

        if name_variable not in self.data_variables:
            self.data_variables[name_variable] = self.visit(ctx.expr()[0])
        elif name_variable in self.data_variables and not recursion:
            raise NameError(f"Variable '{name_variable}' already exists")
            
        
        end_value = int(self.visit(ctx.expr()[1]))
        current_value = self.data_variables[name_variable]

        if current_value < end_value:
            self.visit(ctx.program())
            self.data_variables[name_variable] += 1
            self.visitLoopFor(ctx, True)
        elif current_value > end_value:
            self.visit(ctx.program())
            self.data_variables[name_variable] -= 1
            self.visitLoopFor(ctx, True)
        else:
            del self.data_variables[name_variable]

    
def main():
    visitor = ArithmeticVisitor()
    
    while True:
        input_str = input("Digite uma expressão aritmética ou comando (ou 'sair' para encerrar): ")
        
        if input_str == 'sair':
            break
        
        lexer = ArithmeticLexer(InputStream(input_str))
        stream = CommonTokenStream(lexer)
        parser = ArithmeticParser(stream)
        tree = parser.program()
        visitor.visit(tree)

if __name__ == '__main__':
    main()