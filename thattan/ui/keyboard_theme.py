from __future__ import annotations

from PySide6.QtWidgets import QApplication

_FINGER_NAMES_TAMIL = {
    'thumb': 'கட்டைவிரல்',
    'index': 'சுட்டுவிரல்',
    'middle': 'நடுவிரல்',
    'ring': 'மோதிரவிரல்',
    'pinky': 'சிறுவிரல்',
}

_HAND_NAMES_TAMIL = {
    'left': 'இடது',
    'right': 'வலது',
}


def _build_finger_mapping() -> dict[str, tuple[str, str]]:
    """Build mapping from key to (hand, finger) tuple.

    Returns:
        dict mapping key name to (hand, finger) where:
        - hand: 'left' or 'right'
        - finger: 'thumb', 'index', 'middle', 'ring', 'pinky'
    """
    mapping: dict[str, tuple[str, str]] = {}
    for key in ['`', '1', 'Q', 'A', 'Z', 'TAB', 'CAPS']:
        mapping[key.upper()] = ('left', 'pinky')
    mapping['SHIFT'] = ('left', 'pinky')  # Left shift (default, can be overridden)

    for key in ['2', 'W', 'S', 'X']:
        mapping[key.upper()] = ('left', 'ring')

    for key in ['3', 'E', 'D', 'C']:
        mapping[key.upper()] = ('left', 'middle')

    for key in ['4', '5', 'R', 'T', 'F', 'G', 'V', 'B']:
        mapping[key.upper()] = ('left', 'index')

    mapping['SPACE'] = ('left', 'thumb')
    mapping[' '] = ('left', 'thumb')  # Space as character

    for key in ['6', '7', 'Y', 'U', 'H', 'J', 'N', 'M']:
        mapping[key.upper()] = ('right', 'index')

    for key in ['8', 'I', 'K', ',']:
        mapping[key.upper()] = ('right', 'middle')

    for key in ['9', 'O', 'L', '.']:
        mapping[key.upper()] = ('right', 'ring')

    for key in ['0', '-', '=', 'P', '[', ']', '\\', ';', "'", '/', 'ENTER', 'BACKSPACE']:
        mapping[key.upper()] = ('right', 'pinky')

    # Special keys - Right shift (typically used more often)
    mapping['SHIFT'] = ('right', 'pinky')

    mapping['CTRL'] = ('left', 'pinky')  # Left Ctrl
    mapping['ALT'] = ('left', 'thumb')  # Left Alt

    return mapping


