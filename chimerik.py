class Execute:
    def __init__(self, names):
        self.names = names

    
    def get_obj_type(_obj):
        return str(type(_obj)).split("'")[1]

    def evaluate(self, tree):
        undefined = "Undefined: Variable {0} hasn't been defined!"
        type_error = "Type Error: You can't use '{op}' with types '{obj1}' and '{obj2}'!"
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
            value = self.evaluate(tree[2])
            name = tree[1]
            self.names[name] = value
            return value

        elif rule == "func_define":
            value = tree[2]
            name = tree[1]
            self.names[name] = value
            return value

        elif rule == 'func_call':
            return self.evaluate(self.names[tree[1]])

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
            return int(self.evaluate(tree[1]) or eself.valuate(tree[2]))


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
        elif rule == 'string':
            return str(tree[1])
        elif rule == 'list':
            results = []
            for i in tree[1][1]:
                results.append(self.evaluate(i))
            return results

        elif rule == 'bool':
            return int(tree[1])

        elif rule == 'name':
            varname = tree[1]
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
            value = self.evaluate(tree[1])
            res = input(value)
            try:
                res = float(res)
            except ValueError:
                pass
            return res
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