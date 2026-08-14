"""Package management service for HyperOS daemon."""

import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


class PackageService:
    """Service for package management operations.
    
    Provides secure package operations via pacman:
    - Query installed packages
    - Search available packages
    - Install/remove packages (with authorization)
    - Check for updates
    - Sync databases
    """
    
    def __init__(self) -> None:
        self._cache_valid = False
    
    def _run_pacman(self, args: list[str], check: bool = False) -> subprocess.CompletedProcess:
        """Run pacman command with proper error handling."""
        cmd = ["pacman"] + args
        logger.debug("Running pacman: %s", " ".join(cmd))
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes for operations
            )
            
            if check and result.returncode != 0:
                logger.error("Pacman failed: %s", result.stderr)
            
            return result
        except subprocess.TimeoutExpired:
            logger.error("Pacman command timed out")
            raise
        except Exception as e:
            logger.error("Failed to run pacman: %s", e)
            raise
    
    def get_installed_packages(self) -> list[dict]:
        """Get list of installed packages."""
        packages = []
        try:
            result = self._run_pacman(["-Q"])
            
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append({
                        "name": parts[0],
                        "version": parts[1],
                    })
        except Exception as e:
            logger.error("Failed to list installed packages: %s", e)
        
        return packages
    
    def get_installed_count(self) -> int:
        """Get count of installed packages."""
        try:
            result = self._run_pacman(["-Q"])
            return len(result.stdout.splitlines())
        except Exception as e:
            logger.error("Failed to count packages: %s", e)
            return 0
    
    def search_packages(self, query: str) -> list[dict]:
        """Search for packages in repositories."""
        results = []
        try:
            result = self._run_pacman(["-Ss", query])
            
            current_pkg = {}
            for line in result.stdout.splitlines():
                if line.startswith(" ") and ":" in line:
                    # This is a package description line
                    if current_pkg:
                        results.append(current_pkg)
                    
                    parts = line.strip().split(" ", 1)
                    name_repo = parts[0].split("/")
                    
                    current_pkg = {
                        "name": name_repo[-1] if len(name_repo) > 1 else name_repo[0],
                        "repository": name_repo[0] if len(name_repo) > 1 else "unknown",
                        "version": parts[1].split()[0] if len(parts) > 1 and len(parts[1].split()) > 0 else "",
                        "description": parts[1].split(" ", 1)[-1] if len(parts) > 1 and " " in parts[1] else "",
                    }
            
            if current_pkg:
                results.append(current_pkg)
                
        except Exception as e:
            logger.error("Failed to search packages: %s", e)
        
        return results
    
    def get_package_info(self, name: str) -> Optional[dict]:
        """Get detailed information about a package."""
        try:
            result = self._run_pacman(["-Qi", name])
            
            if result.returncode != 0:
                return None
            
            info = {"name": name}
            for line in result.stdout.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    info[key.strip().lower().replace(" ", "_")] = val.strip()
            
            return info
        except Exception as e:
            logger.error("Failed to get package info: %s", e)
            return None
    
    def get_available_updates(self) -> list[dict]:
        """Get list of available updates."""
        updates = []
        try:
            result = self._run_pacman(["-Qu"])
            
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    updates.append({
                        "name": parts[0],
                        "current_version": parts[1] if len(parts) > 1 else "",
                        "new_version": parts[2] if len(parts) > 2 else "",
                    })
        except Exception as e:
            logger.debug("Could not check updates: %s", e)
        
        return updates
    
    def get_update_count(self) -> int:
        """Get count of available updates."""
        try:
            result = self._run_pacman(["-Qu"])
            return len([l for l in result.stdout.splitlines() if l.strip()])
        except Exception as e:
            logger.debug("Could not count updates: %s", e)
            return 0
    
    def install_package(self, name: str, noconfirm: bool = True) -> bool:
        """Install a package.
        
        Note: This should only be called after proper authorization checks.
        """
        logger.info("Installing package: %s", name)
        try:
            args = ["-S"]
            if noconfirm:
                args.append("--noconfirm")
            args.append(name)
            
            result = self._run_pacman(args)
            success = result.returncode == 0
            
            if success:
                logger.info("Successfully installed %s", name)
            else:
                logger.error("Failed to install %s: %s", name, result.stderr)
            
            return success
        except Exception as e:
            logger.error("Exception during installation of %s: %s", name, e)
            return False
    
    def remove_package(self, name: str, noconfirm: bool = True) -> bool:
        """Remove a package.
        
        Note: This should only be called after proper authorization checks.
        """
        logger.info("Removing package: %s", name)
        try:
            args = ["-R"]
            if noconfirm:
                args.append("--noconfirm")
            args.append(name)
            
            result = self._run_pacman(args)
            success = result.returncode == 0
            
            if success:
                logger.info("Successfully removed %s", name)
            else:
                logger.error("Failed to remove %s: %s", name, result.stderr)
            
            return success
        except Exception as e:
            logger.error("Exception during removal of %s: %s", name, e)
            return False
    
    def update_system(self, noconfirm: bool = True) -> bool:
        """Update the entire system.
        
        Note: This should only be called after proper authorization checks.
        """
        logger.info("Starting system update")
        try:
            args = ["-Syu"]
            if noconfirm:
                args.append("--noconfirm")
            
            result = self._run_pacman(args)
            success = result.returncode == 0
            
            if success:
                logger.info("System update completed successfully")
            else:
                logger.error("System update failed: %s", result.stderr)
            
            return success
        except Exception as e:
            logger.error("Exception during system update: %s", e)
            return False
    
    def sync_databases(self, force: bool = False) -> bool:
        """Sync package databases."""
        logger.info("Syncing package databases")
        try:
            args = ["-Sy"]
            if force:
                args.append("-y")  # -Syy forces refresh
            
            result = self._run_pacman(args)
            return result.returncode == 0
        except Exception as e:
            logger.error("Failed to sync databases: %s", e)
            return False
    
    def clean_cache(self, all_versions: bool = False) -> bool:
        """Clean package cache."""
        logger.info("Cleaning package cache")
        try:
            args = ["-Sc"]
            if all_versions:
                args = ["-Scc"]
            
            # Note: This requires confirmation, so we don't use --noconfirm
            result = self._run_pacman(args)
            return result.returncode == 0
        except Exception as e:
            logger.error("Failed to clean cache: %s", e)
            return False
