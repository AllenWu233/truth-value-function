class Sign:
    # 逻辑运算符符号
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


NOT, AND, OR, IND, EQUAL = Sign('NOT', '¬'), Sign('AND', '∧'), Sign('OR', '∨'), Sign('IND', '→'), Sign('EQUAL', '↔')
value = {  # 运算符优先级
    NOT.symbol: 5,
    AND.symbol: 4,
    OR.symbol: 3,
    IND.symbol: 2,
    EQUAL.symbol: 1
}
symbols = [NOT.symbol, AND.symbol, OR.symbol, IND.symbol, EQUAL.symbol]  # 逻辑运算符符号，便于输入
letters = list('PQRSTUVWXYZABCDEFGHIJKLMNO')  # 命题变元



class Logic:
    # 逻辑运算符的函数表达
    def _not_(self, P):
        return bool(not P)

    def _and_(self, P, Q):
        return bool(P and Q)

    def _or_(self, P, Q):
        return bool(P or Q)

    def _ind_(self, P, Q):
        if P and (not Q):
            return False
        return True

    def _equal_(self, P, Q):
        return bool(P) == bool(Q)

logic = Logic()



class TruthValueFunction:
    
    def __init__(self, function):
        self.function = function  # 公式
        self.value = self.is_truth_value_function()  # 是否为合法的命题公式
        if self.value == True:
            # 命题变元数量
            self.propositional_variable = len(set(self.function.replace(NOT.symbol, '').replace(AND.symbol, '').replace(OR.symbol, '').replace(IND.symbol, '').replace(EQUAL.symbol, '').replace('(', '').replace(')', '')))
            self.truth_table = self.get_truth_table(self.get_postfix_notation())  # 真值表
        else:
            self.propositional_variable = None
            self.truth_table = None


    def __eq__(self, object):
        # 重载运算符“==”
        if self.value == False or object.value == False:
            return False
        return self.truth_table == object.truth_table


    def _check_balance_parentheses(self, s):
        # 检查表达式的括号是否合法
        depth = 0  # 括号层数
        for i in s:
            if i == '(':
                if depth:
                    pass
                depth += 1
            if i == ')':
                if depth == 0:
                    return False
                depth -= 1
        return depth == 0


    def is_truth_value_function(self):
        depth = 0  # 判断最外层括号
        flag1 = False  # 遍历到一个命题变元
        flag2 = False  # 遍历到一个否定联结词
        flag3 = False  # 遍历到一个二元联结词
        for i in range(0, len(self.function)):
            c = self.function[i]
            # 括号成对出现
            if c == '(':
                depth += 1
            elif c == ')':
                if depth == 0:
                    return False
                depth -= 1
            # 至少有一个命题变元（大写字母），且大写字母前一个字符不能为“)”，后一个字符不能为“(”
            elif c.isupper():
                if c != self.function[-1] and self.function[i+1] == '(':
                    return False
                if c != self.function[0] and self.function[i-1] == ')':
                    return False
                # 如果两个命题变元之间没有二元联结词，返回False
                if flag1 and not flag3:
                    return False
                flag1 = True
                flag2 = False  # 否定联结词连接到了一个命题
                flag3 = False  # 二元联结词连接到了两个命题
            elif c == NOT.symbol:
                flag2 = True 
            # 二元联结词前后分别至少至少有一个命题变元（大写字母）
            elif c in symbols:
                if not flag1:
                    return False
                flag3 = True
            else:
                return False
        #  括号不成对 or 不含命题变元 or 否定联结词后无命题变元 or 二元联结词后无命题变元
        if depth != 0 or (not flag1) or flag2 or flag3:
            return False
        return True


    def get_postfix_notation(self):
        # 把命题公式转换成后缀表达式
        postn = [self.function]
        finish = False
        while finish == False:

            # 打印转换过程
            # print(postn, '\n')

            finish = True
            for i in range(len(postn)):
                s1 = postn[i]
                if len(s1) > 1:  # 最终使得列表中所有元素长度为1
                    finish = False
                if not finish and len(s1) > 1:  # 处理长度大于1的元素
                    Min = 100  # 用于判断优先级最低的运算
                    depth = 0  # 括号嵌套层数，用于判断最外层括号
                    # 找出运算级最低的符号
                    for j in range(len(s1)):
                        s2 = s1[j]
                        if s2 == '(':
                            depth += 1
                        elif s2 == ')':
                            depth -= 1
                        elif s2 in symbols and depth == 0:  # 把最外层括号内的看作一个命题变元
                            if Min > value[s2]:
                                Min = value[s2]  # 优先级最低的运算符的优先级
                                ptr = j  # 指针指向优先级最低的运算符
                        else:
                            pass

                    if Min == 100:  # 最外层为可去的括号
                        postn[i] = postn[i][1:-1]
                    elif Min == value[NOT.symbol]:
                        s11 = s1[ptr+1:]
                        postn = postn[:i] + [s11, s1[ptr]] + postn[i+1:]  # 后缀表达式
                    else:
                        s11 = s1[:ptr]
                        s12 = s1[ptr+1:]
                        postn = postn[:i] + [s11, s12, s1[ptr]] + postn[i+1:]  # 后缀表达式
                    break  # 很关键！处理完一个元素后从头开始遍历func列表
        return postn


    def get_truth_table(self, postn):
        # 由后缀表达式计算出真值表
        stack, truth_table = [], []  # 栈用于后缀表达式求值
        # 处理后缀表达式，得出计算式
        func = ""
        for i in postn:
            if i.isupper():
                stack.append(i)
            elif i == NOT.symbol:
                func = f"logic._not_({stack.pop()})"
                stack.append(func)
            else:
                Q = stack.pop()
                P = stack.pop()
                if i == AND.symbol:
                    func = f"logic._and_({P}, {Q})"
                elif i == OR.symbol:
                    func = f"logic._or_({P}, {Q})"
                elif i == IND.symbol:
                    func = f"logic._ind_({P}, {Q})"
                else:
                    func = f"logic._equal_({P}, {Q})"
                stack.append(func)
        # 遍历解释，计算真值
        for i in range(1 << self.propositional_variable):
            s = str(bin(i))[2:]
            explation = (self.propositional_variable - len(s)) * '0' + s
            f = func
            for j in range(self.propositional_variable):  # 代入解释
                f = f.replace(letters[j], explation[j])
            truth_table.append(eval(f))

        # 打印转换结果
        # print(postn)

        return truth_table



