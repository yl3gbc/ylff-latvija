#!/bin/bash

# YLFF projekta automātiskais Git upload skripts

cd /webprojekti/awards || exit 1

echo "=== Git statuss ==="
git status

echo "=== Pievienojam visas izmaiņas ==="
git add .

echo "=== Pārbaudām vai ir ko commitot ==="
if git diff --cached --quiet; then
    echo "Nav jaunu izmaiņu. Nekas nav jāaugšupielādē."
    exit 0
fi

echo "=== Veidojam commit ==="
git commit -m "Update YLFF project"

echo "=== Augšupielādējam uz Gitea ==="
git push

echo "=== Gatavs ==="
