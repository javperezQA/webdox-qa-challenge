from playwright.sync_api import Page, Locator

class AdminOffersPage:
    def __init__(self, page: Page):
        self.page = page
        self.container = page.get_by_test_id("offers-container")
        self.nav_offers = page.get_by_test_id("nav-offers")
        self.nav_settings = page.get_by_test_id("nav-settings")
        self.generate_offers = page.get_by_test_id("generate-offers-btn")

        self.filter_all = page.get_by_test_id("filter-button-TODAS")
        self.filter_pending = page.get_by_test_id("filter-button-PENDIENTE")
        self.filter_accepted = page.get_by_test_id("filter-button-ACEPTADA")

        self.toast = page.get_by_test_id("toast-notification")

    def open(self):
        self.nav_offers.click()

    def rows(self) -> Locator:
        return self.page.locator('[data-testid^="offer-row-"]')

    def status_badge(self, row: Locator) -> Locator:
        return row.locator('[data-testid^="status-badge-"]')

    def generate_batch(self):
        self.generate_offers.click()

    def filter_pending_offers(self):
        self.filter_pending.click()
