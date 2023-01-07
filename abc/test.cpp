#include  <iostream>
#include <string>
using namespace std;

class A {
    public: string name = "viet";
    explicit A(){

    } 
};

int main() {
    cout << A().name << endl;
    A viet = A();
    cout << (viet.name) << endl;
}