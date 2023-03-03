#define NOT "¬"
#define AND "∧"
#define OR "∨"
#define IND "→"
#define EQUAL "↔"
#include <iostream>
#include <string>
using namespace std;

bool P[8] = {0,0,0,0,1,1,1,1};
bool Q[8] = {0,0,1,1,0,0,1,1};
bool R[8] = {0,1,0,1,0,1,0,1};
bool truth_value[8];  


bool Not(bool P) { return !P; }  // Negation

bool And(bool P, bool Q) { return P && Q; }  // Conjunction

bool Or(bool P, bool Q) { return P || Q; }  // Disjunction

bool Ind(bool P, bool Q) {  // Implication
   if (P && !Q) return false;
   return true; 
}

bool Equal(bool P, bool Q) { return (P == Q); }  // Equivalence

void solve() {  // P→((¬P↔Q)∧R)∨Q
    for (int i = 0; i < 8; i++) {
        truth_value[i] = Or(Ind(P[i], And(Equal(Not(P[i]), Q[i]), R[i])), Q[i]);
    }
}



int main() {
    string s = "P→((¬P↔Q)∧R)∨Q";
    solve();
    cout << "P Q R   " << s << endl;
    for (int i = 0; i < 8; i++) {
        cout << P[i] << ' ' << Q[i] << ' ' << R[i]
             << "         " << truth_value[i] << endl;
    }
    return 0;
}