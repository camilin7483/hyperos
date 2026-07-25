# Hyper Backup Architecture

## Overview

Hyper Backup manages system snapshots and user data backups.

## Component Tree

```
HyperBackup
├── SnapshotManager
│   ├── SnapshotList
│   ├── CreateSnapshot
│   └── RestoreSnapshot
├── DataBackup
│   ├── BackupProfiles
│   └── RestoreWizard
└── Scheduler
    ├── BackupSchedule
    └── RetentionPolicy
```

## Data Flow

1. SnapshotManager interfaces with Btrfs/LVM snapshots
2. DataBackup handles file-level backups via rsync
3. Scheduler manages cron/systemd timer-based backups
