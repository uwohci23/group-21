import os
import tkinter
from dataclasses import dataclass
from typing import Any, Union

from PIL import Image, ImageTk

from .lib import Card, Dealer, Hand, Player, Shoe, get_correct_play

from tkinter import messagebox

import pygame
from pygame import mixer

N_CARDS_MAX = 9
IMG_PATH = f"{os.path.dirname(__file__)}/images/"
USER_BET = 0
BC = "#2B674D"

pygame.mixer.init()
#shuffling sound effect
shuffle_sfx = pygame.mixer.Sound("card_shuffle.mp3")
#handing out cards (start of match) sound effect
passing_sfx = pygame.mixer.Sound("card_dealing.mp3")
#hit sound effect
hit_sfx = pygame.mixer.Sound("card_hit.mp3")
#bet sound effect
bet_sfx = pygame.mixer.Sound("chip_bet.mp3")

@dataclass
class Gui:
    root: tkinter.Frame
    menu: dict
    label_text: tkinter.StringVar
    slot_player: dict
    slot_dealer: dict
    info_text: dict
    info: dict
    chips: dict
    finger: dict
    shoe_progress: tkinter.Label
    fix_mistakes: tkinter.IntVar
    insurance_chip: tkinter.Label
    dealer_info: tkinter.Label
    rebet_button: tkinter.Button
    dealer_card_values: tkinter.StringVar  # Add dealer_card_values as an attribute
    player_card_values: tkinter.StringVar  # Add player_card_values as an attribute
    betChips: list = None


