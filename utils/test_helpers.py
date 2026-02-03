# utils/test_helpers.py
import os
import time
from config.config import Config

class TestStats:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0

    def record(self, status: bool):
        self.total += 1
        if status:
            self.passed += 1
        else:
            self.failed += 1

    def summary_text(self) -> str:
        if self.total == 0:
            return "No tests were run."
        passed_pct = self.passed / self.total * 100
        lines = []
        lines.append(f"Total Tests Run: {self.total}")
        lines.append(f"✅ Passed: {self.passed} ({passed_pct:.1f}%)")
        lines.append(f"❌ Failed: {self.failed} ({100-passed_pct:.1f}%)")
        if self.failed == 0:
            lines.append("🎉 ALL TESTS PASSED! Website is functioning perfectly!")
        elif self.failed < self.total * 0.1:
            lines.append("✅ EXCELLENT! More than 90% tests passed!")
        elif self.failed < self.total * 0.2:
            lines.append("👍 GOOD! More than 80% tests passed!")
        else:
            lines.append("⚠️ ATTENTION NEEDED! Some critical tests failed.")
        return "\n".join(lines)


class TestHelper:
    def __init__(self, stats: TestStats, driver=None):
        self.stats = stats
        self.driver = driver
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)

    def test_result(self, test_name: str, status: bool, message: str = ""):
        self.stats.record(status)
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}")
        if message:
            print(f"   → {message}")

    def take_screenshot(self, filename: str):
        if not self.driver:
            return
        path = os.path.join(Config.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(path)
        return path
