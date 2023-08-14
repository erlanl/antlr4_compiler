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
            return float(self.data_variables[ctx.VAR().getText()])
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
            return self.visitExpr(ctx.expr())
        print(self.data_variables)
    
    def visitProgram(self, ctx):
        return self.visitStatement(ctx.statement()[0])
    
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
            self.visitProgram(ctx.program()[0])
            self.visitLoopWhile(ctx)
        elif (ctx.getChild(4)):
            self.visitProgram(ctx.program()[1])

    def visitLoopFor(self, ctx, recursion=False):
        name_variable = ctx.VAR().getText()

        if name_variable not in self.data_variables:
            self.data_variables[name_variable] = self.visitExpr(ctx.expr()[0])
        elif name_variable in self.data_variables and not recursion:
            print(f"Erro de compilação! A variável {name_variable} já existe!")
            exit()
        
        if self.data_variables[name_variable] < int(self.visitExpr(ctx.expr()[1])):
            self.visitProgram(ctx.program()[0])
            self.data_variables[name_variable] += 1
            self.visitLoopFor(ctx, True)
        elif self.data_variables[name_variable] > int(self.visitExpr(ctx.expr()[1])):
            self.visitProgram(ctx.program()[0])
            self.data_variables[name_variable] -= 1
            self.visitLoopFor(ctx, True)


    
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

        if '=' not in input_str:
            result = visitor.visitProgram(tree)
            print("Resultado:", result)
        else:
            visitor.visitProgram(tree)

if __name__ == '__main__':
    main()