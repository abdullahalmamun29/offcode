import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const linearSystems: Record<string, () => CodeFragment> = {
  'gauss_elimination': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs Gaussian Elimination with partial pivoting to solve Ax = b.
void gaussElimination(std::vector<std::vector<double>>& a, int n) {
    for (int i = 0; i < n; i++) {
        // Partial pivoting
        for (int k = i + 1; k < n; k++) {
            if (std::abs(a[i][i]) < std::abs(a[k][i])) std::swap(a[i], a[k]);
        }
        if (std::abs(a[i][i]) < 1e-12) {
            std::cout << "\\nError: Singular or nearly singular matrix detected." << std::endl;
            return;
        }
        for (int k = i + 1; k < n; k++) {
            double t = a[k][i] / a[i][i];
            for (int j = 0; j <= n; j++) a[k][j] -= t * a[i][j];
        }
    }
    std::vector<double> x(n);
    for (int i = n - 1; i >= 0; i--) {
        x[i] = a[i][n];
        for (int j = i + 1; j < n; j++) {
            x[i] = x[i] - a[i][j] * x[j];
        }
        x[i] = x[i] / a[i][i];
    }
    std::cout << "\\nSolution:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "x" << (i + 1) << " = " << x[i] << std::endl;
    }
}`],
    mainCode: `int n;
    std::cout << "Enter the order of the matrix: ";
    if (!(std::cin >> n) || n <= 0) {
        std::cout << "Invalid matrix order." << std::endl;
        return 0;
    }
    std::vector<std::vector<double>> a(n, std::vector<double>(n + 1));
    std::cout << "Enter the elements of the coefficient matrix:" << std::endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) std::cin >> a[i][j];
    }
    std::cout << "Enter the elements of the constant vector:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cin >> a[i][n];
    }
    gaussElimination(a, n);`
  }),
  'gauss_jordan': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs Gauss-Jordan Elimination to solve Ax = b.
void gaussJordan(std::vector<std::vector<double>>& a, int n) {
    for (int i = 0; i < n; i++) {
        // Partial pivoting
        for (int k = i + 1; k < n; k++) {
            if (std::abs(a[i][i]) < std::abs(a[k][i])) std::swap(a[i], a[k]);
        }
        if (std::abs(a[i][i]) < 1e-12) {
            std::cout << "\\nError: Singular or nearly singular matrix detected." << std::endl;
            return;
        }
        for (int k = 0; k < n; k++) {
            if (k != i) {
                double t = a[k][i] / a[i][i];
                for (int j = 0; j <= n; j++) a[k][j] -= t * a[i][j];
            }
        }
    }
    std::cout << "\\nSolution:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "x" << (i + 1) << " = " << (a[i][n] / a[i][i]) << std::endl;
    }
}`],
    mainCode: `int n;
    std::cout << "Enter the order of the matrix: ";
    if (!(std::cin >> n) || n <= 0) {
        std::cout << "Invalid matrix order." << std::endl;
        return 0;
    }
    std::vector<std::vector<double>> a(n, std::vector<double>(n + 1));
    std::cout << "Enter the elements of the coefficient matrix:" << std::endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) std::cin >> a[i][j];
    }
    std::cout << "Enter the elements of the constant vector:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cin >> a[i][n];
    }
    gaussJordan(a, n);`
  }),
  'lu_decomposition': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs Doolittle LU Decomposition and solves the system Ax = b.
