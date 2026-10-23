"""End-to-end Chromium tests against an offline operations portal fixture."""
from pathlib import Path
import unittest
from playwright.sync_api import sync_playwright

PORTAL = (Path(__file__).resolve().parents[1] / "examples" / "demo_order_portal.html").as_uri()


class OrderPortalBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.page.goto(PORTAL)

    def tearDown(self):
        self.context.close()

    def test_happy_path_queues_order(self):
        self.page.get_by_label("Order ID").fill("ORD-1001")
        self.page.get_by_label("Quantity").fill("3")
        self.page.get_by_label("Shipping method").select_option("Express")
        self.page.get_by_role("button", name="Queue order").click()
        output = self.page.get_by_role("status")
        self.assertEqual(output.get_attribute("data-state"), "success")
        self.assertIn("ORD-1001 queued: 3 item(s) via Express", output.inner_text())
        screenshot_path = Path("artifacts/browser/order-success.png")
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(screenshot_path), full_page=True)

    def test_rejects_invalid_order_id(self):
        self.page.get_by_label("Order ID").fill("BAD-77")
        self.page.get_by_role("button", name="Queue order").click()
        output = self.page.get_by_role("status")
        self.assertEqual(output.get_attribute("data-state"), "error")
        self.assertIn("Invalid order ID", output.inner_text())

    def test_rejects_invalid_quantity(self):
        self.page.get_by_label("Order ID").fill("ORD-1002")
        self.page.get_by_label("Quantity").fill("0")
        self.page.get_by_role("button", name="Queue order").click()
        output = self.page.get_by_role("status")
        self.assertEqual(output.get_attribute("data-state"), "error")
        self.assertIn("Quantity must be between 1 and 100", output.inner_text())


if __name__ == "__main__":
    unittest.main()
