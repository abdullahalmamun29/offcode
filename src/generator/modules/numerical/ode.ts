import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const odeModules: Record<string, () => CodeFragment> = {
  'euler': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Returns dy/dx.
double func(int choice, double x, double y) {
    if (choice == 1) return x + y;
    if (choice == 2) return x * y;
    if (choice == 3) return x - y;
    return 0;
}
// Euler's method.
void euler(int choice, double x0, double y0, double x_target, double h) {
    double x = x0, y = y0;
    while (x < x_target) {
        y = y + h * func(choice, x, y);
        x = x + h;
    }
    std::cout << "Result: " << y << std::endl;
}`],
    mainCode: `int choice;
    double x0, y0, x_target, h;
    std::cout << "Select differential equation dy/dx:\\n";
    std::cout << "1. dy/dx = x + y\\n";
    std::cout << "2. dy/dx = x * y\\n";
    std::cout << "3. dy/dx = x - y\\n";
    std::cout << "Enter choice (1-3): ";
    std::cin >> choice;
    std::cout << "Enter initial x (x0): ";
    std::cin >> x0;
    std::cout << "Enter initial y (y0): ";
    std::cin >> y0;
    std::cout << "Enter target x value: ";
    std::cin >> x_target;
    std::cout << "Enter step size (h): ";
    std::cin >> h;
    euler(choice, x0, y0, x_target, h);`
  }),
  'modified_euler': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Returns dy/dx.
double func(int choice, double x, double y) {
    if (choice == 1) return x + y;
    if (choice == 2) return x * y;
    if (choice == 3) return x - y;
    return 0;
}
// Modified Euler's method.
void modifiedEuler(int choice, double x0, double y0, double x_target, double h) {
    double x = x0, y = y0;
    while (x < x_target) {
        double y_pred = y + h * func(choice, x, y);
        y = y + (h / 2.0) * (func(choice, x, y) + func(choice, x + h, y_pred));
        x = x + h;
    }
    std::cout << "\nApproximate y at x = " << x_target << " is: " << y << std::endl;
}`],
    mainCode: `int choice;
    double x0, y0, x_target, h;
    std::cout << "Select differential equation dy/dx:\\n";
    std::cout << "1. dy/dx = x + y\\n";
    std::cout << "2. dy/dx = x * y\\n";
    std::cout << "3. dy/dx = x - y\\n";
    std::cout << "Enter choice (1-3): ";
    std::cin >> choice;
    std::cout << "Enter initial x (x0): ";
    std::cin >> x0;
    std::cout << "Enter initial y (y0): ";
    std::cin >> y0;
    std::cout << "Enter target x value: ";
    std::cin >> x_target;
    std::cout << "Enter step size (h): ";
    std::cin >> h;
    modifiedEuler(choice, x0, y0, x_target, h);`
  }),
  'runge_kutta_4': () => ({
    includes: ['iostream'],
    structs: [STRUCT],
    functions: [
`// Returns dy/dx.
double func(int choice, double x, double y) {
    if (choice == 1) return x + y;
    if (choice == 2) return x * y;
    if (choice == 3) return x - y;
    return 0;
}
// Runge-Kutta 4th order.
void rk4(int choice, double x0, double y0, double x_target, double h) {
    double x = x0, y = y0;
    while (x < x_target) {
        double k1 = h * func(choice, x, y);
        double k2 = h * func(choice, x + h / 2.0, y + k1 / 2.0);
        double k3 = h * func(choice, x + h / 2.0, y + k2 / 2.0);
        double k4 = h * func(choice, x + h, y + k3);
        y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4);
        x = x + h;
    }
    std::cout << "\nApproximate y at x = " << x_target << " is: " << y << std::endl;
}`],
    mainCode: `int choice;
    double x0, y0, x_target, h;
    std::cout << "Select differential equation dy/dx:\\n";
    std::cout << "1. dy/dx = x + y\\n";
    std::cout << "2. dy/dx = x * y\\n";
    std::cout << "3. dy/dx = x - y\\n";
    std::cout << "Enter choice (1-3): ";
    std::cin >> choice;
    std::cout << "Enter initial x (x0): ";
    std::cin >> x0;
    std::cout << "Enter initial y (y0): ";
    std::cin >> y0;
    std::cout << "Enter target x value: ";
    std::cin >> x_target;
    std::cout << "Enter step size (h): ";
    std::cin >> h;
    rk4(choice, x0, y0, x_target, h);`
  })
};
