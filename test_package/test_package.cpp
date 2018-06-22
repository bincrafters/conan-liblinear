#include <cstdlib>
#include <iostream>
#include <cassert>

#include <linear.h>

static feature_node x1 [] = {{1, -1}, {2, 1}, {-1, 0}};
static feature_node x2 [] = {{1, 1}, {2, 1}, {-1, 0}};
static feature_node x3 [] = {{1, -1}, {2, -1}, {-1, 0}};
static feature_node x4 [] = {{1, 1}, {2, -1}, {-1, 0}};
        
static feature_node* x[] = {x1, x2, x3, x4};

static double y[] = {0.0, 0.0, 1.0, 1.0};

static feature_node test1[] = {{1, 0}, {2, 1}, {-1, 0}};
static feature_node test2[] = {{1, 0}, {2, -1}, {-1, 0}};

/**
 * In this test case the following model is trained and * and # are predicted:
 *
 *    |
 *  0 # 0
 *  --|--
 *  1 * 1
 *    |
 *
 * We expect the learned boundary to be the X axis, and therefore # to be assigned label 0 and * to be assigned label 1.
 */
int main()
{
    std::cout << "Testing liblinear version " << LIBLINEAR_VERSION << std::endl;

    problem p = {};

    p.l = 4;
    p.n = 2;
    p.bias = 0;
    p.x = x; 
    p.y = y;

    // The solver settings
    parameter param = {};
    param.solver_type = L2R_L2LOSS_SVC_DUAL;
    param.eps = 10e-8;
    param.C = 1;
    param.nr_weight = 0;
    param.weight_label = nullptr;
    param.weight = nullptr;

    const char* error = check_parameter(&p, &param);
    if (error != nullptr) {
        std::cerr << "Error found while checking model parameters" << std::endl;
        return EXIT_FAILURE;
    }

    model* m = train(&p, &param);

    double result1 = predict(m, test1);
    double result2 = predict(m, test2);

    if (result1 != 0 || result2 != 1) {
        std::cerr << "Incorrect predictions made during testing" << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
