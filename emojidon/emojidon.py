#!/usr/bin/env python


from functools import partial
from os import getenv
from pathlib import Path
from time import sleep

from dotenv import load_dotenv
import httpx
from rich import print
from selenium import webdriver
from selenium.webdriver.common.by import By
from slugify import slugify as og_slugify
import typer


load_dotenv()


SUPPORTED_SUFFIXES = set([".gif", ".png"])

MASTODON_ACCESS_TOKEN = getenv("MASTODON_ACCESS_TOKEN")
MASTODON_API_BASE_URL = getenv("MASTODON_API_BASE_URL")

MASTODON_LOGIN_URL = getenv("MASTODON_LOGIN_URL")
MASTODON_EMOJI_URL = getenv("MASTODON_EMOJI_URL")
MASTODON_EMAIL = getenv("MASTODON_EMAIL")
MASTODON_PASSWORD = getenv("MASTODON_PASSWORD")

EMOJI_DIR = Path(getenv("EMOJI_DIR"))


slugify = partial(og_slugify, separator="_")


def call_api(
    method: str,
    path: str = None,
    token: str = MASTODON_ACCESS_TOKEN,
) -> dict:
    url = f"{MASTODON_API_BASE_URL}/{path}"
    request = httpx.Request(
        method,
        url,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    response = httpx.Client().send(request)
    return response.json()


def list_server_emojis() -> list[str]:
    print("Listing server emojis")

    emojis = call_api(
        method="GET",
        path="custom_emojis",
    )

    print(f"Found {len(emojis)} emojis on server")

    shortcodes = [emoji["shortcode"] for emoji in emojis]
    return shortcodes


def list_local_emojis() -> list[Path]:
    print("Listing local emojis")

    all_files = list(EMOJI_DIR.iterdir())
    valid_emojis = sorted(
        [file_ for file_ in all_files if file_.suffix.lower() in SUPPORTED_SUFFIXES]
    )

    print(f"Found {len(valid_emojis)} locally")

    return valid_emojis


def import_emojis(paths: list[Path]) -> None:
    print("Importing missing emojis")

    # open browser
    options = webdriver.chrome.options.ChromiumOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # log in
    driver.get(MASTODON_LOGIN_URL)

    email_field = driver.find_element(By.ID, "user_email")
    email_field.send_keys(MASTODON_EMAIL)

    password_field = driver.find_element(By.ID, "user_password")
    password_field.send_keys(MASTODON_PASSWORD)

    submit_button = driver.find_element(By.ID, "new_user").find_element(
        By.TAG_NAME,
        "button",
    )
    submit_button.click()

    # upload emojis
    for path in paths:
        shortcode = slugify(path.stem)

        print(f"Importing {shortcode}")

        driver.get(MASTODON_EMOJI_URL)

        shortcode_field = driver.find_element(By.ID, "custom_emoji_shortcode")
        shortcode_field.send_keys(shortcode)

        image_field = driver.find_element(By.ID, "custom_emoji_image")
        image_field.send_keys(str(path))

        upload_button = driver.find_element(By.ID, "new_custom_emoji").find_element(
            By.TAG_NAME,
            "button",
        )
        upload_button.click()

    # close browser
    driver.quit()


def delete_emoji():
    ...  # TODO


def main():
    print("Here we go")

    server_emojis = list_server_emojis()

    local_emojis = list_local_emojis()

    missing_emojis = [
        local_emoji
        for local_emoji in local_emojis
        if slugify(local_emoji.stem) not in server_emojis
    ]

    import_emojis(missing_emojis)

    print("Dunzo")


if __name__ == "__main__":
    typer.run(main)
