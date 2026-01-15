from playwright.sync_api import Page

class SocioDashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.dashboard = page.get_by_test_id("socio-dashboard")
        self.promo_card = page.get_by_test_id("discount-promo-card")
        self.confirm_btn = page.get_by_test_id("confirm-discount-btn")
        self.toast = page.get_by_test_id("toast-notification")

    def confirm_renewal(self):
        self.confirm_btn.click()
