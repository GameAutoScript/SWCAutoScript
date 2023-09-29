from module.base.timer import Timer
from module.logger import logger
from module.base.button import ClickPos
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.login.assets.assets_login import *


class Login(UI):
    def _handle_app_login(self):
        """
        Pages:
            in: Any page
            out: page_main

        Raises:
            GameStuckError:
            GameTooManyClickError:
        """
        logger.hr('App login')

        orientation_timer = Timer(5)
        login_success = False

        while 1:
            # Watch device rotation
            if not login_success and orientation_timer.reached():
                # Screen may rotate after starting an app
                self.device.get_orientation()
                orientation_timer.reset()

            self.device.screenshot()

            # End
            if self.ui_page_appear(page_main):
                logger.info('Login to main confirm')
                break

            # Login
            if self.appear_then_click(LOGIN_CLOSE_TIP):
                continue
            if self.appear_then_click(GOOGLE_SURE):
                continue
            if self.appear_then_click(LGOIN_START):
                continue
            if self.appear_then_click(LOGIN_START_GAME):
                continue
            # Additional
            if self.ui_additional():
                continue

        return True

    def handle_app_login(self):
        self.device.screenshot_interval_set(1.0)
        try:
            self._handle_app_login()
        finally:
            self.device.screenshot_interval_set()

    def app_stop(self):
        logger.hr('App stop')
        self.device.app_stop()

    def app_start(self):
        logger.hr('App start')
        self.device.app_start()
        self.handle_app_login()

    def app_restart(self):
        logger.hr('App restart')
        self.device.app_stop()
        self.device.app_start()
        self.handle_app_login()
        self.config.task_delay(server_update=True)
