import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const integrationModules: Record<string, () => CodeFragment> = {
  'trapezoidal': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Evaluates polynomial.
double evalPoly(const std::vector<double>& coeffs, double x) {
    double res = 0;
    for (size_t i = 0; i < coeffs.size(); ++i) {
        res += coeffs[i] * std::pow(x, i);
    }
    return res;
}
// Trapezoidal rule.
double trapezoidal(const std::vector<double>& coeffs, double a, double b, int n) {
    double h = (b - a) / n;
    double sum = evalPoly(coeffs, a) + evalPoly(coeffs, b);
    for (int i = 1; i < n; i++) sum += 2 * evalPoly(coeffs, a + i * h);
    return sum * h / 2.0;
}`],
    mainCode: `int degree, n; double a, b;
    std::cin >> degree;
    std::vector<double> coeffs(degree + 1);
    for (int i = 0; i <= degree; ++i) std::cin >> coeffs[i];
    std::cin >> a >> b >> n;
    std::cout << "Integral: " << trapezoidal(coeffs, a, b, n) << std::endl;`
  }),
  'simpson_1_3': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Evaluates polynomial.
double evalPoly(const std::vector<double>& coeffs, double x) {
    double res = 0;
    for (size_t i = 0; i < coeffs.size(); ++i) res += coeffs[i] * std::pow(x, i);
    return res;
}
// Simpson's 1/3 rule.
double simpson13(const std::vector<double>& coeffs, double a, double b, int n) {
    double h = (b - a) / n;
    double sum = evalPoly(coeffs, a) + evalPoly(coeffs, b);
    for (int i = 1; i < n; i++) {
        if (i % 2 == 0) sum += 2 * evalPoly(coeffs, a + i * h);
        else sum += 4 * evalPoly(coeffs, a + i * h);
    }
    return sum * h / 3.0;
}`],
    mainCode: `int degree, n; double a, b;
    std::cin >> degree;
    std::vector<double> coeffs(degree + 1);
    for (int i = 0; i <= degree; ++i) std::cin >> coeffs[i];
    std::cin >> a >> b >> n;
    std::cout << "Integral: " << simpson13(coeffs, a, b, n) << std::endl;`
  }),
  'simpson_3_8': () => ({
    includes: ['iostream', 'vector', 'cmath'],
    structs: [STRUCT],
    functions: [
`// Evaluates polynomial.
double evalPoly(const std::vector<double>& coeffs, double x) {
    double res = 0;
    for (size_t i = 0; i < coeffs.size(); ++i) res += coeffs[i] * std::pow(x, i);
    return res;
}
// Simpson's 3/8 rule.
double simpson38(const std::vector<double>& coeffs, double a, double b, int n) {
    double h = (b - a) / n;
    double sum = evalPoly(coeffs, a) + evalPoly(coeffs, b);
    for (int i = 1; i < n; i++) {
        if (i % 3 == 0) sum += 2 * evalPoly(coeffs, a + i * h);
        else sum += 3 * evalPoly(coeffs, a + i * h);
    }
    return sum * 3.0 * h / 8.0;
}`],
    mainCode: `int degree, n; double a, b;
    std::cin >> degree;
    std::vector<double> coeffs(degree + 1);
    for (int i = 0; i <= degree; ++i) std::cin >> coeffs[i];
    std::cin >> a >> b >> n;
    std::cout << "Integral: " << simpson38(coeffs, a, b, n) << std::endl;`
  })
};
