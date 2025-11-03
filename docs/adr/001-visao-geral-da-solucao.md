# ADR-001 — Visão Geral da Solução
**Data:** 03/11/2025  
**Status:** Implementado  

## 1. Contexto  
O objetivo era criar uma ferramenta de BI *self-service* para a persona “Maria”, permitindo-lhe explorar seus dados de vendas (500k+ registros) sem precisar de código.

## 2. Decisão  
Desenvolver uma aplicação **Full-Stack desacoplada**, composta por:  
- **Backend (API)**: responsável por processamento, queries e agregação de dados.  
- **Frontend (Dashboard)**: responsável por visualização e interação do usuário.

## 3. Consequências  
- ✅ Separação clara entre lógica de negócio e interface.  
- ✅ Escalabilidade horizontal.  
- ❌ Necessário implementar autenticação e CORS.
