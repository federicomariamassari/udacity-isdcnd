#include <iostream>
#include <vector>
#include <numeric>
#include <exception>

typedef std::vector< std::vector<float> > t_grid;
t_grid zeros(int n_rows, int n_cols);
t_grid identity(int n);

class Matrix
{
    private:
        t_grid grid;
        std::vector<float>::size_type rows;
        std::vector<float>::size_type cols;

        float dot_product(std::vector<float> p, std::vector<float> q);
        bool is_square();
        float get_minor(t_grid G);
        t_grid get_submatrix(int col);

    public:
        Matrix(t_grid G);

        void set_grid(t_grid G);
        t_grid get_grid();
        std::vector<float>::size_type get_rows();
        std::vector<float>::size_type get_cols();

        float trace();
        float determinant();
        Matrix matrix_inverse();
        Matrix matrix_transpose();
        Matrix matrix_addition(Matrix other);
        Matrix matrix_subtraction(Matrix other);
        Matrix matrix_negation();
        Matrix matrix_multiplication(Matrix other);
        Matrix matrix_right_multiplication(float scalar);

        void matrix_print();
        bool is_identical(Matrix other);

};