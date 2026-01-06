#!/usr/bin/env python3
import os
import sys
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_total_size(api_url, headers):
    total = 0
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code != 200: return 0
        items = response.json()
        for item in items:
            if item["type"] == "file":
                total += item.get("size", 0)
            elif item["type"] == "dir":
                total += get_total_size(item["url"], headers)
    except: pass
    return total

def download_recursive(api_url, output_dir, headers, progress, task_id):
    response = requests.get(api_url, headers=headers, timeout=15)
    if response.status_code != 200:
        return False, f"API Error: {response.status_code}"

    items = response.json()
    os.makedirs(output_dir, exist_ok=True)

    for item in items:
        if item["type"] == "file":
            progress.update(task_id, description=f"FETCHING {item['name'][:30]}")
            r = requests.get(item["download_url"], headers=headers, stream=True)
            with open(os.path.join(output_dir, item["name"]), "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
        elif item["type"] == "dir":
            success, msg = download_recursive(item["url"], os.path.join(output_dir, item["name"]), headers, progress, task_id)
            if not success: return False, msg
    return True, "SUCCESS"

def main():
    console.clear()
    
    # UI SUBGIT
    header = Text("SUBGIT : REPOSITORY SUBSET EXTRACTOR", style="bold white")
    console.print(Panel(header, border_style="white", expand=False))

    auth_text = "AUTHENTICATED" if GITHUB_TOKEN else "ANONYMOUS"
    auth_style = "green" if GITHUB_TOKEN else "yellow"
    console.print(f"SESSION: [{auth_style}]{auth_text}[/] \n")

    repo_url = Prompt.ask("[bold white]INPUT URL[/]").strip()
    
    if "github.com" not in repo_url:
        console.print("\n[bold red]ERROR:[/] Invalid GitHub reference"); sys.exit(1)

    try:
        parts = repo_url.strip("/").split("/")
        user, repo = parts[3], parts[4]
        if "tree" in parts:
            idx = parts.index("tree")
            branch, folder_path = parts[idx + 1], "/".join(parts[idx + 2:])
        else: branch, folder_path = "main", ""
        
        target_dir = parts[-1] if folder_path else repo
        headers = {"Accept": "application/vnd.github.v3+json"}
        if GITHUB_TOKEN: headers["Authorization"] = f"token {GITHUB_TOKEN}"

        with console.status("[bold white]SCANNING STRUCTURE...[/]"):
            total_bytes = get_total_size(api_url := f"https://api.github.com/repos/{user}/{repo}/contents/{folder_path}?ref={branch}", headers)

        if total_bytes == 0 and not GITHUB_TOKEN:
             console.print("\n[bold red]ERROR:[/] Path not found or repository is private.")
             return

        with Progress(
            SpinnerColumn(spinner_name="line", style="white"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(bar_width=40, style="grey37", complete_style="white"),
            DownloadColumn(),
            TimeRemainingColumn(),
            console=console,
            transient=True
        ) as progress:
            
            task_id = progress.add_task(description="DOWNLOAD", total=total_bytes)
            success, message = download_recursive(api_url, target_dir, headers, progress, task_id)

        if success:
            summary = Table.grid(padding=(0, 2))
            summary.add_row("[white]STATUS[/]", "COMPLETED")
            summary.add_row("[white]OBJECT[/]", target_dir)
            summary.add_row("[white]SIZE[/]", f"{total_bytes / 1024:.1f} KB")
            summary.add_row("[white]PATH[/]", os.path.abspath(target_dir))
            
            console.print(Panel(summary, title="[bold white]SUMMARY[/]", border_style="white", expand=False))
        else:
            console.print(f"\n[bold red]CRITICAL ERROR:[/] {message}")

    except Exception as e:
        console.print(f"\n[bold red]CRITICAL ERROR:[/] {e}")

if __name__ == "__main__":
    main()