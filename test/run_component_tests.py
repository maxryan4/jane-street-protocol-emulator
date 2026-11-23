import os
from pathlib import Path
import subprocess
import sys


def discover_tests():
    for root, directories, filenames in os.walk("."):
        directories[:] = [name for name in directories if not name.startswith(".") and name not in {"sim_build", "output", "__pycache__"}]

        for filename in filenames:
            if filename.startswith("test_") and filename.endswith(".py"):
                test_file = Path(root) / filename
                lines = test_file.read_text(encoding="utf-8").splitlines()
                if any(line.strip() and not line.lstrip().startswith("#") for line in lines):
                    yield test_file


def main(make, source_dir, *project_sources):
    rtl_files = {path.relative_to(source_dir) for path in Path(source_dir).rglob("*") if path.suffix in {".sv", ".v"} and path.is_file()}
    # honour explicit compile order before appending discovered sources
    ordered_sources = [Path(path) for path in project_sources]
    sources = " ".join(str(path) for path in [*ordered_sources, *sorted(rtl_files.difference(ordered_sources))])

    for test_file in sorted(discover_tests()):
        module = test_file.stem.removeprefix("test_")
        rtl_path = test_file.with_name(module)
        if rtl_path.with_suffix(".sv") not in rtl_files and rtl_path.with_suffix(".v") not in rtl_files:
            print(f"No matching RTL for {test_file}", file=sys.stderr)
            return 1

        bench = test_file.with_name(f"tb_{module}.sv")
        testbench_source = bench if bench.is_file() else ""
        top = bench.stem if testbench_source else module
        test_module = ".".join(test_file.with_suffix("").parts)
        build_dir = Path("sim_build/unit") / test_file.with_suffix("")

        result = subprocess.run([
            make, "-B", "sim",
            f"PROJECT_SOURCES={sources}",
            f"TESTBENCH_SOURCE={testbench_source}",
            f"COCOTB_TOPLEVEL={top}",
            f"COCOTB_TEST_MODULES={test_module}",
            f"SIM_BUILD={build_dir}",
            f"COCOTB_RESULTS_FILE={build_dir / 'results.xml'}",
        ])
        if result.returncode:
            return result.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
