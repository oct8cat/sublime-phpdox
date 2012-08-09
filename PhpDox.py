import sublime, sublime_plugin
import re

syntax_list = {
    "PHP": True
}

class PhpdoxCommand(sublime_plugin.TextCommand):

    patterns = {
        'class': r"""
            ^\s*                                        # indent
            class\s+                                    # "class" in the beginning of line
            (?P<c_name>\w+)                             # class name
            (
                \s*$                                    # line end
                |\s+extends\s+(?P<pc_name>\w+)          # or "extends" followed by parent class name
            )
        """,
        'function': r"""
            ^\s*                                        # indent
            (?P<access>public|protected|private|var)\s* # access
            (?P<static>static|)\s*                      # static modifier
            function\s                                  # "function"
            (?P<name>\w+)\s*                            # name
            \((?P<params>.*)\)                          # parameters
            .*
        """,
        'var': r"""
            ^\s*                                        # indent
            (?P<access>public|protected|private|)\s*    # access
            (?P<static>static|)\s*                      # static modifier
            (?P<name>\$\w+)\s*                          # name
            (\s*=\s*|)
            (?P<value>.*|);                             # value
            .*
        """,
    }

    def run(self, edit, **args):
        v = self.view
        line = v.line(v.sel()[0])
        snippet = self.process_line(v.substr(line))
        if (snippet != None):
            v.run_command('move', {'by': 'lines', 'forward': False})
            v.run_command('insert_snippet', {'contents': snippet})

    def process_line(self, line):
        for p_name, p_string in self.patterns.iteritems():
            pattern = re.compile(p_string, re.VERBOSE)
            match = pattern.search(line)
            if (match != None):
                method = getattr(self, 'dox_' + p_name)
                return method(match)
        return None

    def dox_class(self, match):
        c_name, pc_name = match.group('c_name', 'pc_name')
        snippet =  '/**\n'
        snippet += ' * ${1:' + c_name + '}.\n'
        snippet += ' *\n'
        if (pc_name != None):
            snippet += ' * @uses     ' + pc_name +'\n'
            snippet += ' *\n'
        snippet += ' * @category ${2:Category}\n'
        snippet += ' * @package  ${3:Package}\n'
        snippet += ' * @author   ${TM_FULLNAME} <${TM_EMAIL}>\n'
        snippet += ' * @license  ${TM_LICENSE}\n'
        snippet += ' * @link     http://www.example.com/\n'
        snippet += ' **/'
        return snippet

    def dox_function(self, match):
        access, static, name, params = match.group('access', 'static', 'name', 'params')
        if (access == ''):
            access = 'public'
        snippet =  '/**\n'
        snippet += ' * ${1:' + name + '}.\n'
        snippet += ' *\n'
        if (params != ''):
            # TODO parameters alignment
            for param in params.split(','):
                param = param.replace(' ', '')
                p_name, eq, initial = param.replace(' ', '').partition('=')
                p_type = self.resolve_var_type(initial)
                snippet += ' * @param ' + p_type + ' \\' + p_name + ' Description.\n'
            snippet += ' *\n'

        snippet += ' * @access ' + access + '\n'
        if (static != ''):
            snippet += ' * @static\n'
        snippet += ' *\n'
        snippet += ' * @return mixed Value.\n'
        snippet += ' **/'
        return snippet

    def dox_var(self, match):
        access, static, name, value = match.group('access', 'static', 'name', 'value')
        type = self.resolve_var_type(value)
        if (access == ''):
            access = 'public'
        snippet =  '/**\n'
        snippet += ' * ${1:\\' + name + '}.\n'
        snippet += ' *\n'
        snippet += ' * @var ' + type + '\n'
        snippet += ' *\n'
        snippet += ' * @access ' + access + '\n'
        if (static != ''):
            snippet += ' * @static\n'
        snippet += ' **/'
        return snippet

    def resolve_var_type(self, var):
        type = 'mixed'
        if (var == 'array()'):
            type = 'array'
        elif (var.isdigit()):
            type = 'int'
        return type
