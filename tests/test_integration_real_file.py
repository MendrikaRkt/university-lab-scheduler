"""Optional integration test on the real Asignacion_2025-2026_v5.xlsx file.

Automatically skipped if the source file is not present (CI without data).
"""
import os

import pytest

from infrastructure.config.config_loader import get_settings
from infrastructure.excel.excel_reader import ExcelReader, SubjectMatcher

REAL_FILE = "/home/ubuntu/Uploads/Asignacion_2025-2026_v5.xlsx"
pytestmark = pytest.mark.skipif(
    not os.path.exists(REAL_FILE), reason="source file not available")


def test_real_file_loads_lab_subjects():
    settings = get_settings()
    matcher = SubjectMatcher.from_settings(settings)
    reader = ExcelReader(settings.sessions_per_credit)
    profs = reader.read_professor_credits(REAL_FILE, subject_matcher=matcher)
    # At least about twenty teachers with P credits
    assert len(profs) >= 20
    # Expected sessions must be positive integers
    subjects = {s for p in profs for s in p.subjects()}
    assert len(subjects) >= 15


def test_real_file_mecanismos_six_credits():
    settings = get_settings()
    matcher = SubjectMatcher.from_settings(settings)
    reader = ExcelReader(settings.sessions_per_credit)
    profs = reader.read_professor_credits(REAL_FILE, subject_matcher=matcher)
    total_p = sum(p.practice_credits("S1_Mecanismos") for p in profs)
    # Mecanismos = 6 P credits in total => 30 expected sessions
    assert round(total_p) == 6
