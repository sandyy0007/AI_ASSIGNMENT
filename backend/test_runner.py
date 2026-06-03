"""
Test runner for AI App Config Compiler
Tests the pipeline with sample prompts
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from pipeline.intent_extraction import IntentExtractor
from pipeline.system_design import SystemDesigner
from pipeline.schema_generation import SchemaGenerator
from pipeline.validation_layer import ValidationLayer
from pipeline.repair_engine import RepairEngine
from pipeline.execution_simulator import ExecutionSimulator
from pipeline.evaluation_framework import EvaluationFramework
from test_prompts import NORMAL_PROMPTS, EDGE_CASE_PROMPTS
import time
import json


def run_pipeline_test(prompt, context=None):
    """Run full pipeline test on a single prompt"""
    print(f"\n{'='*70}")
    print(f"Testing: {prompt[:60]}...")
    print(f"{'='*70}")

    try:
        # Stage 1
        print("[1/7] Intent Extraction...", end=" ", flush=True)
        start = time.time()
        intent_extractor = IntentExtractor()
        intent_result = intent_extractor.extract(prompt)
        print(f"✓ ({time.time()-start:.2f}s)")
        if not intent_result.get("success"):
            print(f"  Error: {intent_result.get('error')}")
            return False

        # Stage 2
        print("[2/7] System Design...", end=" ", flush=True)
        start = time.time()
        designer = SystemDesigner()
        design_result = designer.design(intent_result)
        print(f"✓ ({time.time()-start:.2f}s)")
        if not design_result.get("success"):
            print(f"  Error: {design_result.get('error')}")
            return False

        # Stage 3
        print("[3/7] Schema Generation...", end=" ", flush=True)
        start = time.time()
        generator = SchemaGenerator()
        schema_result = generator.generate(design_result)
        print(f"✓ ({time.time()-start:.2f}s)")
        if not schema_result.get("success"):
            print(f"  Error: {schema_result.get('error')}")
            return False

        # Prepare config
        config = {
            **intent_result.get("data", {}),
            **design_result.get("data", {}),
            **schema_result.get("data", {})
        }

        # Stage 4
        print("[4/7] Validation...", end=" ", flush=True)
        start = time.time()
        validator = ValidationLayer()
        validation_result = validator.validate(config)
        print(f"✓ ({time.time()-start:.2f}s)")

        # Stage 5
        print("[5/7] Repair Engine...", end=" ", flush=True)
        start = time.time()
        errors = validation_result.get("data", {}).get("errors", [])
        repairer = RepairEngine()
        repair_result = repairer.repair(config, errors)
        print(f"✓ ({time.time()-start:.2f}s)")
        if repair_result.get("data", {}).get("was_repaired"):
            config = repair_result.get("data", {}).get("repaired_config", config)
            print(f"  → {repair_result.get('repairs_applied')} repairs applied")

        # Stage 6
        print("[6/7] Execution Simulator...", end=" ", flush=True)
        start = time.time()
        simulator = ExecutionSimulator()
        simulation_result = simulator.simulate(config)
        print(f"✓ ({time.time()-start:.2f}s)")

        # Stage 7
        print("[7/7] Evaluation Framework...", end=" ", flush=True)
        start = time.time()
        evaluator = EvaluationFramework()
        evaluation_result = evaluator.evaluate(config, validation_result, simulation_result)
        print(f"✓ ({time.time()-start:.2f}s)")

        # Print results
        overall_score = evaluation_result.get("overall_score", 0)
        print(f"\n  Overall Score: {overall_score:.1f}/100")
        print(f"  App Name: {config.get('app_name', 'N/A')}")
        print(f"  Entities: {len(config.get('entities', []))}")
        print(f"  Roles: {len(config.get('roles', []))}")
        print(f"  API Endpoints: {len(config.get('api_schema', {}).get('endpoints', []))}")
        print(f"  DB Tables: {len(config.get('database_schema', {}).get('tables', []))}")
        print(f"  Valid: {validation_result.get('data', {}).get('is_valid', False)}")

        return True

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def main():
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║       AI App Config Compiler - Pipeline Tests                      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    # Test normal prompts
    print("\n\n📋 TESTING NORMAL PROMPTS (10 cases)")
    normal_passed = 0
    for i, test_case in enumerate(NORMAL_PROMPTS, 1):
        if run_pipeline_test(test_case["prompt"], test_case.get("context")):
            normal_passed += 1

    # Test edge cases
    print("\n\n⚠️  TESTING EDGE CASES (10 cases)")
    edge_passed = 0
    for i, test_case in enumerate(EDGE_CASE_PROMPTS, 1):
        if run_pipeline_test(test_case["prompt"], test_case.get("context")):
            edge_passed += 1

    # Summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Normal Prompts:  {normal_passed}/10 passed ({'✓' if normal_passed >= 8 else '✗'})")
    print(f"Edge Cases:      {edge_passed}/10 passed ({'✓' if edge_passed >= 5 else '⚠'})")
    print(f"Total:           {normal_passed + edge_passed}/20 passed")
    print(f"Success Rate:    {((normal_passed + edge_passed) / 20) * 100:.1f}%")
    print(f"{'='*70}\n")

    return normal_passed >= 8 and edge_passed >= 5


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
