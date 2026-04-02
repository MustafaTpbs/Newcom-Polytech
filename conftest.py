import pytest
import hardpy
from hardpy import JsonLoader, get_current_report
from pathlib import Path

def finish_executing():
    print("Testing completed")


@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(finish_executing)
    yield


def save_report_to_dir():
    report = get_current_report()
    if report:
        loader = JsonLoader(Path.cwd() / "reports")
        loader.load(report)
        
@pytest.fixture(scope="session", autouse=True)
def fill_actions_after_test(post_run_functions: list):
    post_run_functions.append(save_report_to_dir)
    yield