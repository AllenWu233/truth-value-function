/*
规律：
1.括号成对出现
2.至少有一个命题变元（大写字母）
3.命题变元（大写字母）后一个字符不能为“（”
4.否定联结词（¬）后至少有一个命题变元（大写字母）
5.二元联结词前后分别至少至少有一个命题变元（大写字母）
*/
#define NOT "¬"
#define AND "∧"
#define OR "∨"
#define IND "→"
#define EQUAL "↔"
#include <iostream>
#include <string>
#include <stack>
using namespace std;

const string connectives[5] = {NOT, AND, OR, IND, EQUAL};


bool is_binary_connective(string s) {
    for (int i = 1; i < 5; i++) {
        if (s == connectives[i]) {
            return true;
        }
    }
    return false;
}

bool is_truth_value_function(string s) {
    int len = s.length();
    stack<string> st;
    st.push("#");  // 栈底元素，判断是否到栈底
    bool flag1 = false;  // 遍历到一个命题变元
    bool flag2 = false;  // 遍历到一个否定联结词
    bool flag3 = false;  // 遍历到一个二元联结词
    for (int i = 0; i < len; i++) {
        string c(1, s[i]);  // char转string
        // 1.括号成对出现
        if (c == "(") {
            st.push("(");
        }
        else if (c == ")") {
            if (st.top() != "(") {
                return false;
            }
            st.pop();
        }
        // 2.至少有一个命题变元（大写字母）
        else if ("A" <= c && c <= "Z") {
            if (i != len-1) {  // 3.命题变元（大写字母）后一个字符不能为“（”
                if (s[i+1] == '(') {
                    return false;
                }
            }
            if (i != 0) {
                if (s[i-1] == ')') {
                    return false;
                }
            }
            // 如果两个命题变元之间没有二元联结词，返回false
            if (flag1 && !flag3) {
                return false;
            }
            flag1 = true;
            flag2 = false;  // 否定联结词连接到了一个命题
            flag3 = false;  // 二元联结词连接到了两个命题
        }
        // 
        else while (1) {
            if (i == len-1) {  // 到达字符串结尾，不合法
                return false;
            }
            // 4.否定联结词（¬）后至少有一个命题变元（大写字母）
            if (c == NOT) {
                flag2 = true;
                break;
            }
            // 5.二元联结词前后分别至少至少有一个命题变元（大写字母）
            else if (is_binary_connective(c)) {
                if (!flag1) {
                    return false;
                }
                flag3 = true;
                break;
            }
            // 因为联结词符号是多字节字符，需要拼接字符串才能得到
            // 拼接字符串，直到得到一个联结词，或者到达字符串结尾（说明含有其他字符，不合法）
            else {
                string t(1, s[++i]);
                c += t;
            }
        }
    }
    // 括号不成对 or 不含命题变元 or 否定联结词后无命题变元 or 二元联结词后无命题变元
    if (st.top() != "#" || !flag1 || flag2 || flag3) {
        return false;
    }
    return true;
}

int main() {
    // 真值为 1
    cout << is_truth_value_function("¬P∧Q") << ' ';
    cout << is_truth_value_function("P∧Q") << ' ';
    cout << is_truth_value_function("¬P∧¬Q") << ' ';
    cout << is_truth_value_function("¬¬(P∧Q)") << ' ';
    cout << is_truth_value_function("(¬P∧(Q))") << ' ';
    cout << is_truth_value_function("(¬P∧(Q))∨(S↔T)") << ' ';
    cout << is_truth_value_function("P") << ' ';
    cout << is_truth_value_function("P∧Q∨¬R") << ' ';
    cout << is_truth_value_function("(P→(Q∧R))∨(S↔T)") << ' ';
    cout << is_truth_value_function("¬¬((P))") << ' ';
    cout << is_truth_value_function("P→Q→R") << ' ';
    cout << is_truth_value_function("(¬P∨Q)∧(R∨S)") << ' ';

    cout << "\n-----------------------\n";

    // 真值为 0
    cout << is_truth_value_function("(¬P∧(Q)") << ' ';
    cout << is_truth_value_function("()P→Q") << ' ';
    cout << is_truth_value_function("R∨S,") << ' ';
    cout << is_truth_value_function("¬¬R¬") << ' ';
    cout << is_truth_value_function("P→(Q∧R))∨(S↔T))") << ' ';
    cout << is_truth_value_function("(¬P∨Q)∧(R∨S)T") << ' ';
    cout << is_truth_value_function("(¬P") << ' ';
    cout << is_truth_value_function("(())") << ' ';
    cout << is_truth_value_function("(¬P(Q))") << ' ';
    cout << is_truth_value_function("P(→R)") << ' ';
    cout << is_truth_value_function("PQ→R") << ' ';
    cout << is_truth_value_function("∧Q∨¬R") << endl;
    return 0;
}