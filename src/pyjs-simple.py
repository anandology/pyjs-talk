import ast
import compiler
from cStringIO import StringIO

class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.indent = 0
        self.buf = None
        
    def translate(self, node):
        self.buf = StringIO()
        self.visit(node)
        return self.buf.getvalue()

    def write(self, line, indent=False):
        if indent:
            self.buf.write("    " * self.indent)
        self.buf.write(line)
        return self
    
    def write_block(self, node):
        self.indent += 1
        self.visit(node)
        self.indent -= 1
        
    def generic_visit(self, node):
        for n in node.getChildNodes():
            self.visit(n)

    def visit_Add(self, node):
        self.visit(node.left)
        self.write(" + ")
        self.visit(node.right)

    def visit_Mul(self, node):
        self.visit(node.left)
        self.write(" * ")
        self.visit(node.right)
        
    def visit_Name(self, node):
        names = {
            "True": "true",
            "False": "false",
            "None": "nil"
        }
        name = names.get(node.name, node.name)
        self.write(name)
    
    def visit_Const(self, node):
        self.write(repr(node.value))        

    def visit_If(self, node):
        test, code = node.tests[0]
        self.write("if (", indent=True)
        self.visit(test)
        self.write(") {\n")
        self.write_block(code)
        self.write("}\n", indent=True)

    def visit_Function(self, node):
        self.write("function %s(%s) {\n" % (node.name, ", ".join(node.argnames)), indent=True)
        self.write_block(node.code)
        self.write("}\n", indent=True)

    def visit_Return(self, node):
        self.write("return", indent=True)
        if node.value:
            self.write(" ")
            self.visit(node.value)
        self.write(";\n")

    def visit_Or(self, node):
        self.join(node.nodes, " || ")

    def join(self, nodes, delim):
        if nodes:
            self.visit(nodes[0])
            for n in nodes[1:]:
                self.write(delim)
                self.visit(n)
    
    def visit_Compare(self, node):
        self.visit(node.expr)
        for op, n in node.ops:
            self.write(" " + op + " ")
            self.visit(n)      
    
    def visit_CallFunc(self, node):
        self.visit(node.node)
        self.write("(")
        self.join(node.args, ", ")
        self.write(")")          
        
def main(filename):
    code = open(filename).read()
    _ast = compiler.parse('""\n' + code)
    print Visitor().translate(_ast)
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1])