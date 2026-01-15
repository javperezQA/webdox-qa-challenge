from playwright.sync_api import Page

class AdminSettingsPage:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.get_by_test_id("settings-container")
        self.nav_settings = page.get_by_test_id("nav-settings")

        self.smart_discount_toggle = page.get_by_test_id("smart-discount-toggle")
        self.save_system = page.get_by_test_id("save-system-btn")

        self.notifications_toggle = page.get_by_test_id("notifications-toggle")
        self.save_notifications = page.get_by_test_id("save-notifications-btn")

        self.toast = page.get_by_test_id("toast-notification")

    def open(self):
        self.nav_settings.click()

    def toggle_smart_discount(self) -> bool:
        initial = self.smart_discount_toggle.is_checked()
        self.smart_discount_toggle.click()
        return initial

    def save_system_settings(self):
        self.save_system.click()
