
#include <iostream>
#include <cstdlib>
#include "Graph.h"

using namespace std;

int main(int argc, char *argv[])
{
    cout << "before init!" << endl;

    // char* testpath = "../test/input/g1.in";
    // char* testpath = "../in/square.in";
    // char* testpath = "../in/smolgraph.in";
    // char* testpath = "../in/hexmod.in";
    // char* testpath = "../in/line.in";
    // char* testpath = "../in/3ring.in";
    // char* testpath = "../in/3star.in";
    // char* testpath = "../in/polypbg.in";
    // char* testpath = "../in/polypbgtriangle.in";
    char* testpath = "../in/floatingedge.in";


    BaseGraph* bg = new BaseGraph();

    cout << "loading graph from " << testpath << endl;
    bg->load_txt(testpath);

    cout << "graph size: " << bg->size() << endl;

    cout << "building coloring. k=? " << endl;
    int k;
    cin >> k;

    ColoringGraph* cg = bg->build_coloring_graph(k);

    cout << "coloring graph size: " << cg->size() << endl;

    cout << "reached EOF tester" << endl;

    MetaGraph* mbg = bg->tarjans();

    cout << "metagraph size: " << mbg->size() << endl;

    for (auto& p : mbg->vertices)
    {
        MetaVertex* mv = p.second;
        std::cout << "\nmetavertex " << mv->get_name()
                  << " contents: " << "\t";
        for (long v : mv->vertices)
            std::cout << v << ' ';
    }
    std::cout << "\n";

    return 0;
}
