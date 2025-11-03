# ADR-004 — Estratégia de Filtros e Usabilidade
**Data:** 03/11/2025  
**Status:** Implementado  

## 1. Contexto  
A persona “Maria” precisava explorar dados livremente, sem limitações rígidas de relatórios.

## 2. Decisão  
Implementar dois tipos de filtros:  
- **Globais (Data, Loja)** — afetam todo o dashboard.  
- **Específicos** — aplicados a widgets isolados.

## 3. Justificativas  
- Aumentar a flexibilidade de análise.  
- Evitar colisões entre filtros diferentes.

## 4. Consequências  
- ✅ Experiência mais intuitiva.  
- ✅ Componentes reativos reutilizáveis.  
- ❌ Requer lógica extra de sincronização.
