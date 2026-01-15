from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.admin_offers_page import AdminOffersPage
from pages.admin_settings_page import AdminSettingsPage

def test_tc_ui_01_admin_toggle_smart_discount(page):
    login = LoginPage(page)
    offers = AdminOffersPage(page)
    settings = AdminSettingsPage(page)

    login.goto()
    login.login_as("admin")

    expect(offers.container).to_be_visible()

    settings.open()
    expect(settings.container).to_be_visible()

    initial = settings.toggle_smart_discount()
    expect(settings.smart_discount_toggle).to_have_js_property("checked", not initial)

    settings.save_system_settings()
    expect(settings.toast).to_be_visible()
    expect(settings.toast).to_contain_text("Estado del algoritmo Smart Discoount 2.0 actualizado")
