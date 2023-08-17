from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor(ParseTreeVisitor):
    data_variables = dict()
    
    def visitExpr(self, ctx):
        result = self.visitTerm(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i*2-1).getText() == '+':
                result += self.visitTerm(ctx.term(i))
            else:
                result -= self.visitTerm(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visitFactor(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i*2-1).getText() == '*':
                result *= self.visitFactor(ctx.factor(i))
            else:
                result /= self.visitFactor(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.data_variables:
                var_value = self.data_variables[var_name]
                if isinstance(var_value, int):
                    return var_value
                elif isinstance(var_value, float):
                    return int(var_value) if var_value.is_integer() else var_value
            else:
                raise NameError(f"Variable '{var_name}' is not defined")
        else:
            return self.visitExpr(ctx.expr())

    
    def visitAssignment(self, ctx):
        name = ctx.VAR().getText()
        value = self.visitExpr(ctx.expr())
        self.data_variables[name] = value
        
    def visitStatement(self, ctx):
        if ctx.assignment():
            self.visitAssignment(ctx.assignment())
        elif ctx.commandCond():
            self.visitCommandCond(ctx.commandCond())
        elif ctx.loopWhile():
            self.visitLoopWhile(ctx.loopWhile())
        elif ctx.loopFor():
            self.visitLoopFor(ctx.loopFor())
        else:
            value = self.visitExpr(ctx.expr())
            print(value)
    
    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visitStatement(statement)
    
    def visitCond(self, ctx):
        exp1 = self.visitExpr(ctx.expr()[0])
        op = ctx.getChild(1)
        exp2 = self.visitExpr(ctx.expr()[1])
        return eval(f"{exp1} {op} {exp2}")
    
    def visitCommandCond(self, ctx):
        if self.visitCond(ctx.cond()):
            self.visitProgram(ctx.program()[0])
        elif (ctx.getChild(4)):
            self.visitProgram(ctx.program()[1])     
    
    def visitLoopWhile(self, ctx):
        if self.visitCond(ctx.cond()):
            print("entrou")
            self.visitProgram(ctx.program()[0])
            self.visitLoopWhile(ctx)
        elif (ctx.SENAO()):
            self.visitProgram(ctx.program()[1])

    def visitLoopFor(self, ctx, recursion=False):
        name_variable = ctx.VAR().getText()

        if name_variable not in self.data_variables:
            self.data_variables[name_variable] = self.visitExpr(ctx.expr()[0])
        elif name_variable in self.data_variables and not recursion:
            raise NameError(f"Variable '{name_variable}' already exists")
            
        
        end_value = int(self.visitExpr(ctx.expr()[1]))
        current_value = self.data_variables[name_variable]

        if current_value < end_value:
            self.visitProgram(ctx.program())
            self.data_variables[name_variable] += 1
            self.visitLoopFor(ctx, True)
        elif current_value > end_value:
            self.visitProgram(ctx.program())
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
        visitor.visitProgram(tree)

if __name__ == '__main__':
    main()