class Game:
    def __init__(self, player: Player, dealer: Dealer, gui: Gui, args: Any):
        self.player = player
        self.dealer = dealer
        self.gui = gui
        self.args = args
        self.bet = args.bet
        self.shoe = self.init_shoe()
        self.active_slot = None
        self.initial_bet = args.bet

    def deal(self):
        """Starts new round."""
        global USER_BET

        if USER_BET == 0:
            self.display_info("Please bet")
        else:
            passing_sfx.play()
            self.display_info("")
            self.bet = USER_BET
            self.disable_chips()
            self.hide_all_chips()
            self.hide_insurance_chip()
            self.hide_fingers()
            self.clean_player_slots()
            self.dealer_info()
            self.player.hands = []
            if self.shoe.n_cards < 52:
                self.shoe = Shoe(6)
                self.player.init_count()
            hand = self.player.start_new_hand(self.bet)
            self.dealer.init_hand()
            if self.args.dealer_cards is not None:
                self.shoe.arrange(self.args.dealer_cards)
            self.dealer.deal(self.shoe, self.gui.shoe_progress)
            self.dealer.deal(self.shoe, self.gui.shoe_progress)
            self.dealer.cards[1].visible = False
            self.display_dealer_cards()
            if self.args.cards is not None:
                self.shoe.arrange(self.args.cards)
            hand.deal(self.shoe, self.gui.shoe_progress)
            hand.deal(self.shoe, self.gui.shoe_progress)
            self.show_buttons()
            self.hide_buttons(("deal",))
            self.show()
            self.active_slot = hand.slot
            self.enable_correct_buttons(hand)
            self.display_chip(0,hand)
            self.display_player_cards(hand)
            self.gui.player_card_values.set(f"Player: {hand.sum}")
            self.gui.dealer_card_values.set(f"Dealer: {self.dealer.preFlip}")

            if self.dealer.cards[0].label != "A":
                self.hide_buttons(("insurance", "even-money"))
                if hand.is_blackjack:
                    self.resolve_blackjack()
            else:
                self.hide_buttons(("surrender",))
                if hand.is_blackjack is True:
                    self.show_buttons(("even-money",))
                    self.hide_buttons(("insurance",))
                else:
                    self.show_buttons(("insurance",))
                    self.hide_buttons(("even-money",))


    def surrender(self):
        """Method for Surrender button."""
        if self.gui.fix_mistakes.get() == 1:
            if self.check_play(self.player.hands[0], "surrender") is False:
                return
        self.player.stack += self.bet / 2
        self.display_stack()
        self.player.update_count(self.dealer, self.shoe)
        self.deal()

    def even_money(self):
        """Method for Even Money button"""
        hand = self.get_hand_in_active_slot()
        if self.gui.fix_mistakes.get() == 1:
            if self.check_insurance(hand) is False:
                return
        self.dealer.even_money = True
        self.hide(hand)
        self.payout()

    def double(self):
        """Method for Double button."""
        hand = self.get_hand_in_active_slot()
        if self.player.stack - USER_BET > 0:
            if self.gui.fix_mistakes.get() == 1:
                if self.check_play(hand, "double") is False:
                    return
            self.hide_buttons(("surrender",))
            self.player.stack -= self.bet
            self.display_stack()
            hand.bet += self.bet
            hand.deal(self.shoe, self.gui.shoe_progress)

            self.display_chip(1, hand)
            hand.is_finished = True
            self.gui.player_card_values.set(f"Player: {hand.sum}")
            self.display_player_cards(hand, rotate_last=True)
            if hand.sum > 21:
                self.hide(hand)
                self.hide_chips(hand)
            self.clean_info()
            self.resolve_next_hand()
        else:
            self.display_info("You do not have enough to double")
    def reset(self):
        """Method for Reset button."""

        self.player.buy_in(self.player.initial_stack)
        self.shoe = self.init_shoe()
        self.clean_dealer_slots()
        self.player.init_count()
        USER_BET = 0
        self.display_chip(0)
        self.display_stack()
        self.clean_info()
        self.hide_all_chips()
        self.hide_insurance_chip()
        self.hide_fingers()
        self.clean_player_slots()
        shuffle_sfx.play() #play sound effect


    def disable_chips(self):
        for chip in self.gui.betChips:
            chip.configure(state= tkinter.DISABLED)

    def enable_chips(self):
        for chip in self.gui.betChips:
            chip.configure(state= tkinter.NORMAL)


    def next(self):
        """Methods for Next button."""
        self.clean_info()
        self.clean_dealer_slots()
        self.deal()

    def hit(self):
        """Method for Hit button."""
        hit_sfx.play() #play sound effect
        hand = self.get_hand_in_active_slot()
        if self.gui.fix_mistakes.get() == 1:
            if self.check_play(hand, "hit") is False:
                return
        self.hide_buttons(("surrender", "double"))
        hand.deal(self.shoe, self.gui.shoe_progress)
        self.display_player_cards(hand)
        self.gui.player_card_values.set(f"Player: {hand.sum}")
        if hand.is_over is True:
            self.hide(hand)
            self.hide_chips(hand)
            self.display_info("BUST", hand)
        if hand.is_finished is False:
            self.enable_correct_buttons(hand)
        else:
            self.resolve_next_hand()

    def stay(self):
        """Method for Stay button."""
        hand = self.get_hand_in_active_slot()
        if self.gui.fix_mistakes.get() == 1:
            if self.check_play(hand, "stay") is False:
                return
        hand.is_finished = True
        self.resolve_next_hand()

    def insurance(self):
        """Method for Insurance button."""
        hand = self.get_hand_in_active_slot()
        if self.gui.fix_mistakes.get() == 1:
            if self.check_insurance(hand) is False:
                return
        self.dealer.insurance_bet = hand.bet / 2
        self.display_insurance_chip()
        self.player.stack -= self.dealer.insurance_bet
        self.display_stack()
        self.hide_buttons(("insurance",))

    def split(self):
        """Method for Split button."""
        hand = self.get_hand_in_active_slot()
        if self.gui.fix_mistakes.get() == 1:
            if self.check_play(hand, "split") is False:
                return
        self.hide_buttons(("surrender",))
        new_hand = self.player.start_new_hand(self.bet)
        split_card = hand.cards.pop()
        new_hand.deal(split_card, self.gui.shoe_progress)
        self.display_chip(0, new_hand)
        self.display_stack()
        for handy in (hand, new_hand):
            handy.is_split_hand = True
            handy.deal(self.shoe, self.gui.shoe_progress)
            if handy.cards[0].label == "A":
                # Split Aces receive only one card more
                handy.is_hittable = False
                handy.is_finished = True

        self.player.sort_hands()
        if len(self.player.hands) < 4:
            self.player.hands.sort(key=lambda x: not x.cards[0].value == x.cards[1].value)
        for hand in self.player.hands:
            rotate = hand.cards[0].label == "A" and hand.cards[1].label != "A"
            self.display_player_cards(hand, rotate_last=rotate)
        self.resolve_next_hand()

    def resolve_next_hand(self):
        """Moves to next unfinished hand."""
        hand = self.get_first_unfinished_hand()

        if hand is not None:
            self.active_slot = hand.slot
            self.enable_correct_buttons(hand)
            self.display_finger(hand)
            self.gui.player_card_values.set(f"Player: {hand.sum}")
        else:
            self.clean_info()
            if self.is_all_over() is False or self.dealer.insurance_bet > 0:
                self.display_dealer_cards(hide_second=False)
                self.dealer.cards[1].visible = True
                if self.dealer.is_blackjack and self.dealer.insurance_bet > 0:
                    self.display_insurance_chip(triple=True)
                    self.player.stack += self.dealer.insurance_bet * 3
                else:
                    self.hide_insurance_chip()
                while self.dealer.is_finished is False:
                    self.dealer.deal(self.shoe, self.gui.shoe_progress)
                    self.display_dealer_cards()
            self.payout()

    def increment_bet(self, type: str):
        global USER_BET
        self.hide_all_chips()
        bet_sfx.play() #play sound effect
        if type == "red":
            if self.player.stack - 5 < 0:
                self.display_info("You cannot have a negative balance")
            else:
                USER_BET += 5
                self.player.stack -= 5
        elif type == "blue":
            if self.player.stack - 10 < 0:
                self.display_info("You cannot have a negative balance")
            else:
                USER_BET += 10
                self.player.stack -= 10
        elif type == "green":
            if self.player.stack - 25 < 0:
                self.display_info("You cannot have a negative balance")
            else:
                USER_BET += 25
                self.player.stack -= 25
        elif type == "black":
            if self.player.stack - 50 < 0:
                self.display_info("You cannot have a negative balance")
            else:
                USER_BET += 50
                self.player.stack -= 50
        self.display_chip(0)
        self.display_stack()

    def payout(self):
        global USER_BET
        """Handles payout of all hands."""
        self.hide_fingers()

        for hand in self.player.hands:
            if self.dealer.even_money is True:
                self.player.stack += hand.bet * 2
                result = "EVEN MONEY"
                self._display_chips(hand)
            elif hand.is_blackjack is True and self.dealer.is_blackjack is False:
                self.player.stack += hand.bet * 2.5
                result = "BLACKJACK"
                self._display_chips(hand, bj=True)
            elif hand.is_blackjack is True and self.dealer.is_blackjack is True:
                self.player.stack += hand.bet
                result = "PUSH"
            elif self.dealer.is_blackjack is True and hand.is_blackjack is False:
                self.dealer_info("BLACKJACK")
                result = "LOSE"
                self._resolve_lost_hand(hand)
            elif hand.is_over is False and self.dealer.is_over is True:
                self.gui.dealer_card_values.set(f"Dealer: {self.dealer.sum}")
                self.dealer_info("BUST")
                self.player.stack += hand.bet * 2
                result = ""
                self._display_chips(hand)
            elif hand.is_over is True:
                result = "BUST"
                self._resolve_lost_hand(hand)
            elif hand.sum < self.dealer.sum:
                result = f"LOSE ({hand.sum} vs {self.dealer.sum})"
                self.gui.dealer_card_values.set(f"Dealer: {self.dealer.sum}")
                self._resolve_lost_hand(hand)
            elif hand.surrender is True:
                self.player.stack += hand.bet / 2
                result = ""
            elif hand.sum > self.dealer.sum:
                self.player.stack += hand.bet * 2
                self.gui.dealer_card_values.set(f"Dealer: {self.dealer.sum}")
                result = f"WIN ({hand.sum} vs {self.dealer.sum})"
                self._display_chips(hand)
            elif hand.sum == self.dealer.sum:
                self.player.stack += hand.bet
                result = "PUSH"
            else:
                raise ValueError
            self.display_info(result, hand)
        self.display_stack()
        self.hide_buttons()
        self.show_buttons(("deal",))
        self.player.update_count(self.dealer, self.shoe)
        self.enable_chips()
        self.bet = USER_BET
        USER_BET = 0
        self.gui.rebet_button.configure(state=tkinter.NORMAL)

    def _resolve_lost_hand(self, hand: Hand):
        self.hide_chips(hand)
        self.hide(hand)
        hand.bet = 0

    def resolve_blackjack(self):
        """Resolves player blackjack."""
        self.display_dealer_cards(hide_second=False)
        self.dealer.cards[1].visible = True
        self.payout()

    def enable_correct_buttons(self, hand: Hand):
        """Enables buttons that are OK to press with certain hand."""
        n_hands = len(self.player.hands)
        if len(hand.cards) == 2 and hand.is_hittable is True:
            self.show_buttons(("double",))
        else:
            self.hide_buttons(("double",))
        if hand.cards[0].value == hand.cards[1].value and len(hand.cards) == 2 and n_hands < 4:
            self.show_buttons(("split",))
        else:
            self.hide_buttons(("split",))
        if hand.is_hittable is True:
            self.show_buttons(("hit",))
        else:
            self.hide_buttons(("hit",))

    def check_play(self, hand: Hand, play: str) -> bool:
        """Verifies player decision. It won't complain if you stay when you should take
        insurance because card counting is not expected, just correct basic play."""
        correct_play = get_correct_play(hand, self.dealer.cards[0], len(self.player.hands))
        if correct_play != play:
            self.display_info(f"The correct play is: {correct_play}", hand)
            self.gui.root.after(1000, self.clean_info)
            return False
        return True

    def check_insurance(self, hand: Hand) -> bool:
        """Verifies player decision with insurance / even money. Gives OK when the count is good!"""
        if self.player.true_count < 3:
            self.display_info("Try again!", hand)
            self.gui.root.after(1000, self.clean_info)
            return False
        return True

    def display_stack(self):
        self.gui.label_text.set(f"Stack: {self.player.stack} $")

    def _display_chips(self, hand, bj: bool = False):
        if bj is True:
            self.display_chip(1, hand)
            self.display_chip(4, hand, color="blue")
        elif hand.bet == self.bet:
            self.display_chip(1, hand)
        elif hand.bet == (2 * self.bet):
            self.display_chip(2, hand)
            self.display_chip(3, hand)

    def is_all_over(self) -> bool:
        for hand in self.player.hands:
            if hand.is_over is False and hand.surrender is False:
                return False
        return True

    def get_first_unfinished_hand(self) -> Union[Hand, None]:
        """Finds first unfinished hand."""
        for hand in self.player.hands:
            if hand.is_finished is False:
                return hand
        return None

    def get_hand_in_active_slot(self) -> Hand:
        """Finds hand in active slot."""
        for hand in self.player.hands:
            if hand.slot == self.active_slot:
                self.gui.player_card_values.set(f"Player: {hand.sum}")
                return hand
        raise RuntimeError

    def show(self):
        """Shows all available hands as active."""
        for slot in range(4):
            for n in range(N_CARDS_MAX):
                self.gui.slot_player[f"{str(slot)}{str(n)}"].configure(state=tkinter.NORMAL)

    def hide(self, hand: Hand):
        """Hides cards in slot."""
        for n in range(N_CARDS_MAX):
            self.gui.slot_player[f"{str(hand.slot)}{str(n)}"].configure(state=tkinter.DISABLED)

    def hide_buttons(self, buttons: Union[tuple, None] = None):
        """Hides menu buttons."""
        if buttons is None:
            for key, button in self.gui.menu.items():
                if key != "reset":
                    button.configure(state=tkinter.DISABLED)
                    button.configure(bg=BC, fg=BC)
        else:
            for button in buttons:
                if button in self.gui.menu.keys():
                    self.gui.menu[button].configure(state=tkinter.DISABLED)
                    self.gui.menu[button].configure(bg=BC, fg=BC)


    def show_buttons(self, buttons: Union[tuple, None] = None):
        """Shows menu buttons."""
        if buttons is None:
            for key, button in self.gui.menu.items():
                if key not in ("insurance", "even-money"):
                    button.configure(state=tkinter.NORMAL)
                    button.configure(bg="white", fg="black")
        else:
            for button in buttons:
                if button in self.gui.menu.keys():
                    self.gui.menu[button].configure(state=tkinter.NORMAL)
                    self.gui.menu[button].configure(bg ="white", fg= "black")


    def clean_player_slots(self):
        """Cleans player card slots."""
        for slot in range(4):
            for n in range(N_CARDS_MAX):
                self.gui.slot_player[f"{str(slot)}{str(n)}"].configure(image="", width=0, height=0)

    def clean_dealer_slots(self):
        """Cleans dealer slot."""
        for pos in self.gui.slot_dealer.values():
            pos.configure(image="", width=0)

    def clean_info(self):
        """Removes info text behind all slots."""
        self.gui.dealer_card_values.set(f"")
        self.gui.player_card_values.set(f"")

        for slot in range(4):
            self.gui.info_text[str(slot)].set("")

    def display_dealer_cards(self, hide_second: bool = True):
        """Displays dealer cards."""
        for ind, card in enumerate(self.dealer.cards):
            if ind == 1 and hide_second is True and len(self.dealer.cards) == 2:
                img, width, _ = get_image()
            else:
                img, width, _ = get_image(card)
            self.gui.slot_dealer[str(ind)].configure(image=img, width=width)
            self.gui.slot_dealer[str(ind)].image = img

    def display_player_cards(self, hand: Hand, rotate_last: bool = False):
        """Displays cards of one hand."""
        for ind, card in enumerate(hand.cards):
            rotate = ind == len(hand.cards) - 1 and rotate_last is True
            img, width, height = get_image(card, rotate=rotate)
            self.gui.slot_player[f"{str(hand.slot)}{str(ind)}"].configure(
                image=img, width=width, height=height
            )
            self.gui.slot_player[f"{str(hand.slot)}{str(ind)}"].image = img

    def display_player_hands(self):
        """Displays all player hands on the table."""
        self.clean_player_slots()
        for hand in self.player.hands:
            self.display_player_cards(hand)

    def display_insurance_chip(self, triple: bool = False):
        bet = self.dealer.insurance_bet if triple is False else self.dealer.insurance_bet * 3
        color = "red"
        if bet == 0.5:
            color = "blue"
            text = "0.5"
        elif bet % 1 == 0:
            text = str(round(bet))
        else:
            text = str(bet)
        img = get_chip_image(color)
        self.gui.insurance_chip.configure(
            image=img, compound="center", fg="white", text=text, font="helvetica 10 bold"
        )
        self.gui.insurance_chip.image = img  # type: ignore

    def hide_insurance_chip(self):
        self.gui.insurance_chip.configure(image="", text="")

    def display_chip(self, pos: int,hand: Hand = None, color: str = "red"):
        global USER_BET
        """Displays chip for certain hand and chip position."""
        img = get_chip_image(color)
        if hand is not None:
            if color == "red":
                text = USER_BET
            else:
                text = ".5" if self.bet == 1 else self.bet / 2
            self.gui.chips[f"{str(hand.slot)}{str(pos)}"].configure(
                image=img, compound="center", fg="white", text=text, font="helvetica 10 bold"
            )
            self.gui.chips[f"{str(hand.slot)}{str(pos)}"].image = img
        else:
            self.gui.chips[f"{str(2)}{str(0)}"].configure(
                image=img, compound="center", fg="white", text=USER_BET, font="helvetica 10 bold"
            )
            self.gui.chips[f"{str(2)}{str(0)}"].image = img


    def display_finger(self, hand: Hand):
        """Displays dealer finger over hand."""
        self.hide_fingers()
        img = get_finger_image()
        self.gui.finger[f"{str(hand.slot)}"].configure(image=img)
        self.gui.finger[f"{str(hand.slot)}"].image = img

    def dealer_info(self, text: str = ""):
        self.gui.dealer_info.configure(text=text)

    def hide_chips(self, hand: Hand):
        """Hides chips of a hand."""
        for pos in range(4):
            self.gui.chips[f"{str(hand.slot)}{str(pos)}"].configure(image="", text="")

    def hide_all_chips(self):
        """Hides chips of all hands."""
        for chip in self.gui.chips.values():
            chip.configure(image="", text="")

    def hide_fingers(self):
        """Hides all dealer fingers."""
        for finger in self.gui.finger.values():
            finger.configure(image="")

    def display_info(self, info: str, hand: Hand = None):
        """Prints text below hand."""
        if hand is not None:
            self.gui.info_text[str(hand.slot)].set(info)
        else:
            self.gui.info_text[str(2)].set(info)

    @staticmethod
    def init_shoe():
        return Shoe(6)


