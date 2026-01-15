import os
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.form = page.get_by_test_id("login-form")
        self.email = page.get_by_test_id("email-input")
        self.password = page.get_by_test_id("password-input")
        self.role = page.get_by_test_id("role-select")
        self.submit = page.get_by_test_id("login-submit-btn")

    def goto(self):
        base_url = os.getenv("BASE_URL", "http://127.0.0.1:5173")
        self.page.goto(base_url)

    def login_as(self, role: str, email: str | None = None, password: str = "Password123"):
        if email is None:
            email = f"{role}@demo.com"
        self.email.fill(email)
        self.password.fill(password)
        self.role.select_option(role)
        self.submit.click()
