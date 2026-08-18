# knowledge-core

Orchestration لایه دانش: parse → embed → index → retrieve → (APCS prompt).

## مسئولیت
- ایندکس اسناد از document-parser
- query معنایی از طریق retrieval-engine
- برگرداندن hits آماده Citation برای API / PromptBuilder

## وضعیت
MVP با InMemoryVectorStore + Embedder (Ollama/fallback).
