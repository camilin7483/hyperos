#!/usr/bin/env python3
"""Main entry point for hyperos-daemon."""

import argparse
import logging
import signal
import sys
from pathlib import Path

from hyperos_daemon.daemon import HyperOSDaemon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="HyperOS System Daemon")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("/etc/hyperos/daemon.conf"),
        help="Path to configuration file",
    )
    parser.add_argument(
        "--no-dbus",
        action="store_true",
        help="Run without D-Bus integration (debug mode)",
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("Starting HyperOS Daemon v%s", "0.1.0")
    
    daemon = HyperOSDaemon(
        config_path=args.config,
        use_dbus=not args.no_dbus,
    )
    
    def signal_handler(signum, frame):
        logger.info("Received signal %s, shutting down...", signum)
        daemon.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        daemon.start()
    except Exception as e:
        logger.error("Daemon failed to start: %s", e)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
