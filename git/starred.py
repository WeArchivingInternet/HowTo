#!/usr/bin/env python3
# MIT License
# 
# Copyright (c) 2022 Umar Getagazov
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.parse
import urllib.error
import time


def file(path=None, mode=None, fallback=None):
    if path is None or path == "-":
        return fallback
    else:
        return open(path, mode=mode)


def request(url, params=None):
    if params is not None:
        params = urllib.parse.urlencode(params)
        url += f"?{params}"
    url = f"https://api.github.com/{url}"
    r = urllib.request.Request(url)
    if "GITHUB_TOKEN" in os.environ:
        r.add_header("Authorization", f"token {os.environ['GITHUB_TOKEN']}")
    while True:
        try:
            return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            if int(e.headers.get("x-ratelimit-remaining")) == 0:
                wait_for = int(e.headers.get("x-ratelimit-reset")) - time.time()
                if wait_for > 0:
                    print(f"Waiting {int(wait_for)} sec...", file=sys.stderr)
                    time.sleep(wait_for)
                    continue
            else:
                raise e


def common(url, output):
    repos = []
    page = 1
    while True:
        resp = request(url, {"per_page": 100, "page": page})
        repos += resp
        page += 1
        if len(resp) == 0:
            break
    with file(output, "w", sys.stdout) as f:
        json.dump(repos, f)
        f.write("\n")
    print(f"Export finished. Total count: {len(repos)}", file=sys.stderr)


def stars_command(args):
    common(f"users/{args.user}/starred", args.output)


def user_command(args):
    common(f"users/{args.user}/repos", args.output)


def org_command(args):
    common(f"orgs/{args.organization}/repos", args.output)


def clone_command(args):
    skipped = 0
    cloned = 0
    with file(args.input, "r", sys.stdin) as f:
        repos = json.load(f)
        for repo in repos:
            full_name = repo["full_name"]
            clone_url = repo["clone_url"]
            if not os.path.exists(full_name):
                os.makedirs(full_name, exist_ok=True)
                env = {"GIT_TERMINAL_PROMPT": "0"}
                subprocess.run(["git", "clone", "--recursive", clone_url, full_name], env=env)
                cloned += 1
            else:
                skipped += 1
    print(f"Clone finished. {cloned} cloned, {skipped} skipped", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    parser_stars = subparsers.add_parser('stars', help='export user\'s stars')
    parser_stars.add_argument('user', help='GitHub username')
    parser_stars.add_argument('output', help='output path (- for stdout)')
    parser_stars.set_defaults(func=stars_command)

    parser_user = subparsers.add_parser('user', help='export user\'s repositories')
    parser_user.add_argument('user', help='GitHub username')
    parser_user.add_argument('output', help='output path (- for stdout)')
    parser_user.set_defaults(func=user_command)

    parser_org = subparsers.add_parser('org', help='export organization\'s repositories')
    parser_org.add_argument('organization', help='GitHub organization name')
    parser_org.add_argument('output', help='output path (- for stdout)')
    parser_org.set_defaults(func=org_command)

    parser_clone = subparsers.add_parser('clone', help='clone repositories from the export')
    parser_clone.add_argument('input', help='path to the export JSON file (- for stdin)')
    parser_clone.set_defaults(func=clone_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
