#
# Copyright (c) 2018-2019 Innokentiy Kumshayev <kumshkesh@gmail.com>
# Copyright (c) 2018-2019 IRI, Columbia University
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
import ply.lex as lex

class ODKewaLexer(object):
   # List of token names.   This is always required
   reserved = {
         'and': 'AND',
         'or': 'OR',
         'not': 'NOT'
   }

   tokens = [
      'PLUS',
      'MINUS',
      'TIMES',
      'DIVIDE',
      'LPAREN',
      'RPAREN',
      'COMMA',
      'DOT',
      'DOTDOT',
      'EXCLAMATION',
      'EQUAL',
      'NOT_EQUAL',
      'GREATER',
      'LESS',
      'GREATEROREQ',
      'LESSOREQ',
      'IDENTIFIER',
      'NUMBER', 
      'STRING',
      'VAR',
   ] + list(reserved.values())

   # Regular expression rules for simple tokens
   t_PLUS         = r'\+'
   t_MINUS        = r'-'
   t_TIMES        = r'\*'
   t_DIVIDE       = r'/'
   t_LPAREN       = r'\('
   t_RPAREN       = r'\)'
   t_COMMA        = r','
   t_DOT          = r'\.'
   # t_DOTDOT       = r'\.\.'
   t_EXCLAMATION  = r'\!'
   t_EQUAL        = r'\='
   t_NOT_EQUAL    = r'\!\='
   t_GREATER      = r'\>'
   t_LESS         = r'\<'
   t_GREATEROREQ  = r'\>\='
   t_LESSOREQ     = r'\<\='
   
   def t_IDENTIFIER(self, t):
      r'[a-zA-Z_][a-zA-Z0-9_]*'
      t.type = {  'and': 'AND',
                  'or': 'OR',
                  'not': 'NOT'
               }.get(t.value,'IDENTIFIER')
      return t

   # A regular expression rule with some action code
   def t_NUMBER(self, t):
      r'-?\d+(\.\d*)?'
      try:
         t.value = int(t.value)
      except ValueError:
         t.value = float(t.value)    
      return t

   def t_STRING(self, t):
      r"'[^']*'"
      t.value = t.value[1:-1]
      return t

   def t_VAR(self, t):
      r"\$\{[a-zA-Z_]([a-zA-Z0-9_]*)?\}"
      t.value = t.value[2:-1]
      return t

   # Define a rule so we can track line numbers
   def t_newline(self, t):
      r'\n+'
      t.lexer.lineno += len(t.value)

   # A string containing ignored characters (spaces and tabs)
   t_ignore  = ' \t'

   # Error handling rule
   def t_error(self, t):
      print("Illegal character '%s'" % t.value[0])
      t.lexer.skip(1)

    # Build the lexer
   def build(self,**kwargs):
      self.lexer = lex.lex(module=self, **kwargs)

   def input(self, data):
      return self.lexer.input(data)

   def token(self):
      return self.lexer.token()

   # Test it output
   def test(self,data):
      self.input(data)
      while True:
         tok = self.token()
         if not tok: 
            break
         print(tok.type, tok.value)

if __name__ == '__main__':
   # Build the lexer and try it out
   m = ODKewaLexer()
   m.build()           # Build the lexer
   print("first a simple test:\n")
   m.test("3 + 4 abcde not")
   print("\n\nand next a list of tokens:\n")     # Test it
   m.tokenize("3 + 4 abcde != $ not")
