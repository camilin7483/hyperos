# API

Core API definitions for HyperOS.

## Purpose

Define the programmatic interfaces that HyperOS applications use to interact with the system. This includes REST-like endpoints over local sockets and DBus method signatures.

## Planned APIs

- System API — hardware and OS information
- Package API — package management
- Update API — system updates
- Config API — configuration management
- Profile API — performance profile management

## Design

APIs follow a consistent pattern:

```
/hyperos/v1/<resource>/<action>
```

All APIs return structured responses with status codes and error handling.
