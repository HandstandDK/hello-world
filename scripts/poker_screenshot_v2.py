#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import re
import subprocess
from pathlib import Path

from PIL import Image
import pytesseract


def run_osascript(script: str) -> str:
    result = subprocess.run(["osascript", "-e", script], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def front_window_id() -> str:
    script = (
        'tell application "System Events"\n'
        '  set frontApp to first application process whose frontmost is true\n'
        '  tell frontApp\n'
        '    if (count of windows) is 0 then return ""\n'
        '    return id of front window\n'
        '  end tell\n'
        'end tell'
    )
    return run_osascript(script)


def screencapture_window(window_id: str, output_path: Path) -> None:
    subprocess.run(["screencapture", "-l", window_id, "-x", str(output_path)], check=True)


def crop_box_from_percent(img: Image.Image, box_pct: tuple[float, float, float, float]) -> Image.Image:
    width, height = img.size
    left = int(width * box_pct[0])
    upper = int(height * box_pct[1])
    right = int(width * box_pct[2])
    lower = int(height * box_pct[3])
    return img.crop((left, upper, right, lower))


def extract_player_name(text: str) -> str:
    candidates = re.findall(r"[A-Za-z0-9_]{3,}", text)
    if not candidates:
        return ""
    candidates.sort(key=len, reverse=True)
    return candidates[0]


def ocr_text(img: Image.Image) -> str:
    return pytesseract.image_to_string(img, config="--psm 7 --oem 1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tag screenshot af aktivt vindue og navngiv via OCR.")
    parser.add_argument("--debug-crops", action="store_true", help="Gem crop-billeder til fejlfinding")
    args = parser.parse_args()

    output_dir = Path.home() / "Desktop" / "poker_screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    window_id = front_window_id()
    if not window_id:
        raise SystemExit("Kunne ikke finde det aktive vindue.")

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = output_dir / f"_temp_{timestamp}.png"
    screencapture_window(window_id, temp_path)

    img = Image.open(temp_path)

    # Juster disse områder hvis navnet ikke genkendes korrekt.
    # Format: (left_pct, upper_pct, right_pct, lower_pct)
    player_list_box = (0.71, 0.25, 0.97, 0.90)
    legend_box = (0.38, 0.90, 0.78, 0.98)

    crops = [
        ("player_list", crop_box_from_percent(img, player_list_box)),
        ("legend", crop_box_from_percent(img, legend_box)),
    ]

    detected_name = ""
    for label, crop in crops:
        text = ocr_text(crop)
        candidate = extract_player_name(text)
        if args.debug_crops:
            crop.save(output_dir / f"debug_{label}_{timestamp}.png")
        if candidate:
            detected_name = candidate
            break

    if not detected_name:
        raise SystemExit("Kunne ikke finde et navn via OCR. Juster crop-områderne i scriptet.")

    safe_name = re.sub(r"[^A-Za-z0-9_-]", "", detected_name)
    output_path = output_dir / f"{safe_name}_{timestamp}.png"
    os.replace(temp_path, output_path)
    print(f"Gemte: {output_path}")


if __name__ == "__main__":
    main()
