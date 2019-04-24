/**
 * Implementation of (out of bag) proximity function.
 */

#include <cstdlib>   // size_t
#include <cmath>     // sqrt, pow, abs, acos, cos, sin
#include <limits>    // numeric_limits
#include <vector>    // vector

extern "C" void get_indexes(
    // counts
    int const n_trees,
    int const n_other,
    int const n_treated,

    // leaves for each observation in each tree (2d arrays)
    int const* leaves_other,
    int const* leaves_treated,

    // whether the observation is in each tree (2d arrays)
    bool const* not_in_other,
    bool const* not_in_treated,

    // output matrix (assumed to be zeroed) n_other x n_treated
    double* proximity
) {

#pragma omp parallel
    {
        int
            t, o, l,
            n_common, n_same,
            tio, oio, ti, oi;

#pragma omp for
        for(o=0; o<n_other; ++o) {
            oio = o*n_trees;
            tio = 0;
            for(t=0; t<n_treated; ++t, tio+=n_trees) {
                n_common = n_same = 0;
                ti = tio;
                oi = oio;
                for(l=0; l<n_trees; ++l, ++ti, ++oi) {
                    if(not_in_treated[ti] && not_in_other[oi]) {
                        ++n_common;
                        if(leaves_treated[ti] == leaves_other[oi]) {
                            ++n_same;
                        }
                    }
                }
                proximity[o * n_treated + t] = n_common > 0 ?
                    static_cast<double>(n_same) / static_cast<double>(n_common) :
                    0.;
            }
        }
    }
}