class TruthValueFunction3(TruthValueFunction):

    def __init__(self, function):
        super(TruthValueFunction3, self).__init__(function)
        # 规定为只含三个命题变元的命题公式
        if len(set(self.function.replace(NOT.symbol, '').replace(AND.symbol, '').replace(OR.symbol, '').replace(IND.symbol, '').replace(EQUAL.symbol, '').replace('(', '').replace(')', ''))) != 3:
            self.value = False
        self.__minterm = [
            f"{NOT.symbol}P{AND.symbol}{NOT.symbol}Q{AND.symbol}{NOT.symbol}R",
            f"{NOT.symbol}P{AND.symbol}{NOT.symbol}Q{AND.symbol}R",
            f"{NOT.symbol}P{AND.symbol}Q{AND.symbol}{NOT.symbol}R",
            f"{NOT.symbol}P{AND.symbol}Q{AND.symbol}R",
            f"P{AND.symbol}{NOT.symbol}Q{AND.symbol}{NOT.symbol}R",
            f"P{AND.symbol}{NOT.symbol}Q{AND.symbol}R",
            f"P{AND.symbol}Q{AND.symbol}{NOT.symbol}R",
            f"P{AND.symbol}Q{AND.symbol}R"
        ]
        self.__maxterm = [
            f"P{OR.symbol}Q{OR.symbol}R",
            f"P{OR.symbol}Q{OR.symbol}{NOT.symbol}R",
            f"P{OR.symbol}{NOT.symbol}Q{OR.symbol}R",
            f"P{OR.symbol}{NOT.symbol}Q{OR.symbol}{NOT.symbol}R",
            f"{NOT.symbol}P{OR.symbol}Q{OR.symbol}R",
            f"{NOT.symbol}P{OR.symbol}Q{OR.symbol}{NOT.symbol}R",
            f"{NOT.symbol}P{OR.symbol}{NOT.symbol}Q{OR.symbol}R",
            f"{NOT.symbol}P{OR.symbol}{NOT.symbol}Q{OR.symbol}{NOT.symbol}R"
        ]
        if self.value == True:
            self.principal_disjunction_normal_form = self.get_principal_disjunction_normal_form()
            self.principal_conjunction_normal_form = self.get_principal_conjunction_normal_form()
        else:
            self.principal_disjunction_normal_form = None
            self.principal_conjunction_normal_form = None


    def get_principal_disjunction_normal_form(self):
        # 根据真值表得到主析取范式
        f = ""
        for i in range(1 << self.propositional_variable):
            if self.truth_table[i] == True:
                if f == "":
                    f += f"({self.__minterm[i]})"
                else:
                    f += f"{OR.symbol}({self.__minterm[i]})"
        if f == "":
            return None
        return f


    def get_principal_conjunction_normal_form(self):
        # 根据真值表得到主合取范式
        f = ""
        for i in range(1 << self.propositional_variable):
            if self.truth_table[i] == False:
                if f == "":
                    f += f"({self.__maxterm[i]})"
                else:
                    f += f"{AND.symbol}({self.__maxterm[i]})"
        if f == "":
            return None
        return f



