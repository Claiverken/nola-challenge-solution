# ADR-003 — Arquitetura da API e Camadas de Comunicação
**Data:** 03/11/2025  
**Status:** Implementado  

## 1. Contexto  
A aplicação precisava lidar com grande volume de dados sem comprometer o desempenho do frontend.

## 2. Decisão  
Centralizar a lógica de agregação e processamento no **Backend**, expondo apenas **endpoints otimizados** em formato JSON.

## 3. Justificativas  
- Evita sobrecarga no navegador.  
- Simplifica o consumo de dados.  
- Aumenta a segurança.

## 4. Consequências  
- ✅ Frontend mais rápido e leve.  
- ✅ Backend escalável e testável.  
- ❌ Aumenta a complexidade no servidor.
