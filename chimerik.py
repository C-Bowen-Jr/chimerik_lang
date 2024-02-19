class Execute:
    def __init__(self, names):
        self.names = names
        self.scopes = {}
        self.type_map = {"bool": "zviisida", "int": "intach", "float": "esach", "str": "tonabich"}
    
    def get_obj_type(self, _obj):
        return str(type(_obj)).split("'")[1]

    def evaluate(self, tree):
        undefined = "Undefined: Variable {0} hasn't been defined!"
        type_error = "Type Error: You can't use '{op}' with types '{obj1}' and '{obj2}'!"
        assign_error = "Assignment Error: You can't assign '{obj1}' to '{obj2}' typed variable!"
        op_mismatch = "Operand Mismatch: You can't use '{op}' with type '{obj}'!"

        try:
            rule = tree[0]
        except TypeError:
            return print("Parsed tree contains something invalid.")

        if rule == 'main':
            self.evaluate(tree[1])
        elif rule == 'statements':
            results = []
            for i in tree[1]:
                results.append(self.evaluate(i))
            return results
        elif rule == 'statement-expr':
            value = self.evaluate(tree[1])
            return value

        elif rule == 'assign':
            value = self.evaluate(tree[3])
            value_py_type = self.get_obj_type(value)
            if self.type_map[value_py_type] != tree[2]:
                return print(assign_error.format(obj1=self.type_map[value_py_type], obj2=tree[2]))    
            
            name = tree[1]
            self.names[name] = value
            return value

        elif rule == "func_define":
            params = None if len(tree) <= 3 else tree[3][1]
            value = tree[2]
            name = tree[1]
            #self.names[name] = value
            self.names[name] = {'params': params, 'body': value}
            return value

        elif rule == 'func_call':
            args = None if len(tree) <= 2 else tree[2][1]
            name = tree[1]
            func_info = self.names[name]
            params = func_info['params']
            body = func_info['body']
            local_scope = {}

            if args != None:
                for param, arg in zip(params, args):
                    if isinstance(arg, tuple) and arg[0] == 'assign':
                        arg_name = arg[1]
                        arg_value = self.evaluate(arg[2])
                        local_scope[arg_name] = arg_value
                    else:
                        local_scope[param[1]] = self.evaluate(arg)
            
                # chatGPT Madness, some similarity to gh.com/SniperRacc/vappy, so maybe accurate?
                temp_scope = self.scopes.copy()
                temp_scope.update(local_scope)
                self.scopes = temp_scope

                results = self.evaluate(body)
                self.scopes = self.scopes.copy()
                return results
            else:
                return self.evaluate(body)

        elif rule == 'times':
            multiplier = self.evaluate(tree[1])
            multiplicand = self.evaluate(tree[2])
            try:
                return multiplier * multiplicand
            except TypeError:
                return print(type_error.format(op="*", obj1=get_obj_type(multiplier), obj2=get_obj_type(multiplicand)))
        elif rule == 'plus':
            addend1 = self.evaluate(tree[1])
            addend2 = self.evaluate(tree[2])
            try:
                return addend1 + addend2
            except TypeError:
                return print(type_error.format(op="+", obj1=get_obj_type(addend1), obj2=get_obj_type(addend2)))
        elif rule == 'minus':
            minuend = self.evaluate(tree[1])
            subtrahend = self.evaluate(tree[2])
            try:
                return minuend - subtrahend
            except TypeError:
                return print(type_error.format(op="-", obj1=get_obj_type(minuend), obj2=get_obj_type(subtrahend)))
        elif rule == 'divide':
            dividend = self.evaluate(tree[1])
            divisor = self.evaluate(tree[2])
            try:
                return dividend / divisor
            except TypeError:
                return print(type_error.format(op="/", obj1=get_obj_type(dividend), obj2=get_obj_type(divisor)))
        elif rule == 'mod':
            a = self.evaluate(tree[1])
            n = self.evaluate(tree[2])
            try:
                return a % n
            except TypeError:
                return print(type_error.format(op="%", obj1=get_obj_type(a), obj2=get_obj_type(n)))
        elif rule == 'pow':
            target_num = self.evaluate(tree[1])
            exponent = self.evaluate(tree[2])
            try:
                return target_num ** exponent
            except TypeError:
                return print(type_error.format(op="^", obj1=get_obj_type(target_num), obj2=get_obj_type(exponent)))
    
        elif rule == 'equals':
            return int(self.evaluate(tree[1]) == self.evaluate(tree[2]))
        elif rule == 'ne':
            return int(self.evaluate(tree[1]) != self.evaluate(tree[2]))
        elif rule == 'gt':
            return int(self.evaluate(tree[1]) > self.evaluate(tree[2]))
        elif rule == 'lt':
            return int(self.evaluate(tree[1]) < self.evaluate(tree[2]))
        elif rule == 'and':
            return int(self.evaluate(tree[1]) and self.evaluate(tree[2]))
        elif rule == 'or':
            return int(self.evaluate(tree[1]) or self.valuate(tree[2]))


        elif rule == 'uminus':
            return -self.evaluate(tree[1])
        elif rule == 'inc':
            name = tree[1]

            try:        
                oldval = self.names[tree[1]]
            except KeyError:
                return print(undefined.format(name))        
            newval = oldval + 1
        
            self.names[name] = newval
            return newval
        elif rule == 'dec':
            name = tree[1]
            try:        
                oldval = self.names[tree[1]]
            except KeyError:
                return print(undefined.format(name)) 

            newval = oldval - 1
        
            self.names[name] = newval
            return newval
        elif rule == 'number':
            try:
                return int(tree[1])
            except ValueError:
                return float(tree[1])
        elif rule == 'float':
            return float(tree[1])
        elif rule == 'string':
            formatted = str(tree[1])
            for var in self.names:
                formatted = formatted.replace(f"{{{var}}}", str(self.names[var]))
            return formatted
        elif rule == 'list':
            results = []
            for i in tree[1][1]:
                results.append(self.evaluate(i))
            return results

        elif rule == 'bool':
            return bool(tree[1])

        elif rule == 'name':
            varname = tree[1]
            try:
                return self.scopes[varname]
            except KeyError:
                pass
            try:
                return self.names[varname]
            except KeyError:
                print(undefined.format(varname))
        elif rule == 'index':
            op = self.evaluate(tree[1])
            index = self.evaluate(tree[2])
            try:
                return op[index]
            except IndexError as e:
                print(f'Index error: {e}')
            except TypeError as e:
                print(f'Type Error: Only lists and strings can be indexed')
        elif rule == 'paren':
            return self.evaluate(tree[1])

        elif rule == 'pass':
            pass
        elif rule == 'break':
            return Break()
        elif rule == 'print':
            value = self.evaluate(tree[1])
            print(value)
            return value
        elif rule == 'input':
            output = self.evaluate(tree[3])
            res = input(output)
            assignType = 'string'

            try:
                value = float(res)
                # valid int assigning to int, otherwise float even if coerced
                if value.is_integer() and tree[2] == 'intach':
                    value = int(value)
                    assignType = 'number'
                else:
                    assignType = 'float'
                
            except:
                value = res
            
            if tree[2] == 'intach' and assignType != 'number':
                print(f"Failed to assign intach, got {assignType}")
            elif tree[2] == 'esach' and assignType != 'float':
                print(f"Failed to assign esach, got {assignType}")
            elif tree[2] == 'tonabich' and assignType != 'string': 
                print(f"Failed to assign tonabich, got {assignType}")
            
            return self.evaluate(('assign', tree[1], tree[2], ('statement-expr', (assignType, value))))
        elif rule == 'if-elif-else':
            expr1 = self.evaluate(tree[1])
            expr2 = None if tree[3] is None else eself.valuate(tree[3])
            if expr1:
                return self.evaluate(tree[2])
            elif expr2:
                return self.evaluate(tree[4])
            else:
                if tree[5]:
                    return self.evaluate(tree[5])
                else:
                    pass
        elif rule == 'while':
            while self.evaluate(tree[1]):
                results = self.evaluate(tree[2])
            
                if any([isinstance(res,Break) for res in results]):
                    break
        else:
            #print(rule, tree)
            pass
class Break:
    pass