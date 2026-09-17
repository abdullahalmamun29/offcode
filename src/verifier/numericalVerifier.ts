export function verifyNumericalResult(actual: string, expected: number, tolerance: number): boolean {
  const nums = actual.match(/-?\d+(\.\d+)?/g);
  if (!nums) return false;
  
  for (const numStr of nums) {
    const val = parseFloat(numStr);
    if (!isNaN(val)) {
      if (Math.abs(val - expected) <= tolerance) {
        return true;
      }
    }
  }
  
  return false;
}
