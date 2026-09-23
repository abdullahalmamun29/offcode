/**
 * Filesystem Abstraction Layer for CHUP Runtime Discovery.
 *
 * Provides a mockable filesystem interface to enable deterministic cross-platform
 * candidate discovery testing on any OS.
 */

import * as fs from "fs";

export interface IFileStat {
  isFile(): boolean;
  isDirectory(): boolean;
}

export interface IFileSystem {
  existsSync(filePath: string): boolean;
  statSync(filePath: string): IFileStat;
}

export class NodeFileSystem implements IFileSystem {
  public existsSync(filePath: string): boolean {
    return fs.existsSync(filePath);
  }

  public statSync(filePath: string): IFileStat {
    return fs.statSync(filePath);
  }
}

export class MockFileSystem implements IFileSystem {
  private files = new Set<string>();
  private directories = new Set<string>();
  private caseInsensitive: boolean;

  constructor(caseInsensitive: boolean = false) {
    this.caseInsensitive = caseInsensitive;
  }

  private normalize(p: string): string {
    return this.caseInsensitive ? p.toLowerCase() : p;
  }

  public addFile(filePath: string): this {
    this.files.add(this.normalize(filePath));
    return this;
  }

  public addDirectory(dirPath: string): this {
    this.directories.add(this.normalize(dirPath));
    return this;
  }

  public existsSync(filePath: string): boolean {
    const norm = this.normalize(filePath);
    return this.files.has(norm) || this.directories.has(norm);
  }

  public statSync(filePath: string): IFileStat {
    const norm = this.normalize(filePath);
    const isFile = this.files.has(norm);
    const isDir = this.directories.has(norm);

    if (!isFile && !isDir) {
      throw new Error(`ENOENT: no such file or directory, stat '${filePath}'`);
    }

    return {
      isFile: () => isFile,
      isDirectory: () => isDir
    };
  }
}
