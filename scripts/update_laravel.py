import subprocess, urllib.request
def value(*command):
    return subprocess.run(command, check=True, text=True, capture_output=True).stdout.strip()
def show(*command):
    subprocess.run(command, check=True)
try:
    if value("git", "branch", "--show-current") != "ylff--php": raise RuntimeError("nav zars ylff--php")
    if value("git", "remote", "get-url", "origin") != "https://github.com/yl3gbc/ylff-latvija.git": raise RuntimeError("nepareizs origin")
    if value("git", "status", "--porcelain"): raise RuntimeError("Git darba koks nav tīrs")
    show("git", "fetch", "origin", "ylff--php")
    show("docker", "compose", "exec", "-T", "app", "composer", "update", "laravel/framework", "--with-dependencies", "--prefer-source", "--no-interaction", "--no-progress")
    if value("git", "status", "--porcelain", "--", "composer.lock"):
        show("git", "add", "composer.lock")
        show("git", "commit", "-m", "Update Laravel Framework 13.x development dependencies")
    show("git", "fetch", "https://github.com/laravel/laravel.git", "13.x")
    if value("git", "rev-list", "--count", "HEAD..FETCH_HEAD") != "0":
        show("git", "merge", "--no-edit", "FETCH_HEAD")
    urllib.request.urlopen("http://127.0.0.1:8080/", timeout=20).read(1)
    if value("git", "rev-list", "--count", "origin/ylff--php..HEAD") != "0":
        show("git", "push", "origin", "ylff--php")
    print("OK: Laravel 13.x un Framework 13.x ir atjaunināti")
except Exception as error:
    subprocess.run(("git", "merge", "--abort"), capture_output=True); subprocess.run(("git", "restore", "--staged", "--worktree", "composer.lock"), capture_output=True); raise SystemExit(f"KĻŪDA: {error}")
