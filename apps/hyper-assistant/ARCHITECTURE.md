# Hyper Assistant Architecture

## Overview

Hyper Assistant provides natural language interaction with the HyperOS system.

## Component Tree

```
HyperAssistant
├── ChatInterface
│   ├── MessageHistory
│   └── InputHandler
├── LLMBackend
│   ├── LocalModel
│   └── RemoteAPI
└── SystemActions
    ├── CommandParser
    └── ActionExecutor
```

## Data Flow

1. User input is processed by ChatInterface
2. LLMBackend interprets natural language
3. SystemActions converts intent to system operations
4. Results are displayed in chat format
