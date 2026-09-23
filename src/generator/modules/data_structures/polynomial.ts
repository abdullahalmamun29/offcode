import { CodeFragment } from '../../codeComposer';

const POLY_STRUCT = `struct Term {
    int coeff;
    int exp;
    Term* next;
    Term(int c, int e) : coeff(c), exp(e), next(nullptr) {}
};`;

const INSERT_TERM_FN = `// Inserts a term into the polynomial keeping terms in descending order of exponent.
// Combines terms with duplicate powers.
void insertTerm(Term*& poly, int coeff, int exp) {
    if (coeff == 0) return;
    Term* newNode = new Term(coeff, exp);
    if (!poly || exp > poly->exp) {
        newNode->next = poly;
        poly = newNode;
        return;
    }
    Term* curr = poly;
    Term* prev = nullptr;
    while (curr && curr->exp > exp) {
        prev = curr;
        curr = curr->next;
    }
    if (curr && curr->exp == exp) {
        curr->coeff += coeff;
        delete newNode;
        return;
    }
    newNode->next = curr;
    if (prev) {
        prev->next = newNode;
    } else {
        poly = newNode;
    }
}`;

const DISPLAY_POLY_FN = `// Displays the polynomial in standard algebraic notation.
void displayPolynomial(Term* poly) {
    if (!poly) {
        cout << "0" << endl;
        return;
    }
    Term* curr = poly;
    bool first = true;
    while (curr) {
        if (curr->coeff != 0) {
            if (!first && curr->coeff > 0) cout << " + ";
            else if (!first && curr->coeff < 0) cout << " - ";
            else if (first && curr->coeff < 0) cout << "-";

            int absCoeff = abs(curr->coeff);
            if (curr->exp == 0) {
                cout << absCoeff;
            } else if (curr->exp == 1) {
                if (absCoeff != 1) cout << absCoeff;
                cout << "x";
            } else {
                if (absCoeff != 1) cout << absCoeff;
                cout << "x^" << curr->exp;
            }
            first = false;
        }
        curr = curr->next;
    }
    if (first) cout << "0";
    cout << endl;
}`;

const ADD_POLY_FN = `// Adds two polynomials represented as linked lists.
Term* addPolynomials(Term* p1, Term* p2) {
    Term* result = nullptr;
    Term* t1 = p1;
    Term* t2 = p2;
    while (t1 && t2) {
        if (t1->exp > t2->exp) {
            insertTerm(result, t1->coeff, t1->exp);
            t1 = t1->next;
        } else if (t1->exp < t2->exp) {
            insertTerm(result, t2->coeff, t2->exp);
            t2 = t2->next;
        } else {
            insertTerm(result, t1->coeff + t2->coeff, t1->exp);
            t1 = t1->next;
            t2 = t2->next;
        }
    }
    while (t1) {
        insertTerm(result, t1->coeff, t1->exp);
        t1 = t1->next;
    }
    while (t2) {
        insertTerm(result, t2->coeff, t2->exp);
        t2 = t2->next;
    }
    return result;
}`;

const FREE_POLY_FN = `// Frees all nodes in the polynomial linked list.
void freePolynomial(Term*& poly) {
    while (poly) {
        Term* next = poly->next;
        delete poly;
        poly = next;
    }
}`;

const MULTIPLY_POLY_FN = `// Multiplies two polynomials using linked list.
Term* multiplyPolynomials(Term* p1, Term* p2) {
    Term* result = nullptr;
    for (Term* t1 = p1; t1 != nullptr; t1 = t1->next) {
        for (Term* t2 = p2; t2 != nullptr; t2 = t2->next) {
            insertTerm(result, t1->coeff * t2->coeff, t1->exp + t2->exp);
        }
    }
    return result;
}`;

