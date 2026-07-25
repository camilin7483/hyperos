# Security Policy

## Supported Versions

HyperOS is currently in pre-release development (v0.x). No stable releases are available yet. Security updates are applied at the distribution level during development.

| Version | Supported |
|---------|-----------|
| v0.x (dev) | ✅ Active development — security fixes applied continuously |
| < v0.1 | ❌ Pre-repository state, not supported |

---

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in HyperOS, please follow these steps:

### Do NOT

- **Do not** disclose the vulnerability publicly (no GitHub issues, no forums, no social media)
- **Do not** create a public pull request with the fix without coordinating
- **Do not** exploit the vulnerability beyond what is necessary to demonstrate it

### DO

1. **Send details** to the maintainers through a private channel:
   - GitHub Security Advisory (preferred): Navigate to the repository's **Security** tab → **Report a vulnerability**
   - Email: Use the maintainer's contact information from GitHub profile
2. **Include** the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Affected versions and components
   - Potential impact
   - Suggested fix (if available)
3. **Await response** — We will acknowledge receipt within 48 hours and work on a fix

### Disclosure Timeline

We aim to:
- **Acknowledge** within 48 hours
- **Assess** severity and impact within 5 business days
- **Release a fix** within 14 days for critical vulnerabilities
- **Publish advisory** after the fix is released

---

## Security Practices

### System-Level Security

| Area | Practice |
|------|----------|
| **Firewall** | nftables enabled by default with strict ruleset |
| **SSH** | Disabled by default (can be enabled via Hyper Center) |
| **Bluetooth** | Disabled by default |
| **Kernel** | linux-zen with hardened sysctl parameters |
| **Audit** | auditd configured for security-relevant events |
| **/tmp** | Mounted as tmpfs with `noexec,nosuid,nodev` |
| **swap** | Encrypted swap partition by default |
| **Boot** | Full disk encryption recommended during installation |
| **PAM** | `pam_faillock` enabled (account lockout after failed attempts) |
| **Core dumps** | Disabled (`LimitCORE=0` in systemd) |

### Application Security

- All GUI applications run as **unprivileged user**
- Privileged operations require **polkit** authentication
- No application holds root privileges persistently
- User input is sanitized before use in system commands
- Commands are constructed with arguments arrays (not shell strings) to prevent injection
- Temporary files use predictable names only within user-owned directories

### Kernel Hardening (sysctl)

```ini
# Network hardening
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.tcp_rfc1337 = 1

# Kernel hardening
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.printk = 3 3 3 3
kernel.unprivileged_bpf_disabled = 1
kernel.kexec_load_disabled = 1
kernel.sysrq = 0

# Memory hardening
vm.mmap_min_addr = 65536
vm.unprivileged_userfaultfd = 0

# BPF hardening
net.core.bpf_jit_harden = 2

# Link protection
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
fs.protected_regular = 2
fs.protected_fifos = 2
```

### Dependency Auditing

- All packages come from the official Arch Linux repositories
- Packages are signed and verified by pacman
- AUR packages are minimized and reviewed before inclusion
- Dependencies are updated with the system (weekly updates recommended)
- No vendored or bundled dependencies in HyperOS applications

### Build Security

- Builds are deterministic (same source → same binary)
- PKGBUILDs are reviewed for suspicious commands
- No network access during build (except for downloading sources)
- Checksums verify source integrity before build

---

## Secure Development Guidelines

### Code Requirements

```python
# ✅ DO: Use argument lists (prevents shell injection)
import subprocess
subprocess.run(["pacman", "-Qi", package_name], capture_output=True)

# ❌ DON'T: Use shell strings
import os
os.system(f"pacman -Qi {package_name}")  # Insecure!
```

### Secrets and Credentials

- **Never** hardcode credentials, API keys, tokens, or passwords
- **Never** commit secrets to the repository (use `.env` files or system keyrings)
- **Never** log sensitive information (passwords, tokens, personal data)
- Use the system keyring (Secret Service API) for storing secrets
- Configuration files with secrets should be `chmod 600`

### Input Validation

- Validate file paths (reject `../` traversal)
- Validate user input before using in system commands
- Reject unexpected input types and lengths
- Use allowlists over blocklists when filtering input

### Least Privilege

- Split privileged operations into separate scripts invoked via polkit
- Applications should request elevation only when necessary
- Release elevated privileges immediately after the operation completes
- Use `pkexec` or `polkit` actions rather than `sudo`

### Logging and Monitoring

- Log security-relevant events (authentication failures, privilege escalation)
- Do not log sensitive data (passwords, tokens, session keys)
- Logs should be readable only by root and the respective service user
- Use structured logging for automated log analysis

---

## Security Architecture

```
┌──────────────────────────────────────┐
│      User (unprivileged)             │
│  ┌──────┐ ┌──────┐ ┌─────────────┐ │
│  │Center│ │Store │ │Other Apps   │ │
│  └──┬───┘ └──┬───┘ └──────┬──────┘ │
│     │        │             │        │
├─────┼────────┼─────────────┼────────┤
│     ▼        ▼             ▼        │
│  ┌──────────────────────────────┐  │
│  │      Polkit (Authentication) │  │
│  └──────────┬───────────────────┘  │
├─────────────┼──────────────────────┤
│             ▼                      │
│  ┌──────────────────────────────┐  │
│  │   Privileged Operations     │  │
│  │  (systemd, pacman, sysctl)  │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

---

## Vulnerability Disclosure Process

```
Discovery → Private Report → Triage → Fix → Release → Public Advisory
    ↑                                                     │
    └─────────────────────────────────────────────────────┘
                     14 days max
```

1. **Discovery** — Security researcher finds vulnerability
2. **Private Report** — Reported via security advisory or encrypted email
3. **Triage** — Maintainer assesses severity and impact
   - **Critical**: Remote code execution, privilege escalation, data breach
   - **High**: Local privilege escalation, authentication bypass
   - **Medium**: Information disclosure, denial of service
   - **Low**: Minor information leaks, best practice violations
4. **Fix** — Patch developed and tested
5. **Release** — Fixed version published
6. **Public Advisory** — Details published after release

---

## Security Checklist for Contributors

Before submitting code, verify:

- [ ] No hardcoded secrets or credentials
- [ ] No shell injection vectors (use argument lists)
- [ ] User input is validated and sanitized
- [ ] File paths are validated (no path traversal)
- [ ] Temporary files are in secure locations
- [ ] No sensitive data is logged
- [ ] Privileged operations use polkit, not direct root
- [ ] Dependencies are from trusted sources
- [ ] No world-writable files or directories
- [ ] Descriptors and resources are properly cleaned up

---

## Contact

For security concerns, please use:
1. **GitHub Security Advisory** (preferred): Navigate to repository → Security → Report a vulnerability
2. **Maintainer email**: Available from GitHub profile

---

HyperOS is committed to providing a secure computing environment. Thank you for helping us improve.