def get_image(
    card: Union[Card, None] = None, width: int = 100, height: int = 130, rotate: bool = False
):
    if card is None:
        filename = f"{IMG_PATH}/back.png"
    else:
        prefix = {
            "A": "ace",
            "J": "jack",
            "Q": "queen",
            "K": "king",
        }
        if card.label in prefix:
            fix = prefix[card.label]
        else:
            fix = str(card.value)
        filename = f"{IMG_PATH}/{fix}_of_{card.suit}.png"
    image = Image.open(filename).resize((width, height), Image.ANTIALIAS)
    if rotate is True:
        image = image.resize((height, height))
        image = image.rotate(angle=90)
        image = image.resize((height, width))
        width, height = height, width
    return ImageTk.PhotoImage(image), width, height


def get_chip_image(color: str = "red"):
    size = 50
    filename = f"{IMG_PATH}/{color}.png"
    image = Image.open(filename).resize((size, size), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


def get_finger_image():
    filename = f"{IMG_PATH}/finger2.png"
    image = Image.open(filename).resize((40, 60), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


def round_polygon(canvas, x, y, sharpness, **kwargs):
    sharpness = max(sharpness, 2)
    ratio_multiplier = sharpness - 1
    ratio_divider = sharpness
    points = []
    for i, _ in enumerate(x):
        points.append(x[i])
        points.append(y[i])
        if i != (len(x) - 1):
            points.append((ratio_multiplier * x[i] + x[i + 1]) / ratio_divider)
            points.append((ratio_multiplier * y[i] + y[i + 1]) / ratio_divider)
            points.append((ratio_multiplier * x[i + 1] + x[i]) / ratio_divider)
            points.append((ratio_multiplier * y[i + 1] + y[i]) / ratio_divider)
        else:
            points.append((ratio_multiplier * x[i] + x[0]) / ratio_divider)
            points.append((ratio_multiplier * y[i] + y[0]) / ratio_divider)
            points.append((ratio_multiplier * x[0] + x[i]) / ratio_divider)
            points.append((ratio_multiplier * y[0] + y[i]) / ratio_divider)
            points.append(x[0])
            points.append(y[0])
    return canvas.create_polygon(points, **kwargs, smooth=tkinter.TRUE)


def rebet(self):
    global USER_BET
    if self.player.stack - self.bet < 0:
        self.display_info("You cannot have a negative balance")
    else:
        self.player.stack -= self.bet
        USER_BET = self.bet
        self.hide_all_chips()
        self.display_chip(0)
        self.display_stack()
        self.gui.rebet_button.configure(state = tkinter.DISABLED)



# function to show the help text
def show_help(root):
    help_text = "Blackjack Help\n\n"
    help_text += "Hit: Request another card from the dealer.\n\n"
    help_text += "Stay: End your turn without requesting another card.\n\n"
    help_text += "Double Down: Double your bet and receive only one more card.\n\n"
    help_text += "Split: If you have two cards of the same rank, split them into two separate hands.\n\n"
    help_text += "Surrender: Forfeit your hand and lose half your bet.\n\n"
    help_text += "Insurance: Protect yourself against the dealer having a blackjack when their face-up card is an Ace.\n\n"
    help_text += "Double-up: Double your bet after your first two cards.\n\n"
    help_text += "Even money: Take even money when the dealer has an Ace showing and you have a blackjack.\n\n"

    help_window = tkinter.Toplevel(root)
    help_window.title("Help")

    help_label = tkinter.Label(help_window, text=help_text, font=("Arial", 12), justify="left")
    help_label.pack(fill="both", expand=True)

def main(args):
    root = tkinter.Tk()
    root.geometry("1200x700")
    root.title("Blackjack")
    root.configure(background=BC)

    main_menu_frame = tkinter.Frame(root, height=700, width=1200, background=BC)
    main_menu_frame.pack(fill="both")

    game_frame = tkinter.Frame(root, height=700, width=1200, background=BC)
    credits_frame = tkinter.Frame(root, height=700, width=1200, background=BC)

    rect = tkinter.Canvas(
        game_frame, bg=BC, height=100, width=80, bd=0, highlightthickness=0, relief="ridge"
    )
    rect.place(x=525, y=485)
    round_polygon(rect, [5, 75, 75, 5], [5, 5, 90, 90], 10, width=4, outline="#bbb500", fill=BC)
    rules_text = tkinter.Label(game_frame,
                                  text="BLACKJACK PAYS 3 TO 2\nDealer must stand on a 17 and draw to 16\nInsurance pays 2 to 1",
                                  font=("Helvetica", 14, "italic"),
                                  bg=BC)
    rules_text.place(relx=0.5, rely=0.5, anchor="center")
    # Shoe status
    shoe_status_container = tkinter.Label(game_frame, borderwidth=0, background="white")
    shoe_status_container.place(x=20, y=40, height=150, width=30)
    shoe_progress = tkinter.Label(
        shoe_status_container, background="black", borderwidth=0, anchor="e"
    )
    shoe_label = tkinter.Label(
        game_frame, text="Discard", font="12", borderwidth=0, background=BC, fg="white"
    )
    shoe_label.place(x=5, y=195)

    # Stack info
    label_text = tkinter.StringVar(game_frame)
    label = tkinter.Label(
        game_frame,
        textvariable=label_text,
        font="Helvetica 13 bold",
        borderwidth=0,
        background=BC,
        fg="white",
    )
    label.place(x=430, y=670)

    # Hand info
    x_slot = 250
    padding_left = 20
    info_text = {str(slot): tkinter.StringVar(game_frame) for slot in range(4)}
    info = {
        str(slot): tkinter.Label(
            game_frame,
            textvariable=info_text[str(slot)],
            font="helvetica 11 bold",
            borderwidth=0,
            background=BC,
            fg="white",
        )
        for slot in range(4)
    }
    for ind, i in enumerate(info.values()):
        i.place(x=ind * x_slot + padding_left + 110, y=465)

    # Dealer info
    dealer_info = tkinter.Label(
        game_frame, text="", font="helvetica 11 bold", borderwidth=0, background=BC, fg="white"
    )
    dealer_info.place(x=305, y=180)

    # Dealer finger
    finger = {str(slot): tkinter.Label(game_frame, borderwidth=0, background=BC) for slot in range(4)}
    for ind, f in enumerate(finger.values()):
        f.place(x=ind * x_slot + padding_left - 5, y=250)

    # Player cards
    slot_player = {
        f"{str(slot)}{str(pos)}": tkinter.Label(game_frame, borderwidth=0, background=BC)
        for slot in range(4)
        for pos in range(N_CARDS_MAX)
    }
    for frame in range(4):
        for pos in range(N_CARDS_MAX):
            slot_player[f"{str(frame)}{str(pos)}"].place(
                x=frame * x_slot + pos * 30 + padding_left, y=350 - pos * 30
            )

    # Dealer cards
    n_dealer_cards = 7
    card_back_img, _, _ = get_image()
    slot_dealer = {
        f"{str(pos)}": tkinter.Label(game_frame, borderwidth=0, background=BC)
        for pos in range(n_dealer_cards)
    }
    for pos in range(2):
        slot_dealer[str(pos)].configure(image=card_back_img)
        slot_dealer[str(pos)].image = card_back_img  # type: ignore
        slot_dealer[str(pos)].pack(side=tkinter.LEFT)
    for pos, slot in enumerate(slot_dealer.values()):
        slot.place(y=40, x=300 + pos * 105)

    # Chips
    chips = {
        f"{str(slot)}{str(pos)}": tkinter.Label(game_frame, borderwidth=0, background=BC)
        for slot in range(4)
        for pos in range(5)
    }


    for a_slot in range(4):
        for pos in range(5):
            padx, pady = 0, 0
            if pos == 1:
                padx = 50
            elif pos == 2:
                padx = -50
            elif pos == 3:
                padx = 100
            elif pos == 4:
                padx = 25
                pady = 35
            chips[f"{str(a_slot)}{str(pos)}"].place(
                x=a_slot * x_slot + padding_left + padx + 20, y=500 + pady
            )

    # Insurance chip
    insurance_chip = tkinter.Label(game_frame, borderwidth=0, background=BC)
    insurance_chip.place(x=450, y=400)

    # Side panel
    panel = tkinter.Label(
    game_frame, width=200, height=720, background=BC, borderwidth=0, padx=20
    )
    panel.place(x=1000, y=0)

    # Advisor button
    fix_mistakes = tkinter.IntVar()
    checkbox_container = tkinter.Checkbutton(
        game_frame, text="Coach mode", variable=fix_mistakes,fg="black", background="lightgrey",
        command=lambda: help_button.config(state=tkinter.NORMAL if fix_mistakes.get() else tkinter.DISABLED)
    )
    checkbox_container.place(x=1050, y=580)

    # Help button
    help_button = tkinter.Button(
    game_frame,
    text="Get Help",
    width=12,
    font=("Helvetica", 14),
    bg="white",
    fg="black",
    activebackground="#0072c6",
    activeforeground="white",
    bd=0,
    highlightthickness=0,
    padx=10,
    pady=5,
    command=lambda: show_help(game_frame),
    state=tkinter.DISABLED
)
    help_button.place(x=1025, y=650)

    dealer_card_values = tkinter.StringVar(game_frame)
    dealer_card_values_label = tkinter.Label(
        game_frame,
        textvariable=dealer_card_values,
        font="Helvetica 13 bold",
        borderwidth=0,
        background=BC,
        fg="white",
    )
    dealer_card_values_label.place(x=250, y=20)

    # Add the following lines to create the player's card values label
    player_card_values = tkinter.StringVar(game_frame)
    player_card_values_label = tkinter.Label(
        game_frame,
        textvariable=player_card_values,
        font="Helvetica 13 bold",
        borderwidth=0,
        background=BC,
        fg="white",
    )
    player_card_values_label.place(x=250, y=600)


    # Buttons
    menu = {
            name.split()[0].lower(): tkinter.Button(
            master=game_frame,
            text=name.replace("-", " "),
            width=12,
            font=("Helvetica", 14),
            bg="white",
            fg="black",
            activebackground="#0072c6",
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=5,
        )
        for name in (
            "Even-money",
            "Insurance",
            "Surrender",
            "Double up",
            "Hit",
            "Stay",
            "Split",
            "Deal",
            "Reset",
        )
    }
    for name, button in menu.items():
        if name == "hit":
            button.configure(command=lambda: game.hit())
        elif name == "split":
            button.configure(command=lambda: game.split())
        elif name == "surrender":
            button.configure(command=lambda: game.surrender())
        elif name == "stay":
            button.configure(command=lambda: game.stay())
        elif name == "double":
            button.configure(command=lambda: game.double())
        elif name == "deal":
            button.configure(command=lambda: game.next())
        elif name == "reset":
            button.configure(command=lambda: game.reset())
        elif name == "insurance":
            button.configure(command=lambda: game.insurance())
        elif name == "even-money":
            button.configure(command=lambda: game.even_money())
        else:
            raise ValueError

    x_sidepanel = 1025
    for ind, button in enumerate(menu.values()):
        button.place(x=x_sidepanel, y=ind * 33 + 230)

    menu["deal"].place(x=x_sidepanel, y=500)
    menu["reset"].place(x=x_sidepanel, y=20)

    #Rebet Button
    rebet_button = tkinter.Button(
    game_frame,
    text="Rebet",
    width=12,
    font=("Helvetica", 14),
    bg=BC,
    fg="black",
    activebackground=BC,
    activeforeground="white",
    bd=0,
    highlightthickness=0,
    padx=4,
    pady=2,
    command=lambda: rebet(game),
    state=tkinter.DISABLED
    )
    rebet_button.place(x = 650, y = 525)


    # Add chips
    chipList = []
    redChip = Image.open(f"{IMG_PATH}/red.png").resize((50, 50 ), Image.ANTIALIAS)
    redChipPhoto = ImageTk.PhotoImage(redChip)

    blueChip = Image.open(f"{IMG_PATH}/blue.png").resize((50, 50 ), Image.ANTIALIAS)
    blueChipPhoto = ImageTk.PhotoImage(blueChip)

    greenChip = Image.open(f"{IMG_PATH}/green.png").resize((50, 50), Image.ANTIALIAS)
    greenChipPhoto = ImageTk.PhotoImage(greenChip)

    blackChip = Image.open(f"{IMG_PATH}/black.png").resize((50, 50), Image.ANTIALIAS)
    blackChipPhoto = ImageTk.PhotoImage(blackChip)

    button1 = tkinter.Button(game_frame, image=redChipPhoto, bd = 0, command = lambda: game.increment_bet("red"), bg=BC)
    button1.place(x=500, y = 600)

    button2 = tkinter.Button(game_frame, image=blueChipPhoto, bd = 0, command = lambda: game.increment_bet("blue"), bg=BC)
    button2.place(x=555, y = 600)

    button3 = tkinter.Button(game_frame, image=greenChipPhoto, bd = 0, command = lambda: game.increment_bet("green"), bg=BC)
    button3.place(x=610, y = 600)

    button4 = tkinter.Button(game_frame, image=blackChipPhoto, bd = 0, command = lambda: game.increment_bet("black"), bg=BC)
    button4.place(x=665, y = 600)

    chipList = [button1, button2, button3, button4]

    def back():
        game_frame.pack_forget()
        credits_frame.pack_forget()
        main_menu_frame.pack(fill="both")
        game.reset()


    back_button = tkinter.Button(
    game_frame,
    text="Back",
    width=12,
    font=("Helvetica", 14),
    bg="white",
    fg="black",
    activebackground="#0072c6",
    activeforeground="white",
    bd=0,
    highlightthickness=0,
    padx=10,
    pady=5,
    command=back,
    state=tkinter.NORMAL
)

    back_button.place(x=5, y=5)

    def start_game():
        main_menu_frame.pack_forget()
        game_frame.pack(fill="both")
        fix_mistakes.set(0)

    menu_label = tkinter.Label(main_menu_frame,
                                  text="BLACKJACK",
                                  font=("Times", 36, "bold italic"),
                                  bg=BC)
    menu_label.place(relx=0.5, y=225, anchor="center")

    play_game_button = tkinter.Button(main_menu_frame,
                                      text="Start Game",
                                      width=12,
                                      font=("Helvetica", 14),
                                      bg="white",
                                      fg="black",
                                      activebackground="#0072c6",
                                      activeforeground="white",
                                      bd=0,
                                      highlightthickness=0,
                                      padx=10,
                                      pady=5,
                                      command=start_game
                                      )
    play_game_button.place(relx=0.5, y=300, anchor="center")

    def start_tutorial():
        main_menu_frame.pack_forget()
        game_frame.pack(fill="both")
        fix_mistakes.set(1)

    tutorial_button = tkinter.Button(main_menu_frame,
                                     text="Tutorial",
                                     width=12,
                                     font=("Helvetica", 14),
                                     bg="white",
                                     fg="black",
                                     activebackground="#0072c6",
                                     activeforeground="white",
                                     bd=0,
                                     highlightthickness=0,
                                     padx=10,
                                     pady=5,
                                     command=start_tutorial
                                     )
    tutorial_button.place(relx=0.5, y=350, anchor="center")

    def show_credits():
        main_menu_frame.pack_forget()
        credits_frame.pack(fill="both")

    credits_button = tkinter.Button(main_menu_frame,
                                    text="Credits",
                                    width=12,
                                    font=("Helvetica", 14),
                                    bg="white",
                                    fg="black",
                                    activebackground="#0072c6",
                                    activeforeground="white",
                                    bd=0,
                                    highlightthickness=0,
                                    padx=10,
                                    pady=5,
                                    command=show_credits
                                    )
    credits_button.place(relx=0.5, y=400, anchor="center")

    credits_label = tkinter.Label(credits_frame,
                                  text="Developers:\nReese Collins\nDaniel McGarr\nNavjeeven Mann\nSundin\nAndrew Domfe",
                                  font=("Helvetica", 18),
                                  bg=BC)
    credits_label.place(relx=0.5, rely=0.5, anchor="center")

    gui = Gui(
        game_frame,
        menu,
        label_text,
        slot_player,
        slot_dealer,
        info_text,
        info,
        chips,
        finger,
        shoe_progress,
        fix_mistakes,
        insurance_chip,
        dealer_info,
        rebet_button,
        dealer_card_values,  # Add dealer_card_values as an attribute
        player_card_values, # Add player_card_values as an attribute
        chipList
    )

    dealer = Dealer()
    player = Player(stack=args.stack)
    game = Game(player, dealer, gui, args)
    game.reset()
    tkinter.mainloop()