export const polynomial: Record<string, () => CodeFragment> = {
  'multiply': () => ({
    includes: ['iostream', 'cmath'],
    structs: [POLY_STRUCT],
    functions: [INSERT_TERM_FN, DISPLAY_POLY_FN, MULTIPLY_POLY_FN, FREE_POLY_FN],
    mainCode: `Term* poly1 = nullptr;
    Term* poly2 = nullptr;

    int n1, n2;
    cout << "Enter number of terms for first polynomial: ";
    if (!(cin >> n1) || n1 < 0) {
        cout << "Invalid number of terms." << endl;
        return 1;
    }
    for (int i = 0; i < n1; ++i) {
        int c, e;
        cout << "Enter coefficient and exponent for term " << (i + 1) << ": ";
        cin >> c >> e;
        insertTerm(poly1, c, e);
    }

    cout << "Enter number of terms for second polynomial: ";
    if (!(cin >> n2) || n2 < 0) {
        cout << "Invalid number of terms." << endl;
        freePolynomial(poly1);
        return 1;
    }
    for (int i = 0; i < n2; ++i) {
        int c, e;
        cout << "Enter coefficient and exponent for term " << (i + 1) << ": ";
        cin >> c >> e;
        insertTerm(poly2, c, e);
    }

    cout << "\\nPolynomial 1: ";
    displayPolynomial(poly1);
    cout << "Polynomial 2: ";
    displayPolynomial(poly2);

    Term* prod = multiplyPolynomials(poly1, poly2);
    cout << "Product: ";
    displayPolynomial(prod);

    freePolynomial(poly1);
    freePolynomial(poly2);
    freePolynomial(prod);`
  }),
  'add': () => ({
    includes: ['iostream', 'cmath'],
    structs: [POLY_STRUCT],
    functions: [INSERT_TERM_FN, DISPLAY_POLY_FN, ADD_POLY_FN, FREE_POLY_FN],
    mainCode: `Term* poly1 = nullptr;
    Term* poly2 = nullptr;

    int n1, n2;
    cout << "Enter number of terms for first polynomial: ";
    if (!(cin >> n1) || n1 < 0) {
        cout << "Invalid number of terms." << endl;
        return 1;
    }
    for (int i = 0; i < n1; ++i) {
        int c, e;
        cout << "Enter coefficient and exponent for term " << (i + 1) << ": ";
        cin >> c >> e;
        insertTerm(poly1, c, e);
    }

    cout << "Enter number of terms for second polynomial: ";
    if (!(cin >> n2) || n2 < 0) {
        cout << "Invalid number of terms." << endl;
        freePolynomial(poly1);
        return 1;
    }
    for (int i = 0; i < n2; ++i) {
        int c, e;
        cout << "Enter coefficient and exponent for term " << (i + 1) << ": ";
        cin >> c >> e;
        insertTerm(poly2, c, e);
    }

    cout << "\\nPolynomial 1: ";
    displayPolynomial(poly1);
    cout << "Polynomial 2: ";
    displayPolynomial(poly2);

    Term* sum = addPolynomials(poly1, poly2);
    cout << "Sum: ";
    displayPolynomial(sum);

    freePolynomial(poly1);
    freePolynomial(poly2);
    freePolynomial(sum);`
  }),

  'create': () => ({
    includes: ['iostream', 'cmath'],
    structs: [POLY_STRUCT],
    functions: [INSERT_TERM_FN, DISPLAY_POLY_FN, FREE_POLY_FN],
    mainCode: `Term* poly = nullptr;
    int n;
    cout << "Enter number of terms for polynomial: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        int c, e;
        cout << "Enter coefficient and exponent for term " << (i + 1) << ": ";
        cin >> c >> e;
        insertTerm(poly, c, e);
    }
    cout << "Polynomial: ";
    displayPolynomial(poly);
    freePolynomial(poly);`
  }),

  'display': () => ({
    includes: ['iostream', 'cmath'],
    structs: [POLY_STRUCT],
    functions: [INSERT_TERM_FN, DISPLAY_POLY_FN, FREE_POLY_FN],
    mainCode: `Term* poly = nullptr;
    int n;
    cout << "Enter number of terms for polynomial: ";
    cin >> n;
    for (int i = 0; i < n; ++i) {
        int c, e;
        cout << "Enter coefficient and exponent for term " << (i + 1) << ": ";
        cin >> c >> e;
        insertTerm(poly, c, e);
    }
    cout << "Polynomial: ";
    displayPolynomial(poly);
    freePolynomial(poly);`
  })
};