class KeyboardTheme:
    """Colors, finger-guidance, and key-style helpers for the on-screen Tamil99 keyboard.

    Self-contained: holds only the static key-to-finger mapping, no window/widget state.
    """

    def __init__(self) -> None:
        self.key_to_finger: dict[str, tuple[str, str]] = _build_finger_mapping()

    def get_finger_name(self, key_label: str, needs_shift: bool = False) -> tuple[str, str]:
        """Get finger name for a key in both English and Tamil.

        Args:
            key_label: The key label (e.g., 'A', 'Space', 'Shift')
            needs_shift: Whether Shift is required

        Returns:
            tuple of (english_name, tamil_name)
        """
        if key_label.upper() == 'SHIFT':
            # If it's the Shift key itself, default to right shift (pinky)
            hand, finger = self.key_to_finger.get('SHIFT', ('right', 'pinky'))
        elif needs_shift:
            # Shift rule:
            # - If the actual key is typed with LEFT hand -> use RIGHT shift
            # - If the actual key is typed with RIGHT hand -> use LEFT shift
            key_hand, _key_finger = self.key_to_finger.get(key_label.upper(), ('right', 'index'))
            shift_hand = 'right' if key_hand == 'left' else 'left'
            hand, finger = (shift_hand, 'pinky')
        else:
            hand, finger = self.key_to_finger.get(key_label.upper(), ('right', 'index'))

        english_name = f"{hand.capitalize()} {finger.capitalize()}"
        tamil_name = f"{_HAND_NAMES_TAMIL.get(hand, hand)} {_FINGER_NAMES_TAMIL.get(finger, finger)}"
        return (english_name, tamil_name)

    def shift_side_for_key(self, key_label: str) -> str:
        """Return which Shift side to use for a given key label ('left' or 'right')."""
        key_hand, _ = self.key_to_finger.get(key_label.upper(), ('right', 'index'))
        return 'right' if key_hand == 'left' else 'left'

    def get_theme_colors(self) -> dict:
        """Get light theme color palette"""
        return {
            # Background: neutral light grey with soft teal tint
            'bg_main': '#EEF6F6',
            'bg_container': 'rgba(255, 255, 255, 0.34)',
            'bg_card': 'rgba(255, 255, 255, 0.24)',
            'bg_input': 'rgba(255, 255, 255, 0.38)',
            'bg_hover': 'rgba(255, 255, 255, 0.46)',

            # Typing text: dark neutral
            'text_primary': '#1F2933',
            'text_secondary': '#334155',
            'text_muted': '#64748B',

            'border': 'rgba(15, 23, 42, 0.14)',
            'border_light': 'rgba(15, 23, 42, 0.10)',

            # Active character: accent (teal)
            'highlight': '#0F766E',
            'highlight_bg': 'rgba(15, 118, 110, 0.18)',

            'error': '#D64545',
            'error_bg': 'rgba(214, 69, 69, 0.18)',
            'success': '#2F855A',
            'success_bg': 'rgba(47, 133, 90, 0.18)',
            'progress': '#0F766E',

            # Kept for compatibility with older styles
            'key_bg': 'rgba(255, 255, 255, 0.22)',
            'key_highlight': '#0F766E',
            'key_highlight_bg': 'rgba(15, 118, 110, 0.18)',
            'key_shift': '#0F766E',
            'key_shift_bg': 'rgba(15, 118, 110, 0.18)',
        }

    def get_finger_colors(self) -> dict[tuple[str, str], str]:
        """Finger color palette (hand, finger) -> hex color."""
        return {
            ('left', 'pinky'): '#5C96EB',
            ('left', 'ring'): '#EF6060',
            ('left', 'middle'): '#2ECC71',
            ('left', 'index'): '#7A5CEB',
            ('left', 'thumb'): '#EB78D2',
            ('right', 'pinky'): '#5C96EB',
            ('right', 'ring'): '#EF6060',
            ('right', 'middle'): '#2ECC71',
            ('right', 'index'): '#FF953D',
            ('right', 'thumb'): '#EB78D2',
        }

    def darken_hex_color(self, hex_color: str, factor: float) -> str:
        """Darken a hex color by multiplying RGB by factor (0..1)."""
        try:
            c = hex_color.strip()
            if not c.startswith("#"):
                return hex_color
            if len(c) != 7:
                return hex_color
            factor = max(0.0, min(1.0, factor))
            r = int(c[1:3], 16)
            g = int(c[3:5], 16)
            b = int(c[5:7], 16)
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            return hex_color

    def blend_hex_colors(self, a: str, b: str, t: float) -> str:
        """Blend two #RRGGBB colors. t=0 -> a, t=1 -> b."""
        try:
            a = a.strip()
            b = b.strip()
            if not (a.startswith("#") and b.startswith("#") and len(a) == 7 and len(b) == 7):
                return a
            t = max(0.0, min(1.0, float(t)))
            ar, ag, ab = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
            br, bg, bb = int(b[1:3], 16), int(b[3:5], 16), int(b[5:7], 16)
            r = int(ar + (br - ar) * t)
            g = int(ag + (bg - ag) * t)
            bl = int(ab + (bb - ab) * t)
            return f"#{r:02X}{g:02X}{bl:02X}"
        except Exception:
            return a

    def finger_color_for_key(self, key_label: str) -> str:
        """Return background color for a given key label."""
        hand, finger = self.key_to_finger.get(key_label.upper(), ('right', 'index'))
        return self.get_finger_colors().get((hand, finger), '#5C96EB')

    def muted_key_fill_color_for_key(self, key_label: str) -> str:
        """Muted/pastel version of the finger color for this key."""
        colors = self.get_theme_colors()
        base = self.finger_color_for_key(key_label)
        # Blend towards window background to mute the color
        return self.blend_hex_colors(base, colors['bg_main'], 0.62)

    def highlight_border_color_for_key(self, key_label: str) -> str:
        """Border color for highlight that matches the finger palette (darker shade)."""
        base = self.finger_color_for_key(key_label)
        return self.darken_hex_color(base, 0.45)

    def build_key_style(
        self,
        key_label: str,
        font_px: int,
        *,
        border_px: int = 4,
        border_color: str = "transparent",
        font_weight: int = 500,
    ) -> str:
        colors = self.get_theme_colors()
        bg = self.muted_key_fill_color_for_key(key_label)
        border = f"{border_px}px solid {border_color}" if border_px > 0 else "none"
        return f"""
            QLabel {{
                background: {bg};
                color: {colors['text_primary']};
                border: {border};
                border-radius: 6px;
                padding: 12px 8px;
                font-family: '{QApplication.font().family()}', sans-serif;
                font-size: {font_px}px;
                font-weight: {font_weight};
            }}
        """
