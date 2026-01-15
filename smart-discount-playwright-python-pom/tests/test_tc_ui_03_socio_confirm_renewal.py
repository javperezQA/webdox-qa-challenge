from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.socio_dashboard_page import SocioDashboardPage

def test_tc_ui_03_socio_confirm_renewal(page):
    login = LoginPage(page)
    socio = SocioDashboardPage(page)

    login.goto()
    login.login_as("socio")

    expect(socio.dashboard).to_be_visible()
    expect(socio.promo_card).to_be_visible()

    socio.confirm_renewal()

    expect(socio.toast).to_be_visible()
    expect(socio.toast).to_contain_text("¡Felicidades! Tu renovación con descuento ha sido procesada")