void luDecomposition(const std::vector<std::vector<double>>& A, const std::vector<double>& b, int n) {
    std::vector<std::vector<double>> L(n, std::vector<double>(n, 0.0));
    std::vector<std::vector<double>> U(n, std::vector<double>(n, 0.0));

    // Doolittle algorithm: L has 1s on diagonal
    for (int i = 0; i < n; ++i) {
        // Upper Triangular Matrix U
        for (int k = i; k < n; ++k) {
            double sum = 0.0;
            for (int j = 0; j < i; ++j) sum += (L[i][j] * U[j][k]);
            U[i][k] = A[i][k] - sum;
        }

        // Lower Triangular Matrix L
        for (int k = i; k < n; ++k) {
            if (i == k) {
                L[i][i] = 1.0;
            } else {
                if (std::abs(U[i][i]) < 1e-12) {
                    std::cout << "\\nError: Zero pivot encountered at U[" << (i + 1) << "][" << (i + 1) << "]. LU decomposition without pivoting fails." << std::endl;
                    return;
                }
                double sum = 0.0;
                for (int j = 0; j < i; ++j) sum += (L[k][j] * U[j][i]);
                L[k][i] = (A[k][i] - sum) / U[i][i];
            }
        }
    }

    std::cout << "\\nMatrix L:" << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) std::cout << L[i][j] << " ";
        std::cout << std::endl;
    }

    std::cout << "\\nMatrix U:" << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) std::cout << U[i][j] << " ";
        std::cout << std::endl;
    }

    // Forward Substitution: Ly = b
    std::vector<double> y(n, 0.0);
    for (int i = 0; i < n; ++i) {
        double sum = 0.0;
        for (int j = 0; j < i; ++j) sum += L[i][j] * y[j];
        y[i] = b[i] - sum;
    }

    // Back Substitution: Ux = y
    std::vector<double> x(n, 0.0);
    for (int i = n - 1; i >= 0; --i) {
        double sum = 0.0;
        for (int j = i + 1; j < n; ++j) sum += U[i][j] * x[j];
        if (std::abs(U[i][i]) < 1e-12) {
            std::cout << "\\nError: Singular matrix detected during back substitution." << std::endl;
            return;
        }
        x[i] = (y[i] - sum) / U[i][i];
    }

    std::cout << "\\nSolution:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "x" << (i + 1) << " = " << x[i] << std::endl;
    }
}`],
    mainCode: `int n;
    std::cout << "Enter the order of the matrix: ";
    if (!(std::cin >> n) || n <= 0) {
        std::cout << "Invalid matrix order." << std::endl;
        return 0;
    }
    std::vector<std::vector<double>> A(n, std::vector<double>(n));
    std::vector<double> B(n);

    std::cout << "Enter the elements of the coefficient matrix:" << std::endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) std::cin >> A[i][j];
    }

    std::cout << "Enter the elements of the constant vector:" << std::endl;
    for (int i = 0; i < n; ++i) {
        std::cin >> B[i];
    }

    luDecomposition(A, B, n);`
  }),
  'jacobi': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs Jacobi Iteration to solve Ax = b.
void jacobi(const std::vector<std::vector<double>>& a, const std::vector<double>& b, std::vector<double>& x, int n, double tol, int max_iter) {
    std::vector<double> x_new(n);
    int iter = 0;
    for (; iter < max_iter; iter++) {
        double error = 0.0;
        for (int i = 0; i < n; i++) {
            double sum = b[i];
            for (int j = 0; j < n; j++) {
                if (i != j) sum -= a[i][j] * x[j];
            }
            x_new[i] = sum / a[i][i];
            error = std::max(error, std::abs(x_new[i] - x[i]));
        }
        x = x_new;
        if (error < tol) {
            iter++;
            break;
        }
    }
    std::cout << "\\nConverged in " << iter << " iterations." << std::endl;
    std::cout << "\\nSolution:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "x" << (i + 1) << " = " << x[i] << std::endl;
    }
}`],
    mainCode: `int n;
    std::cout << "Enter the order of the matrix: ";
    if (!(std::cin >> n) || n <= 0) {
        std::cout << "Invalid matrix order." << std::endl;
        return 0;
    }
    std::vector<std::vector<double>> a(n, std::vector<double>(n));
    std::vector<double> b(n), x(n, 0.0);
    std::cout << "Enter the elements of the coefficient matrix:" << std::endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) std::cin >> a[i][j];
    }
    std::cout << "Enter the elements of the constant vector:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cin >> b[i];
    }
    int max_iter;
    double tol;
    std::cout << "Enter maximum iterations: ";
    std::cin >> max_iter;
    std::cout << "Enter tolerance: ";
    std::cin >> tol;
    jacobi(a, b, x, n, tol, max_iter);`
  }),
  'gauss_seidel': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs Gauss-Seidel Iteration to solve Ax = b.
void gaussSeidel(const std::vector<std::vector<double>>& a, const std::vector<double>& b, std::vector<double>& x, int n, double tol, int max_iter) {
    int iter = 0;
    for (; iter < max_iter; iter++) {
        double error = 0.0;
        for (int i = 0; i < n; i++) {
            double sum = b[i];
            for (int j = 0; j < n; j++) {
                if (i != j) sum -= a[i][j] * x[j];
            }
            double old_xi = x[i];
            x[i] = sum / a[i][i];
            error = std::max(error, std::abs(x[i] - old_xi));
        }
        if (error < tol) {
            iter++;
            break;
        }
    }
    std::cout << "\\nConverged in " << iter << " iterations." << std::endl;
    std::cout << "\\nSolution:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "x" << (i + 1) << " = " << x[i] << std::endl;
    }
}`],
    mainCode: `int n;
    std::cout << "Enter the order of the matrix: ";
    if (!(std::cin >> n) || n <= 0) {
        std::cout << "Invalid matrix order." << std::endl;
        return 0;
    }
    std::vector<std::vector<double>> a(n, std::vector<double>(n));
    std::vector<double> b(n), x(n, 0.0);
    std::cout << "Enter the elements of the coefficient matrix:" << std::endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) std::cin >> a[i][j];
    }
    std::cout << "Enter the elements of the constant vector:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cin >> b[i];
    }
    int max_iter;
    double tol;
    std::cout << "Enter maximum iterations: ";
    std::cin >> max_iter;
    std::cout << "Enter tolerance: ";
    std::cin >> tol;
    gaussSeidel(a, b, x, n, tol, max_iter);`
  })
};
