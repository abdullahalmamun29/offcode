import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const interpolation: Record<string, () => CodeFragment> = {
  'lagrange': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Lagrange Interpolation.
double lagrange(const std::vector<double>& x, const std::vector<double>& y, int n, double point) {
    double result = 0;
    for (int i = 0; i < n; i++) {
        double term = y[i];
        for (int j = 0; j < n; j++) {
            if (j != i) term = term * (point - x[j]) / (x[i] - x[j]);
        }
        result += term;
    }
    return result;
}`],
    mainCode: `int n; double point;
    std::cout << "Enter number of data points (n): ";
    if (!(std::cin >> n) || n <= 0) return 0;
    std::vector<double> x(n), y(n);
    std::cout << "\\nEnter data points (x and y pairs):\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Point " << (i + 1) << " (x y): ";
        std::cin >> x[i] >> y[i];
    }
    std::cout << "\\nEnter value of x to interpolate: ";
    std::cin >> point;
    std::cout << "\\nInterpolated value at x = " << point << " is: " << lagrange(x, y, n, point) << std::endl;`
  }),
  'newton_forward': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Newton Forward Interpolation.
double newtonForward(std::vector<double>& x, std::vector<double>& y, int n, double point) {
    std::vector<std::vector<double>> diff(n, std::vector<double>(n));
    for (int i = 0; i < n; i++) diff[i][0] = y[i];
    for (int j = 1; j < n; j++) {
        for (int i = 0; i < n - j; i++) {
            diff[i][j] = diff[i + 1][j - 1] - diff[i][j - 1];
        }
    }
    double sum = diff[0][0];
    double u = (point - x[0]) / (x[1] - x[0]);
    double u_term = 1;
    double fact = 1;
    for (int j = 1; j < n; j++) {
        u_term = u_term * (u - (j - 1));
        fact = fact * j;
        sum += (u_term * diff[0][j]) / fact;
    }
    return sum;
}`],
    mainCode: `int n; double point;
    std::cout << "Enter number of data points (n): ";
    if (!(std::cin >> n) || n <= 0) return 0;
    std::vector<double> x(n), y(n);
    std::cout << "\\nEnter data points (x and y pairs):\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Point " << (i + 1) << " (x y): ";
        std::cin >> x[i] >> y[i];
    }
    std::cout << "\\nEnter value of x to interpolate: ";
    std::cin >> point;
    std::cout << "\\nInterpolated value at x = " << point << " is: " << newtonForward(x, y, n, point) << std::endl;`
  }),
  'newton_backward': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Newton Backward Interpolation.
double newtonBackward(std::vector<double>& x, std::vector<double>& y, int n, double point) {
    std::vector<std::vector<double>> diff(n, std::vector<double>(n));
    for (int i = 0; i < n; i++) diff[i][0] = y[i];
    for (int j = 1; j < n; j++) {
        for (int i = n - 1; i >= j; i--) {
            diff[i][j] = diff[i][j - 1] - diff[i - 1][j - 1];
        }
    }
    double sum = diff[n - 1][0];
    double u = (point - x[n - 1]) / (x[1] - x[0]);
    double u_term = 1;
    double fact = 1;
    for (int j = 1; j < n; j++) {
        u_term = u_term * (u + (j - 1));
        fact = fact * j;
        sum += (u_term * diff[n - 1][j]) / fact;
    }
    return sum;
}`],
    mainCode: `int n; double point;
    std::cout << "Enter number of data points (n): ";
    if (!(std::cin >> n) || n <= 0) return 0;
    std::vector<double> x(n), y(n);
    std::cout << "\\nEnter data points (x and y pairs):\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Point " << (i + 1) << " (x y): ";
        std::cin >> x[i] >> y[i];
    }
    std::cout << "\\nEnter value of x to interpolate: ";
    std::cin >> point;
    std::cout << "\\nInterpolated value at x = " << point << " is: " << newtonBackward(x, y, n, point) << std::endl;`
  }),
  'divided_difference': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Newton Divided Difference Interpolation.
double dividedDifference(std::vector<double>& x, std::vector<double>& y, int n, double point) {
    std::vector<std::vector<double>> diff(n, std::vector<double>(n));
    for (int i = 0; i < n; i++) diff[i][0] = y[i];
    for (int j = 1; j < n; j++) {
        for (int i = 0; i < n - j; i++) {
            diff[i][j] = (diff[i + 1][j - 1] - diff[i][j - 1]) / (x[i + j] - x[i]);
        }
    }
    double sum = diff[0][0];
    double term = 1;
    for (int j = 1; j < n; j++) {
        term = term * (point - x[j - 1]);
        sum += term * diff[0][j];
    }
    return sum;
}`],
    mainCode: `int n; double point;
    std::cout << "Enter number of data points (n): ";
    if (!(std::cin >> n) || n <= 0) return 0;
    std::vector<double> x(n), y(n);
    std::cout << "\\nEnter data points (x and y pairs):\\n";
    for (int i = 0; i < n; i++) {
        std::cout << "Point " << (i + 1) << " (x y): ";
        std::cin >> x[i] >> y[i];
    }
    std::cout << "\\nEnter value of x to interpolate: ";
    std::cin >> point;
    std::cout << "\\nInterpolated value at x = " << point << " is: " << dividedDifference(x, y, n, point) << std::endl;`
  })
};
