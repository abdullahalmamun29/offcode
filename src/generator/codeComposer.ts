export interface CodeFragment {
  includes: string[];
  structs?: string[];
  functions: string[];
  mainCode?: string;
}

export function composeCode(fragments: CodeFragment[]): string {
  const includes = new Set<string>();
  const structs = new Set<string>();
  const functions: string[] = [];
  const mainCodes: string[] = [];

  for (const frag of fragments) {
    frag.includes?.forEach(inc => includes.add(inc));
    frag.structs?.forEach(st => structs.add(st));
    frag.functions?.forEach(fn => functions.push(fn));
    if (frag.mainCode) mainCodes.push(frag.mainCode);
  }

  let code = '';
  for (const inc of includes) {
    if (inc.startsWith('<') || inc.startsWith('"')) {
      code += `#include ${inc}\n`;
    } else {
      code += `#include <${inc}>\n`;
    }
  }
  code += '\nusing namespace std;\n\n';
  
  for (const st of structs) {
    code += `${st}\n\n`;
  }
  
  for (const fn of functions) {
    code += `${fn}\n\n`;
  }
  
  code += `int main() {\n`;
  for (const m of mainCodes) {
    code += `    ${m}\n`;
  }
  code += `    return 0;\n}\n`;
  return code;
}
