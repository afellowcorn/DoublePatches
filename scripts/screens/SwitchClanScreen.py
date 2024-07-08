import logging

import pygame
import pygame_gui

from scripts.clan import Clan
from scripts.game_structure.game_essentials import (
    game,
    screen,
    screen_x,
    screen_y,
    MANAGER,
    offset,
)
from scripts.game_structure.ui_elements import UIImageButton
from scripts.game_structure.windows import DeleteCheck
from scripts.utility import (
    get_text_box_theme,
    ui_scale,
    ui_scale_dimensions,
)  # pylint: disable=redefined-builtin
from .Screens import Screens

logger = logging.getLogger(__name__)


class SwitchClanScreen(Screens):
    """
    TODO: DOCS
    """

    def handle_event(self, event):
        """
        TODO: DOCS
        """
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if game.switches["window_open"]:
                pass
            elif event.ui_element == self.main_menu:
                self.change_screen("start screen")
            elif event.ui_element == self.next_page_button:
                self.page += 1
                self.update_page()
            elif event.ui_element == self.previous_page_button:
                self.page -= 1
                self.update_page()
            else:
                for page in self.delete_buttons:
                    if event.ui_element in page:
                        DeleteCheck(
                            self.change_screen,
                            self.clan_name[self.page][page.index(event.ui_element)],
                        )

                        return

                for page in self.clan_buttons:
                    if event.ui_element in page:
                        Clan.switch_clans(
                            self.clan_name[self.page][page.index(event.ui_element)]
                        )

        elif event.type == pygame.KEYDOWN and game.settings["keybinds"]:
            if event.key == pygame.K_ESCAPE:
                self.change_screen("start screen")

    def exit_screen(self):
        """
        TODO: DOCS
        """
        self.main_menu.kill()
        del self.main_menu
        self.info.kill()
        del self.info
        self.current_clan.kill()
        del self.current_clan

        # del self.screen  # No need to keep that in memory.

        for page in self.clan_buttons:
            for button in page:
                button.kill()
                del button  # pylint: disable=modified-iterating-list

        for page in self.delete_buttons:
            for button in page:
                button.kill()
                del button  # pylint: disable=modified-iterating-list

        self.next_page_button.kill()
        del self.next_page_button
        self.previous_page_button.kill()
        del self.previous_page_button
        self.page_number.kill()
        del self.page_number

        self.clan_buttons = [[]]
        self.delete_buttons = [[]]
        self.clan_name = [[]]

    def screen_switches(self):
        """
        TODO: DOCS
        """
        self.screen = pygame.transform.scale(
            pygame.image.load("resources/images/clan_saves_frame.png").convert_alpha(),
            ui_scale_dimensions((220, 368)),
        )
        self.main_menu = UIImageButton(
            ui_scale(pygame.Rect((25, 25), (153, 30))),
            "",
            object_id="#main_menu_button",
            manager=MANAGER,
        )
        self.info = pygame_gui.elements.UITextBox(
            "Note: This will close the game.\n When you open it next, it should have the new Clan.",
            # pylint: disable=line-too-long
            ui_scale(pygame.Rect((100, 600), (600, 70))),
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER,
        )

        self.current_clan = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((0, 100), (600, 30))),
            object_id="#medium_text_xcenter",
            manager=MANAGER,
            anchors={"centerx": "centerx"},
        )
        if game.clan:
            self.current_clan.set_text(
                f"The currently loaded Clan is {game.clan.name}Clan"
            )
        else:
            self.current_clan.set_text("There is no Clan currently loaded.")

        self.clan_list = game.read_clans()

        self.clan_buttons = [[]]
        self.clan_name = [[]]
        self.delete_buttons = [[]]

        i = 0
        y_pos = 190
        for clan in self.clan_list[1:]:
            self.clan_name[-1].append(clan)
            self.clan_buttons[-1].append(
                pygame_gui.elements.UIButton(
                    ui_scale(pygame.Rect((0, y_pos), (200, 40))),
                    clan + "Clan",
                    object_id="@heading",
                    manager=MANAGER,
                    anchors={"centerx": "centerx"},
                )
            )
            self.delete_buttons[-1].append(
                UIImageButton(
                    ui_scale(pygame.Rect((470, y_pos + 8), (22, 22))),
                    "",
                    object_id="#exit_window_button",
                    manager=MANAGER,
                    starting_height=2,
                )
            )

            y_pos += 40
            i += 1
            if i >= 8:
                self.clan_buttons.append([])
                self.clan_name.append([])
                self.delete_buttons.append([])
                i = 0
                y_pos = 190

        self.next_page_button = UIImageButton(
            ui_scale(pygame.Rect((456, 540), (34, 34))),
            "",
            object_id="#arrow_right_button",
            manager=MANAGER,
        )
        self.previous_page_button = UIImageButton(
            ui_scale(pygame.Rect((310, 540), (34, 34))),
            "",
            object_id="#arrow_left_button",
            manager=MANAGER,
        )
        self.page_number = pygame_gui.elements.UITextBox(
            "",
            ui_scale(pygame.Rect((0, 540), (110, 35))),
            object_id="#medium_text_xcenter",
            manager=MANAGER,
            anchors={
                "left": "left",
                "right": "right",
                "left_target": self.previous_page_button,
                "right_target": self.next_page_button,
            },
        )
        self.page = 0

        self.update_page()

        return super().screen_switches()

    def update_page(self):
        """
        TODO: DOCS
        """

        if self.page == 0:
            self.previous_page_button.disable()
        else:
            self.previous_page_button.enable()

        if self.page >= len(self.clan_buttons) - 1:
            self.next_page_button.disable()
        else:
            self.next_page_button.enable()

        self.page_number.set_text(f"Page {self.page + 1} of {len(self.clan_buttons)}")

        for page in self.clan_buttons:
            for button in page:
                button.hide()
        for page in self.delete_buttons:
            for button in page:
                button.hide()

        for button in self.clan_buttons[self.page]:
            button.show()

        for button in self.delete_buttons[self.page]:
            button.show()

    def on_use(self):
        """
        TODO: DOCS
        """
        super().on_use()
        screen.blit(
            self.screen,
            (580 / 1600 * screen_x + offset[0], 302 / 1400 * screen_y + offset[1]),
        )
