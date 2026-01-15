from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.admin_offers_page import AdminOffersPage

def test_tc_ui_02_admin_generate_and_filter_pending(page):
    login = LoginPage(page)
    offers = AdminOffersPage(page)

    login.goto()
    login.login_as("admin")

    expect(offers.container).to_be_visible()

    offers.generate_batch()
    expect(offers.toast).to_be_visible()
    expect(offers.toast).to_contain_text("Lote de ofertas generado correctamente")

    offers.filter_pending_offers()

    rows = offers.rows()
    assert rows.count() > 0, "No hay filas para validar en la tabla de ofertas"

    for i in range(rows.count()):
        row = rows.nth(i)
        expect(offers.status_badge(row)).to_have_text("PENDIENTE")
