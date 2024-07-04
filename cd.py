#!/usr/bin/env python3
import subprocess
from time import sleep

BASE_COMMAND = "docker compose -f $(pwd)/docker-compose.production.yml"


def run_command(command):
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    return result.stdout, result.stderr


def check_for_git_changes():
    pull_output, _ = run_command("git pull")
    print(pull_output)
    if "Already up to date." not in pull_output:
        print("New changes detected. Deploying...")
        out, error = run_command(f"{BASE_COMMAND} stop")
        print(out, error)
        out, error = run_command(f"{BASE_COMMAND} up -d")
        print(out, error)
        print("Deployed successfully.")
    else:
        print("No new changes detected.")


if __name__ == "__main__":
    while True:
        check_for_git_changes()
        sleep(30)
