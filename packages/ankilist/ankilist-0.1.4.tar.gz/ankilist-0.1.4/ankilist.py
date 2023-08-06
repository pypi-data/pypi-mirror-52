import argparse
import configparser
import os
import sys

import requests

config_dir = os.environ["HOME"] + "/.config/ankilist"
config_path = config_dir + "/config"


def get_translate(source_text, **kwargs):
    response = requests.get(f"https://translate.googleapis.com/"
                            f"translate_a/single?client=gtx&sl="
                            f"{kwargs['source_lang']}&tl={kwargs['target_lang']}&dt=t&q={source_text}").json()
    if "error" in str(response):
        raise Exception("Error translate")
    else:
        return response[0][0][0]


def argspars():
    parser = argparse.ArgumentParser(description="Easy generator list for learning language. For Anki")
    parser.add_argument("-t", "--text", help="Text, to add in list or translite", default="")
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    parser.add_argument("--set_lang", "-sl", type=str, default="ru", help="Set custom target language (default: ru)")
    parser.add_argument("--set_default_lang", "-sdl", default=None, help="Set default target language")
    parser.add_argument("--restore_default_lang", "-rdl", help="Restore default target language",
                        action="store_true")
    parser.add_argument("--just_translate", "-jt", help="If true, just translate text", action="store_true")
    parser.add_argument("--just_translate_default", "-jtd", help="Off/on just translate default", action="store_true")
    return parser.parse_args()


def read_config():
    if not os.path.exists(config_dir):
        os.mkdir(config_dir, 0o755)
    if not os.path.exists(config_path):
        create_config()
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def create_config():
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "default_lang", "ru")
    config.set("Settings", "just_translate_default", "False")
    config.set("Settings", "output_path", "None")
    with open(config_path, "w") as config_file:
        config.write(config_file)


def config_set(config, section, setting, value):
    config.set(section, setting, value)
    with open(config_path, "w") as config_file:
        config.write(config_file)


def main():
    args = argspars()
    config = read_config()
    if args.show_version:
        print("Ankilist\nVersion:0.1.4")
    if args.set_default_lang is not None:
        config_set(config, "Settings", "default_lang", args.set_default_lang)
    if args.restore_default_lang:
        config_set(config, "Settings", "default_lang", "ru")
    if args.just_translate_default:
        if config.getboolean("Settings", "just_translate_default"):
            config_set(config, "Settings", "just_translate_default", "False")
        else:
            config_set(config, "Settings", "just_translate_default", "True")
    if args.text == "":
        exit()
    if args.set_lang is not None:
        res = get_translate(args.text, target_lang=args.set_lang, source_lang="auto")
    else:
        res = get_translate(args.text, target_lang=config.get("Settings", "default_lang"), source_lang="auto")
    print(res)
    if args.just_translate:
        exit()
    if config.getboolean("Settings", "just_translate_default"):
        exit()
    res = f'"{args.text}";"{res}"\n'
    if config.get("Settings", "output_path") == "None":
        output_path = str(input("Enter default anki output path: "))
        if "~/" in output_path:
            output_path = output_path.replace("~", os.environ["HOME"])
        if os.path.exists(output_path):
            with open(output_path, "a") as file:
                file.write(res)
        else:
            with open(output_path, "x") as file:
                file.write(res)
        config_set(config, "Settings", "output_path", output_path)
    with open(config.get("Settings", "output_path"), "a") as file:
        file.write(res)


if __name__ == "__main__":
    main()
