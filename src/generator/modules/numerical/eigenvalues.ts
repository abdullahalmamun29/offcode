import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const eigenvaluesModules: Record<string, () => CodeFragment> = {
  'power_method': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs Power Method to find dominant eigenvalue and eigenvector.
void powerMethod(const std::vector<std::vector<double>>& a, std::vector<double>& x, int n, double tol, int max_iter) {
    double lambda_old = 0;
    int iter = 0;
    for (; iter < max_iter; iter++) {
        std::vector<double> x_new(n, 0);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                x_new[i] += a[i][j] * x[j];
            }
        }
        double lambda_new = 0;
        for (int i = 0; i < n; i++) {
            if (std::abs(x_new[i]) > std::abs(lambda_new)) {
                lambda_new = x_new[i];
            }
        }
        for (int i = 0; i < n; i++) {
            x[i] = x_new[i] / lambda_new;
        }
        if (std::abs(lambda_new - lambda_old) < tol) {
            lambda_old = lambda_new;
            iter++;
            break;
        }
        lambda_old = lambda_new;
    }
    std::cout << "\\nDominant Eigenvalue: " << lambda_old << std::endl;
    std::cout << "Corresponding Eigenvector:" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "x[" << (i + 1) << "] = " << x[i] << std::endl;
    }
}`],
    mainCode: `int n;
    std::cout << "Enter the order of the square matrix (n): ";
    if (!(std::cin >> n) || n <= 0) return 0;
    std::vector<std::vector<double>> a(n, std::vector<double>(n));
    std::cout << "\\nEnter elements of matrix A (" << n << "x" << n << ") row by row:\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Row " << (i + 1) << ": ";
        for (int j = 0; j < n; j++) std::cin >> a[i][j];
    }
    std::vector<double> x(n, 1.0);
    int max_iter; double tol;
    std::cout << "\\nEnter tolerance (e.g. 0.0001): ";
    std::cin >> tol;
    std::cout << "Enter max iterations: ";
    std::cin >> max_iter;
    powerMethod(a, x, n, tol, max_iter);`
  })
};
