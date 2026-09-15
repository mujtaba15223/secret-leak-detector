from pathlib import Path
import shutil


def install_hook() -> None:
    """
    Install the Secret Leak Detector pre-commit hook.
    """

    project_root = Path(__file__).resolve().parent.parent

    git_hooks_dir = project_root / ".git" / "hooks"
    source_hook = project_root / "githook" / "pre_commit"
    target_hook = git_hooks_dir / "pre-commit"

    if not (project_root / ".git").exists():
        print("❌ Git repository not found.")
        return

    if not source_hook.exists():
        print("❌ pre_commit hook file not found.")
        return

    git_hooks_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        source_hook,
        target_hook,
    )

    print("✅ Secret Leak Detector pre-commit hook installed.")
    print(f"📍 Hook: {target_hook}")


if __name__ == "__main__":
    install_hook()