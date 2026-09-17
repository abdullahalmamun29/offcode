import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const differentiationModules: Record<string, () => CodeFragment> = {
  'forward_difference': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Forward Difference.
double forwardDiff(const std::vector<double>& x, const std::vector<double>& y, int n, double target_x) {
    for (int i = 0; i < n - 1; i++) {
        if (x[i] == target_x) return (y[i + 1] - y[i]) / (x[i + 1] - x[i]);
    }
    return 0;
}`],
    mainCode: `int n; double target_x;
    std::cout << "Enter n: ";
    std::cin >> n;
    std::vector<double> x(n), y(n);
    for (int i = 0; i < n; i++) std::cin >> x[i] >> y[i];
    std::cout << "Enter target x: ";
    std::cin >> target_x;
    std::cout << "Derivative: " << forwardDiff(x, y, n, target_x) << std::endl;`
  }),
  'backward_difference': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Backward Difference.
double backwardDiff(const std::vector<double>& x, const std::vector<double>& y, int n, double target_x) {
    for (int i = 1; i < n; i++) {
        if (x[i] == target_x) return (y[i] - y[i - 1]) / (x[i] - x[i - 1]);
    }
    return 0;
}`],
    mainCode: `int n; double target_x;
    std::cout << "Enter n: ";
    std::cin >> n;
    std::vector<double> x(n), y(n);
    for (int i = 0; i < n; i++) std::cin >> x[i] >> y[i];
    std::cout << "Enter target x: ";
    std::cin >> target_x;
    std::cout << "Derivative: " << backwardDiff(x, y, n, target_x) << std::endl;`
  }),
  'central_difference': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Central Difference.
double centralDiff(const std::vector<double>& x, const std::vector<double>& y, int n, double target_x) {
    for (int i = 1; i < n - 1; i++) {
        if (x[i] == target_x) return (y[i + 1] - y[i - 1]) / (x[i + 1] - x[i - 1]);
    }
    return 0;
}`],
    mainCode: `int n; double target_x;
    std::cout << "Enter n: ";
    std::cin >> n;
    std::vector<double> x(n), y(n);
    for (int i = 0; i < n; i++) std::cin >> x[i] >> y[i];
    std::cout << "Enter target x: ";
    std::cin >> target_x;
    std::cout << "Derivative: " << centralDiff(x, y, n, target_x) << std::endl;`
  })
};
