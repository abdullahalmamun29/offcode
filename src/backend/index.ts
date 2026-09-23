/**
 * CHUP / Offcode — Backend Subsystem (Phase 5)
 *
 * Public exports for backend contracts, registry, and specialized adapters.
 */

export * from '../models/backendModel';
export * from './backendRegistry';
export * from './adapters/dataStructureAdapter';
export * from './adapters/numericalAdapter';
export * from './adapters/cp/sequenceAdapter';
export * from './adapters/cp/graphAdapter';
export * from './adapters/cp/stringAdapter';
export * from './backends/dataStructureBackend';
export * from './backends/numericalBackend';
export * from './backends/cpAlgorithmBackend';
