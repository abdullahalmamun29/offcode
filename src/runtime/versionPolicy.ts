/**
 * Centralized Python Version Policy for CHUP.
 *
 * Grounded in repository AST inspection and verified compatibility:
 * Requires Python >= 3.8, Major Version 3.
 */

export const SUPPORTED_PYTHON_MAJOR = 3;
export const SUPPORTED_PYTHON_MIN_MINOR = 8;
export const SUPPORTED_RANGE_DESCRIPTION = "Python >= 3.8 (Major Version 3)";

export interface ParsedPythonVersion {
  major: number;
  minor: number;
  patch: number;
  raw: string;
}

/**
 * Parse a version string such as "3.12.3", "Python 3.10.8", "3.9.1+ ..."
 */
export function parsePythonVersion(rawVersion: string): ParsedPythonVersion | null {
  if (!rawVersion || typeof rawVersion !== "string") {
    return null;
  }

  const match = rawVersion.match(/(\d+)\.(\d+)(?:\.(\d+))?/);
  if (!match) {
    return null;
  }

  const major = parseInt(match[1], 10);
  const minor = parseInt(match[2], 10);
  const patch = match[3] !== undefined ? parseInt(match[3], 10) : 0;

  if (isNaN(major) || isNaN(minor) || isNaN(patch)) {
    return null;
  }

  return {
    major,
    minor,
    patch,
    raw: rawVersion.trim()
  };
}

/**
 * Checks if the given major and minor versions meet CHUP's requirements.
 */
export function isVersionSupported(major: number, minor: number): boolean {
  return major === SUPPORTED_PYTHON_MAJOR && minor >= SUPPORTED_PYTHON_MIN_MINOR;
}

/**
 * Generates an authoritative error diagnostic for unsupported versions.
 */
export function formatVersionRejectionMessage(
  detectedVersion: string,
  executablePath: string
): string {
  return (
    `CHUP Python Runtime Error\n\n` +
    `Detected:\n` +
    `    Python ${detectedVersion}\n` +
    `    ${executablePath}\n\n` +
    `This Python version is outside CHUP's supported range:\n` +
    `    ${SUPPORTED_RANGE_DESCRIPTION}\n\n` +
    `Please configure a supported Python interpreter using the "chup.pythonPath" setting.`
  );
}
