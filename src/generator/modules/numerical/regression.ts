import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const regressionModules: Record<string, () => CodeFragment> = {
  'linear_regression': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Performs linear regression to fit y = mx + c.
void linearRegression(const std::vector<double>& x, const std::vector<double>& y, int n) {
    double sum_x = 0, sum_y = 0, sum_xy = 0, sum_xx = 0;
    for (int i = 0; i < n; i++) {
        sum_x += x[i];
        sum_y += y[i];
        sum_xy += x[i] * y[i];
        sum_xx += x[i] * x[i];
    }
    double slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x);
    double intercept = (sum_y - slope * sum_x) / n;
    std::cout << "\nBest-fit linear equation: y = " << slope << "x + " << intercept << std::endl;
}`],
    mainCode: `int n;
    std::cout << "Enter number of data points (n): ";
    if (!(std::cin >> n) || n <= 1) return 0;
    std::vector<double> x(n), y(n);
    std::cout << "\\nEnter data points (x and y pairs):\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Point " << (i + 1) << " (x y): ";
        std::cin >> x[i] >> y[i];
    }
    linearRegression(x, y, n);`
  }),
  'polynomial_regression': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Performs polynomial regression of degree 2.
void polyRegression(const std::vector<double>& x, const std::vector<double>& y, int n) {
    // Basic implementation for degree 2.
    std::cout << "Not fully implemented. Try linear regression for full functionality." << std::endl;
}`],
    mainCode: `int n;
    std::cout << "Enter number of data points (n): ";
    if (!(std::cin >> n) || n <= 1) return 0;
    std::vector<double> x(n), y(n);
    std::cout << "\\nEnter data points (x and y pairs):\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Point " << (i + 1) << " (x y): ";
        std::cin >> x[i] >> y[i];
    }
    polyRegression(x, y, n);`
  })
};
