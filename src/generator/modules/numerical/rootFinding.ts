import { CodeFragment } from '../../codeComposer';

const POLY_EVAL = `// Evaluates polynomial with given coefficients at x.
double evaluate(const vector<double>& coeff, int degree, double x) {
    double result = 0;
    for (int i = 0; i <= degree; ++i)
        result = result * x + coeff[i];
    return result;
}`;

const POLY_DERIV = `// Evaluates the derivative of the polynomial at x.
double evaluateDerivative(const vector<double>& coeff, int degree, double x) {
    double result = 0;
    for (int i = 0; i < degree; ++i)
        result = result * x + coeff[i] * (degree - i);
    return result;
}`;

const READ_POLY = `int degree;
    cout << "Enter degree of polynomial: ";
    cin >> degree;
    vector<double> coeff(degree + 1);
    cout << "Enter coefficients (highest power first): ";
    for (int i = 0; i <= degree; ++i)
        cin >> coeff[i];`;

export const rootFinding: Record<string, () => CodeFragment> = {
  'bisection': () => ({
    includes: ['iostream', 'vector', 'cmath', 'iomanip'],
    functions: [POLY_EVAL],
    mainCode: `${READ_POLY}

    double a, b, tol;
    int maxIter;
    cout << "Enter lower bound (a): "; cin >> a;
    cout << "Enter upper bound (b): "; cin >> b;
    cout << "Enter tolerance: "; cin >> tol;
    cout << "Enter max iterations: "; cin >> maxIter;

    double fa = evaluate(coeff, degree, a);
    double fb = evaluate(coeff, degree, b);

    if (fa * fb > 0) {
        cout << "f(a) and f(b) must have opposite signs." << endl;
        return 1;
    }

    cout << fixed << setprecision(6);
    cout << "Iter\\ta\\t\\tb\\t\\tc\\t\\tf(c)" << endl;

    for (int i = 1; i <= maxIter; ++i) {
        double c = (a + b) / 2.0;
        double fc = evaluate(coeff, degree, c);

        cout << i << "\\t" << a << "\\t" << b << "\\t" << c << "\\t" << fc << endl;

        if (abs(fc) < tol || (b - a) / 2.0 < tol) {
            cout << "Root: " << c << endl;
            return 0;
        }

        if (fa * fc < 0) { b = c; fb = fc; }
        else { a = c; fa = fc; }
    }

    cout << "Root (after max iterations): " << (a + b) / 2.0 << endl;`
  }),

  'false_position': () => ({
    includes: ['iostream', 'vector', 'cmath', 'iomanip'],
    functions: [POLY_EVAL],
    mainCode: `${READ_POLY}

    double a, b, tol;
    int maxIter;
    cout << "Enter lower bound (a): "; cin >> a;
    cout << "Enter upper bound (b): "; cin >> b;
    cout << "Enter tolerance: "; cin >> tol;
    cout << "Enter max iterations: "; cin >> maxIter;

    double fa = evaluate(coeff, degree, a);
    double fb = evaluate(coeff, degree, b);

    if (fa * fb > 0) {
        cout << "f(a) and f(b) must have opposite signs." << endl;
        return 1;
    }

    cout << fixed << setprecision(6);
    cout << "Iter\\ta\\t\\tb\\t\\tc\\t\\tf(c)" << endl;

    for (int i = 1; i <= maxIter; ++i) {
        double c = (a * fb - b * fa) / (fb - fa);
        double fc = evaluate(coeff, degree, c);

        cout << i << "\\t" << a << "\\t" << b << "\\t" << c << "\\t" << fc << endl;

        if (abs(fc) < tol) {
            cout << "Root: " << c << endl;
            return 0;
        }

        if (fa * fc < 0) { b = c; fb = fc; }
        else { a = c; fa = fc; }
    }

    double c = (a * fb - b * fa) / (fb - fa);
    cout << "Root (after max iterations): " << c << endl;`
  }),

  'newton_raphson': () => ({
    includes: ['iostream', 'vector', 'cmath', 'iomanip'],
    functions: [POLY_EVAL, POLY_DERIV],
    mainCode: `${READ_POLY}

    double x0, tol;
    int maxIter;
    cout << "Enter initial guess: "; cin >> x0;
    cout << "Enter tolerance: "; cin >> tol;
    cout << "Enter max iterations: "; cin >> maxIter;

    cout << fixed << setprecision(6);
    cout << "Iter\\tx\\t\\tf(x)\\t\\tf'(x)" << endl;

    double x = x0;
    for (int i = 1; i <= maxIter; ++i) {
        double fx = evaluate(coeff, degree, x);
        double fpx = evaluateDerivative(coeff, degree, x);

        cout << i << "\\t" << x << "\\t" << fx << "\\t" << fpx << endl;

        if (abs(fpx) < 1e-12) {
            cout << "Derivative too small. Method fails." << endl;
            return 1;
        }

        double x1 = x - fx / fpx;
        if (abs(x1 - x) < tol) {
            cout << "Root: " << x1 << endl;
            return 0;
        }
        x = x1;
    }

    cout << "Root (after max iterations): " << x << endl;`
  }),

  'secant': () => ({
    includes: ['iostream', 'vector', 'cmath', 'iomanip'],
    functions: [POLY_EVAL],
    mainCode: `${READ_POLY}

    double x0, x1, tol;
    int maxIter;
    cout << "Enter x0: "; cin >> x0;
    cout << "Enter x1: "; cin >> x1;
    cout << "Enter tolerance: "; cin >> tol;
    cout << "Enter max iterations: "; cin >> maxIter;

    cout << fixed << setprecision(6);
    cout << "Iter\\tx0\\t\\tx1\\t\\tf(x1)" << endl;

    for (int i = 1; i <= maxIter; ++i) {
        double f0 = evaluate(coeff, degree, x0);
        double f1 = evaluate(coeff, degree, x1);

        if (abs(f1 - f0) < 1e-12) {
            cout << "Division by near-zero. Method fails." << endl;
            return 1;
        }

        double x2 = x1 - f1 * (x1 - x0) / (f1 - f0);
        cout << i << "\\t" << x0 << "\\t" << x1 << "\\t" << f1 << endl;

        if (abs(x2 - x1) < tol) {
            cout << "Root: " << x2 << endl;
            return 0;
        }

        x0 = x1;
        x1 = x2;
    }

    cout << "Root (after max iterations): " << x1 << endl;`
  }),

  'fixed_point_iteration': () => ({
    includes: ['iostream', 'vector', 'cmath', 'iomanip'],
    functions: [POLY_EVAL, POLY_DERIV],
    mainCode: `${READ_POLY}

    double x0, tol;
    int maxIter;
    cout << "Enter initial guess (x0): "; cin >> x0;
    cout << "Enter tolerance: "; cin >> tol;
    cout << "Enter max iterations: "; cin >> maxIter;

    cout << fixed << setprecision(6);
    cout << "Iter\\tx\\t\\tf(x)" << endl;

    double x = x0;
    for (int i = 1; i <= maxIter; ++i) {
        double fx = evaluate(coeff, degree, x);
        cout << i << "\\t" << x << "\\t" << fx << endl;

        if (abs(fx) < tol) {
            cout << "Root: " << x << endl;
            return 0;
        }

        double fpx = evaluateDerivative(coeff, degree, x);
        if (abs(fpx) < 1e-12) fpx = 1.0;
        double x_next = x - fx / fpx;

        if (abs(x_next - x) < tol) {
            cout << "Root: " << x_next << endl;
            return 0;
        }
        x = x_next;
    }

    cout << "Root (after max iterations): " << x << endl;`
  }),
};
