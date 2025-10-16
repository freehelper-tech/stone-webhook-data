# Correção: Campos Removidos do Formulário Jotform

**Data:** 16 de outubro de 2025  
**Status:** ✅ Resolvido

## Problema

Após a remoção de 4 campos do formulário Jotform, o webhook começou a retornar erro 500:

### Campos Removidos
1. **Raça/cor**
2. **Quais são as suas fontes de renda atualmente?**
3. **Segmento de atuação do negócio**
4. **Se outros, qual o segmento de atuação do negócio**

### Erro Registrado

```
1 validation error for JotformWebhookPayload
Quais são as suas fontes de renda atualmente?
  Input should be a valid list [type=list_type, input_value='', input_type=str]
  For further information visit https://errors.pydantic.dev/2.12/v/list_type
```

**Causa raiz:**  
O Jotform envia strings vazias (`""`) para campos que foram removidos do formulário, mas o sistema esperava uma **lista** para o campo "Quais são as suas fontes de renda atualmente?", causando falha na validação do Pydantic.

## Solução Implementada

### 1. Ajustes no DTO (`dto/webhook_dtos.py`)

#### Mudanças nos imports
```python
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, EmailStr, field_validator
```

#### Campo fontes_renda aceita lista OU string
```python
fontes_renda: Optional[Union[List[str], str]] = Field(None, alias="Quais são as suas fontes de renda atualmente?")
```

#### Validadores customizados adicionados

**Validador para fontes_renda:**
```python
@field_validator('fontes_renda', mode='before')
@classmethod
def validate_fontes_renda(cls, v):
    """Validador para aceitar string vazia e convertê-la em None"""
    if v == "" or v is None:
        return None
    if isinstance(v, str):
        # Se for string não-vazia, retornar como lista
        return [v] if v.strip() else None
    return v
```

**Validador para outros campos removidos:**
```python
@field_validator('raca_cor', 'segmento_atuacao', 'segmento_outros', mode='before')
@classmethod
def validate_empty_string(cls, v):
    """Validador para converter strings vazias em None"""
    if v == "" or (isinstance(v, str) and not v.strip()):
        return None
    return v
```

### 2. Ajustes no Processador (`utils/jotform_processor.py`)

Função `processar_fontes_renda()` atualizada para lidar com:
- Listas (comportamento original)
- Strings não vazias (convertidas para lista)
- Strings vazias (retorna None)
- Campo ausente/None (retorna None)

```python
@staticmethod
def processar_fontes_renda(payload: JotformWebhookPayload) -> Optional[str]:
    """
    Processar fontes de renda
    Pode vir como lista, string ou None (campo removido do formulário)
    """
    try:
        # Se vier lista do Jotform
        if payload.fontes_renda and isinstance(payload.fontes_renda, list):
            # Filtrar itens vazios
            items = [str(item).strip() for item in payload.fontes_renda if item]
            return '; '.join(items) if items else None
        
        # Se vier string direta de fonte_renda
        if payload.fonte_renda and payload.fonte_renda.strip():
            return payload.fonte_renda.strip()
        
        # Fallback para fontes_renda como string
        if payload.fontes_renda and isinstance(payload.fontes_renda, str):
            stripped = payload.fontes_renda.strip()
            return stripped if stripped else None
        
        # Campo removido do formulário ou vazio
        return None
        
    except Exception as e:
        logger.error(f"Erro ao processar fontes de renda: {e}")
        return None
```

## Testes Realizados

### ✅ Teste 1: Payload com campos removidos (strings vazias)
**Cenário:** Payload exato que causou o erro nos logs  
**Resultado:** ✅ Passou - Campos vazios convertidos para `None`

### ✅ Teste 2: Payload com campos preenchidos (lista)
**Cenário:** Formulário com todos os campos preenchidos (comportamento normal)  
**Resultado:** ✅ Passou - Lista processada corretamente como "Emprego formal; Freelancer"

### ✅ Teste 3: Payload com fontes de renda como string
**Cenário:** Campo vindo como string ao invés de lista  
**Resultado:** ✅ Passou - String convertida para lista e processada corretamente

## Comportamento Após a Correção

| Entrada | Processamento | Saída |
|---------|---------------|-------|
| `""` (string vazia) | Convertido para `None` | `None` |
| `"Emprego formal"` (string) | Convertido para lista `["Emprego formal"]` | `"Emprego formal"` |
| `["Emprego formal", "Freelancer"]` (lista) | Processado diretamente | `"Emprego formal; Freelancer"` |
| `None` ou ausente | Mantido como `None` | `None` |

## Impacto

✅ **Retrocompatibilidade:** Mantida - formulários antigos com campos preenchidos continuam funcionando  
✅ **Novos formulários:** Aceita campos removidos sem gerar erros  
✅ **Flexibilidade:** Aceita tanto lista quanto string para fontes de renda  
✅ **Robustez:** Tratamento de casos extremos (strings vazias, None, etc.)

## Arquivos Modificados

1. `dto/webhook_dtos.py` - Adicionados validadores customizados
2. `utils/jotform_processor.py` - Melhorado processamento de fontes de renda

## Validação em Produção

Para validar em produção:

1. Monitorar logs do webhook para o endpoint `/api/v1/webhook/jotform`
2. Verificar se payloads com campos vazios são processados sem erros
3. Confirmar que empreendedores são criados com sucesso no banco de dados
4. Validar que campos `None` são salvos corretamente

## Observações

- A correção é **compatível com Pydantic v2.x** (usa `field_validator` ao invés de `validator`)
- Campos removidos são salvos como `NULL` no banco de dados
- A API continua aceitando campos extras devido à configuração `extra = "allow"`
- Logs detalhados ajudam a debugar problemas futuros

## Próximos Passos (Opcional)

1. Considerar adicionar testes automatizados de integração
2. Documentar no Jotform quais campos são obrigatórios vs opcionais
3. Adicionar alertas para campos críticos ausentes

