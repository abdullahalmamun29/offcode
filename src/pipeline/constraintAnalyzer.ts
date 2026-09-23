import {
  ParsedConstraint,
  FeasibilityEstimate,
  ComplexityClass,
  StructuredProblem
} from '../models/problemSpec';

/**
 * Computes the factorial of a number, capped at 20 to avoid large numbers.
 */
function factorial(n: number): number {
  if (n <= 1) return 1;
  let result = 1;
  for (let i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}

/**
 * Formats operation counts into a human-readable string (e.g., "10^8" or "2×10^5").
 */
function formatOps(ops: number): string {
  if (ops < 1000) return ops.toString();
  const exp = Math.floor(Math.log10(ops));
  const coeff = ops / Math.pow(10, exp);
  const coeffRounded = Math.round(coeff * 10) / 10;
  if (coeffRounded === 1) return `10^${exp}`;
  return `${coeffRounded}×10^${exp}`;
}

/**
 * Analyzes the constraints of a problem to estimate the feasibility of different time complexity classes.
 * 
 * @param problem - The structured problem containing constraints, time limits, etc.
 * @returns A FeasibilityEstimate indicating which complexity classes are feasible, marginal, or likely infeasible.
 */
export function analyzeConstraints(problem: StructuredProblem): FeasibilityEstimate {
  let primaryN: number | null = null;
  const constraints = problem.constraints || [];
  
  // 1. Find primary constraint (prefer standard size variables n, m, N, M, V, E, etc.)
  const sizeVars = new Set(['n', 'm', 'v', 'e', 'len', 'size', 'length', 'nodes', 'vertices']);
  const sizeConstraint = constraints.find(c => sizeVars.has(c.variable.toLowerCase()));
  if (sizeConstraint) {
    primaryN = sizeConstraint.upperBound;
  } else {
    for (const c of constraints) {
      if (/^[a-zA-Z]$/.test(c.variable) && !/^[tTqQ]$/.test(c.variable) && c.upperBound <= 1e8) {
        if (primaryN === null || c.upperBound > primaryN) {
          primaryN = c.upperBound;
        }
      }
    }
  }

  // 2. Detect test case count
  let T = 1;
  const tConstraint = constraints.find(c => /^[tT]$/.test(c.variable));
  
  if (tConstraint) {
    T = tConstraint.upperBound;
  } else if (problem.statement) {
    const stmtLower = problem.statement.toLowerCase();
    // Scan problem statement for test case phrases
    if (
      stmtLower.includes('the first line contains t') || 
      stmtLower.includes('number of test cases')
    ) {
      const match = stmtLower.match(/(\d+)\s*test cases/);
      if (match) {
        T = parseInt(match[1], 10);
      }
    }
  }

  const timeLimit = problem.timeLimit ?? 1.0;
  
  // Overflow risk check helper
  const checkOverflowRisk = (): boolean => {
    for (const c of constraints) {
      if (c.upperBound >= 1e9) return true;
    }
    let maxVal = 0;
    for (const c of constraints) {
      if (c.upperBound > maxVal) maxVal = c.upperBound;
    }
    if (primaryN && primaryN * maxVal > 2147483648) return true;

    const textLower = (problem.statement + ' ' + (problem.rawText || '')).toLowerCase();
    if (
      textLower.includes('exceed 32-bit') ||
      textLower.includes('exceed int') ||
      textLower.includes('overflow') ||
      textLower.includes('64-bit') ||
      textLower.includes('long long')
    ) {
      return true;
    }
    return false;
  };

  const overflowRisk = checkOverflowRisk();

  if (primaryN === null) {
    return {
      constraints,
      timeLimit,
      testCases: T,
      memoryLimit: problem.memoryLimit ?? null,
      feasible: [
        'O(1)', 'O(log N)', 'O(N)', 'O(N log N)',
        'O(N sqrt N)', 'O(N²)', 'O(N³)', 'O(2^N)', 'O(N!)'
      ],
      marginal: [],
      likelyInfeasible: [],
      overflowRisk,
      reasoning: 'No constraints detected. Cannot estimate feasibility.'
    };
  }

  // 4. Compute estimated operations per second
  const opsPerSecond = 100_000_000; // 10^8
  
  // 5. For each complexity class, compute estimated ops
  const classes: ComplexityClass[] = [
    'O(1)', 'O(log N)', 'O(N)', 'O(N log N)',
    'O(N sqrt N)', 'O(N²)', 'O(N³)', 'O(2^N)', 'O(N!)'
  ];

  const feasible: ComplexityClass[] = [];
  const marginal: ComplexityClass[] = [];
  const likelyInfeasible: ComplexityClass[] = [];
  
  const getOps = (cClass: ComplexityClass, N: number): number => {
    switch (cClass) {
      case 'O(1)': return 1;
      case 'O(log N)': return Math.ceil(Math.log2(N || 1));
      case 'O(N)': return N;
      case 'O(N log N)': return N * Math.ceil(Math.log2(N || 1));
      case 'O(N sqrt N)': return N * Math.ceil(Math.sqrt(N));
      case 'O(N²)': return N * N;
      case 'O(N³)': return N * N * N;
      case 'O(2^N)': return Math.pow(2, Math.min(N, 30));
      case 'O(N!)': return factorial(Math.min(N, 20));
      default: return N;
    }
  };

  // 7. Classify each
  for (const cClass of classes) {
    const estOps = getOps(cClass, primaryN);
    const totalOps = estOps * T;
    
    if (totalOps <= opsPerSecond * timeLimit * 0.5) {
      feasible.push(cClass);
    } else if (totalOps <= opsPerSecond * timeLimit * 2.0) {
      marginal.push(cClass);
    } else {
      likelyInfeasible.push(cClass);
    }
  }

  // 9. Build reasoning string
  const oN_ops = getOps('O(N)', primaryN) * T;
  const oN2_ops = getOps('O(N²)', primaryN) * T;
  
  const getStatus = (ops: number): string => {
    if (ops <= opsPerSecond * timeLimit * 0.5) return 'feasible';
    if (ops <= opsPerSecond * timeLimit * 2.0) return 'marginal';
    return 'infeasible';
  };

  const opsPerSecFormatted = formatOps(opsPerSecond);
  const reasoning = `N = ${primaryN}, T = ${T}, time limit = ${timeLimit}s. Estimated safe operation count: ${opsPerSecFormatted}. O(N) = ${formatOps(oN_ops)} ops [${getStatus(oN_ops)}]. O(N²) = ${formatOps(oN2_ops)} ops [${getStatus(oN2_ops)}].`;

  return {
    constraints,
    timeLimit,
    testCases: T,
    memoryLimit: problem.memoryLimit ?? null,
    feasible,
    marginal,
    likelyInfeasible,
    overflowRisk,
    reasoning
  };
}