if __name__ == '__main__':
    flag1 = True
    flag2 = True

    def test1(s):
        global case
        G = TruthValueFunction(s)
        case += 1
        print(f"Case: {case}")
        print(G.function)
        print("合法命题公式:", G.value)
        print("命题变元数:", G.propositional_variable)
        print("真值表:", G.truth_table)
        print("")

    functions = [
        f"{NOT.symbol}P", 
        f"P{AND.symbol}Q", 
        f"P{OR.symbol}Q", 
        f"P{IND.symbol}Q", 
        f"P{EQUAL.symbol}Q", 
        f"P{AND.symbol}Q", 
        f"P{AND.symbol}Q{AND.symbol}R",
        NOT.symbol + 'P' + OR.symbol + 'Q', 
        f"{NOT.symbol}(P{OR.symbol}Q){AND.symbol}(R{IND.symbol}S){EQUAL.symbol}T", 
        'P' + OR.symbol + 'Q' + AND.symbol  + 'R', 
        "(P∧Q∧R)",
        "(P→(Q∧R))∨(R↔S)", 
        "()P→Q∨R∧S", 
        "¬P∨Q∧R→S",
        "∧Q∨¬R",
    ]
    case = 0
    if flag1:
        for i in functions:
            test1(i)



    def test2(s):
        global case
        G = TruthValueFunction3(s)
        case += 1
        print(f"Case: {case}")
        print(G.function)
        print("合法命题公式（只含三个命题变元）:", G.value)
        print("命题变元数:", G.propositional_variable)
        print("真值表:", G.truth_table)

        G1 = TruthValueFunction3(G.principal_disjunction_normal_form)
        G2 = TruthValueFunction3(G.principal_conjunction_normal_form)
        print("主析取范式:", G1.function)
        print(G1.truth_table)
        print("主合取范式:", G2.function)
        print(G2.truth_table)

        print(G == G1)
        print(G == G2)
        print("")


    case = 0
    functions3 = [
        f"P{AND.symbol}(Q{IND.symbol}R)",
        f"P{AND.symbol}Q{AND.symbol}R",
        "(P∧Q∧R)",
        "(P∨Q∨R)∧(P∨Q∨¬R)∧(P∨¬Q∨R)∧(P∨¬Q∨¬R)∧(¬P∨Q∨R)∧(¬P∨Q∨¬R)∧(¬P∨¬Q∨R)",
    ]
    if flag2:
        for _ in range(100):
            print('=', end="")
        print("\n")
        for i in functions3:
            test2(i)
