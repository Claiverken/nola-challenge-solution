# main.py (VERSÃO CORRIGIDA E COM FILTRO GLOBAL DE LOJA)
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

# Importa as funções que acabámos de criar em database.py
from database import get_db, test_connection
# Importa TODOS os schemas
from schemas import (
    KpiResponse, ProductSaleStat, TimeSeriesResponse,
    TimeSeriesDataPoint, ItemSaleStat, DeliveryPerformanceStat,
    CustomerSegmentStat, StoreSchema
)

# 1. Cria a instância da aplicação FastAPI
app = FastAPI(
    title="Nola BI API",
    description="API para servir dados de BI para o desafio God Level.",
    version="0.1.0"
)

# --- CORREÇÃO DE CORS ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints de Teste (Iguais) ---
@app.get("/")
def read_root():
    return {"message": "Olá! Bem-vindo à API do Desafio Nola!"}


@app.get("/api/v1/test-connection")
def api_test_connection(db: Session = Depends(get_db)):  # Adicionado get_db
    if test_connection():
        return {"status": "sucesso", "message": "Conexão com a base de dados bem-sucedida!"}
    else:
        return {"status": "falha", "message": "Falha ao conectar à base de dados."}


@app.get("/api/v1/test-data")
def get_real_data(db: Session = Depends(get_db)):
    try:
        query = text("SELECT COUNT(*) FROM sales")
        total_sales = db.execute(query).scalar()
        return {"total_sales": total_sales, "metric_name": "Total de Vendas (Real)", "source": "PostgreSQL no Docker"}
    except Exception as e:
        return {"error": str(e)}


# 5. ATUALIZADO: Endpoint de KPIs (com store_id)
@app.get("/api/v1/kpis/main", response_model=KpiResponse)
def get_main_kpis(
        start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
        store_id: Optional[int] = Query(None, description="Filtrar por um ID de loja específico"),  # <-- MUDANÇA
        db: Session = Depends(get_db)
):
    base_query = """
        SELECT
            COALESCE(SUM(total_amount), 0) AS total_revenue,
            COALESCE(COUNT(id), 0) AS total_sales
        FROM sales s -- Adicionado 's'
        WHERE s.sale_status_desc = 'COMPLETED'
    """
    params = {}
    if start_date:
        base_query += " AND DATE(s.created_at) >= :start_date"
        params["start_date"] = start_date
    if end_date:
        base_query += " AND DATE(s.created_at) <= :end_date"
        params["end_date"] = end_date
    if store_id:  # <-- MUDANÇA
        base_query += " AND s.store_id = :store_id"
        params["store_id"] = store_id

    try:
        result = db.execute(text(base_query), params).first()
        if not result or result.total_sales == 0:
            return KpiResponse(total_revenue=0, total_sales=0, average_ticket=0)
        avg_ticket = result.total_revenue / result.total_sales
        return KpiResponse(
            total_revenue=round(result.total_revenue, 2),
            total_sales=result.total_sales,
            average_ticket=round(avg_ticket, 2)
        )
    except Exception as e:
        return {"error": str(e)}


# 6. ATUALIZADO: Endpoint Top Produtos (com store_id)
@app.get("/api/v1/analytics/top-products", response_model=List[ProductSaleStat])
def get_top_products(
        start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
        store_id: Optional[int] = Query(None, description="Filtrar por um ID de loja específico"),  # <-- MUDANÇA
        channel_type: Optional[str] = Query(None, description="Tipo de Canal: 'D' (Delivery) ou 'P' (Presencial)"),
        limit: int = Query(10, description="Número de produtos a retornar (Top N)"),
        db: Session = Depends(get_db)
):
    base_query = """
        SELECT
            p.id AS product_id, p.name AS product_name,
            SUM(ps.quantity) AS total_sold, SUM(ps.total_price) AS total_revenue
        FROM product_sales ps
        JOIN products p ON ps.product_id = p.id
        JOIN sales s ON ps.sale_id = s.id
        JOIN channels c ON s.channel_id = c.id
        WHERE s.sale_status_desc = 'COMPLETED'
    """
    params = {"limit": limit}
    if start_date:
        base_query += " AND DATE(s.created_at) >= :start_date"
        params["start_date"] = start_date
    if end_date:
        base_query += " AND DATE(s.created_at) <= :end_date"
        params["end_date"] = end_date
    if store_id:  # <-- MUDANÇA
        base_query += " AND s.store_id = :store_id"
        params["store_id"] = store_id
    if channel_type:
        base_query += " AND c.type = :channel_type"
        params["channel_type"] = channel_type

    base_query += " GROUP BY p.id, p.name ORDER BY total_sold DESC LIMIT :limit"

    try:
        results = db.execute(text(base_query), params).fetchall()
        top_products = [
            ProductSaleStat(
                product_id=row.product_id,
                product_name=row.product_name,
                total_sold=row.total_sold,
                total_revenue=round(row.total_revenue, 2)
            ) for row in results
        ]
        return top_products
    except Exception as e:
        return {"error": str(e)}


# 7. MUDANÇA: Endpoint de Série Temporal (com datas opcionais e store_id)
@app.get("/api/v1/analytics/time-series", response_model=TimeSeriesResponse)
def get_time_series(
        start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
        metric: str = Query(..., description="Métrica: 'total_revenue', 'total_sales', ou 'average_ticket'"),
        time_unit: str = Query('day', description="Agrupar por: 'day', 'week', ou 'month'"),
        group_by: Optional[str] = Query(None, description="Agrupar por categoria: 'channel' ou 'store'"),
        store_id: Optional[int] = Query(None, description="Filtrar por um ID de loja específico"),  # <-- MUDANÇA
        channel_id: Optional[int] = Query(None, description="Filtrar por um ID de canal específico"),
        db: Session = Depends(get_db)
):
    if metric not in ['total_revenue', 'total_sales', 'average_ticket']:
        raise HTTPException(status_code=422, detail="Métrica inválida.")
    if time_unit not in ['day', 'week', 'month']:
        raise HTTPException(status_code=422, detail="Unidade de tempo inválida.")
    if group_by and group_by not in ['channel', 'store']:
        raise HTTPException(status_code=422, detail="Agrupamento inválido.")

    select_clause = f"SELECT DATE_TRUNC('{time_unit}', s.created_at)::date AS date,"
    group_by_clause_columns = ["date"]
    order_by_clause_columns = ["date"]

    if group_by == 'channel':
        select_clause += " c.name AS group,"
        group_by_clause_columns.append("c.name")
        order_by_clause_columns.append("c.name")
    elif group_by == 'store':
        select_clause += " st.name AS group,"
        group_by_clause_columns.append("st.name")
        order_by_clause_columns.append("st.name")
    else:
        select_clause += " 'all' AS group,"

    select_clause += """
        COALESCE(SUM(s.total_amount), 0.0) AS total_revenue,
        COALESCE(COUNT(s.id), 0) AS total_sales,
        COALESCE(SUM(s.total_amount) / NULLIF(COUNT(s.id), 0), 0.0) AS average_ticket
    """

    from_clause = "FROM sales s"
    if group_by == 'channel':
        from_clause += " JOIN channels c ON s.channel_id = c.id"
    if group_by == 'store':
        from_clause += " JOIN stores st ON s.store_id = st.id"

    where_clause = " WHERE s.sale_status_desc = 'COMPLETED' "
    params = {}

    if start_date:
        where_clause += " AND DATE(s.created_at) >= :start_date"
        params["start_date"] = start_date
    if end_date:
        where_clause += " AND DATE(s.created_at) <= :end_date"
        params["end_date"] = end_date
    if channel_id:
        where_clause += " AND s.channel_id = :channel_id"
        params["channel_id"] = channel_id
    if store_id:  # <-- MUDANÇA
        where_clause += " AND s.store_id = :store_id"
        params["store_id"] = store_id

    final_query = f"""
        {select_clause}
        {from_clause}
        {where_clause}
        GROUP BY {', '.join(group_by_clause_columns)}
        ORDER BY {', '.join(order_by_clause_columns)}
    """

    try:
        results = db.execute(text(final_query), params).fetchall()
        data_points = []
        for row in results:
            value = 0
            if metric == 'total_revenue':
                value = row.total_revenue
            elif metric == 'total_sales':
                value = row.total_sales
            elif metric == 'average_ticket':
                value = row.average_ticket
            data_points.append(
                TimeSeriesDataPoint(
                    date=row.date.isoformat(), group=row.group, value=round(value, 2)
                )
            )
        return TimeSeriesResponse(
            start_date=start_date or date.min,
            end_date=end_date or date.today(),
            time_unit=time_unit,
            metric=metric,
            data=data_points
        )
    except Exception as e:
        print(f"Erro na query SQL: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a query: {e}")


# 8. ATUALIZADO: Endpoint Top Itens (com store_id)
@app.get("/api/v1/analytics/top-items", response_model=List[ItemSaleStat])
def get_top_items(
        start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
        store_id: Optional[int] = Query(None, description="Filtrar por um ID de loja específico"),  # <-- MUDANÇA
        limit: int = Query(10, description="Número de itens a retornar (Top N)"),
        db: Session = Depends(get_db)
):
    base_query = """
        SELECT
            i.id AS item_id, i.name AS item_name,
            SUM(ips.quantity) AS total_sold, SUM(ips.additional_price) AS total_revenue
        FROM item_product_sales ips
        JOIN items i ON i.id = ips.item_id
        JOIN product_sales ps ON ps.id = ips.product_sale_id
        JOIN sales s ON s.id = ps.sale_id
        WHERE s.sale_status_desc = 'COMPLETED'
    """
    params = {"limit": limit}
    if start_date:
        base_query += " AND DATE(s.created_at) >= :start_date"
        params["start_date"] = start_date
    if end_date:
        base_query += " AND DATE(s.created_at) <= :end_date"
        params["end_date"] = end_date
    if store_id:  # <-- MUDANÇA
        base_query += " AND s.store_id = :store_id"
        params["store_id"] = store_id

    base_query += " GROUP BY i.id, i.name ORDER BY total_sold DESC LIMIT :limit"

    try:
        results = db.execute(text(base_query), params).fetchall()
        top_items = [
            ItemSaleStat(
                item_id=row.item_id,
                item_name=row.item_name,
                total_sold=row.total_sold,
                total_revenue=round(row.total_revenue, 2)
            ) for row in results
        ]
        return top_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a query: {e}")


# 9. ATUALIZADO: Endpoint Performance de Entrega (com store_id)
@app.get("/api/v1/analytics/delivery-performance", response_model=List[DeliveryPerformanceStat])
def get_delivery_performance(
        start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
        store_id: Optional[int] = Query(None, description="Filtrar por um ID de loja específico"),  # <-- MUDANÇA
        limit: int = Query(10, description="Número de bairros a retornar (Top N)"),
        min_deliveries: int = Query(1, description="Mínimo de entregas para o bairro aparecer"),  # Padrão 1
        db: Session = Depends(get_db)
):
    base_query = """
        SELECT 
            da.neighborhood, da.city,
            COUNT(*) as total_deliveries,
            AVG(s.delivery_seconds / 60.0) as avg_delivery_minutes
        FROM sales s
        JOIN delivery_addresses da ON da.sale_id = s.id
        WHERE s.sale_status_desc = 'COMPLETED' AND s.delivery_seconds IS NOT NULL
    """
    params = {"limit": limit, "min_deliveries": min_deliveries}
    if start_date:
        base_query += " AND DATE(s.created_at) >= :start_date"
        params["start_date"] = start_date
    if end_date:
        base_query += " AND DATE(s.created_at) <= :end_date"
        params["end_date"] = end_date
    if store_id:  # <-- MUDANÇA
        base_query += " AND s.store_id = :store_id"
        params["store_id"] = store_id

    base_query += " GROUP BY da.neighborhood, da.city HAVING COUNT(*) >= :min_deliveries ORDER BY avg_delivery_minutes DESC LIMIT :limit"

    try:
        results = db.execute(text(base_query), params).fetchall()
        performance_stats = [
            DeliveryPerformanceStat(
                neighborhood=row.neighborhood,
                city=row.city,
                total_deliveries=row.total_deliveries,
                avg_delivery_minutes=round(row.avg_delivery_minutes, 2)
            ) for row in results
        ]
        return performance_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a query: {e}")


# 10. Endpoint Clientes em Risco (Simplificado - usa sempre HOJE)
@app.get("/api/v1/analytics/customer-segments", response_model=List[CustomerSegmentStat])
def get_customer_segments(
        min_recency_days: int = Query(30, description="Nº mínimo de dias desde a última compra"),
        min_frequency: int = Query(3, description="Nº mínimo de compras"),
        limit: int = Query(50, description="Nº máximo de clientes a retornar"),
        db: Session = Depends(get_db)
):
    base_query = """
        WITH customer_kpis AS (
            SELECT
                customer_id,
                COUNT(s.id) AS frequency,
                SUM(s.total_amount) AS monetary_value,
                MAX(s.created_at) AS last_purchase_date,
                EXTRACT(DAY FROM (CURRENT_DATE - MAX(s.created_at))) AS recency_days
            FROM sales s
            WHERE
                s.sale_status_desc = 'COMPLETED'
                AND s.customer_id IS NOT NULL
            GROUP BY customer_id
        )
        SELECT
            k.customer_id,
            c.customer_name,
            c.phone_number AS customer_phone,
            k.last_purchase_date::date,
            k.recency_days::int,
            k.frequency,
            k.monetary_value
        FROM customer_kpis k
        LEFT JOIN customers c ON k.customer_id = c.id
        WHERE
            k.recency_days >= :min_recency_days
            AND k.frequency >= :min_frequency
        ORDER BY
            k.recency_days DESC,
            k.frequency DESC
        LIMIT :limit
    """
    params = {
        "min_recency_days": min_recency_days,
        "min_frequency": min_frequency,
        "limit": limit
    }
    try:
        results = db.execute(text(base_query), params).fetchall()
        customers = [
            CustomerSegmentStat(
                customer_id=row.customer_id,
                customer_name=row.customer_name,
                customer_phone=row.customer_phone,
                last_purchase_date=row.last_purchase_date,
                recency_days=row.recency_days,
                frequency=row.frequency,
                monetary_value=round(row.monetary_value, 2)
            ) for row in results
        ]
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a query: {e}")


# 11. Endpoint Top Clientes (AGORA GLOBAL, com store_id)
@app.get("/api/v1/analytics/top-customers", response_model=List[CustomerSegmentStat])
def get_top_customers(
        start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
        end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
        store_id: Optional[int] = Query(None, description="Filtrar por um ID de loja específico"),
        sort_by: str = Query('monetary_value', description="Ordenar por: 'monetary_value' ou 'frequency'"),
        limit: int = Query(10, description="Nº máximo de clientes a retornar"),
        db: Session = Depends(get_db)
):
    if sort_by not in ['monetary_value', 'frequency']:
        raise HTTPException(status_code=422, detail="sort_by inválido. Use 'monetary_value' ou 'frequency'.")

    base_query = """
        WITH customer_kpis AS (
            SELECT
                customer_id,
                COUNT(s.id) AS frequency,
                SUM(s.total_amount) AS monetary_value,
                MAX(s.created_at) AS last_purchase_date,
                EXTRACT(DAY FROM (CURRENT_DATE - MAX(s.created_at))) AS recency_days
            FROM sales s
            WHERE
                s.sale_status_desc = 'COMPLETED'
                AND s.customer_id IS NOT NULL
    """
    params = {"limit": limit}
    if start_date:
        base_query += " AND DATE(s.created_at) >= :start_date"
        params["start_date"] = start_date
    if end_date:
        base_query += " AND DATE(s.created_at) <= :end_date"
        params["end_date"] = end_date
    if store_id:  # <-- MUDANÇA (Já estava aqui, mas agora é global)
        base_query += " AND s.store_id = :store_id"
        params["store_id"] = store_id

    base_query += """
            GROUP BY customer_id
        )
        SELECT
            k.customer_id,
            c.customer_name,
            c.phone_number AS customer_phone,
            k.last_purchase_date::date,
            k.recency_days::int,
            k.frequency,
            k.monetary_value
        FROM customer_kpis k
        LEFT JOIN customers c ON k.customer_id = c.id
        ORDER BY
            CASE WHEN :sort_by = 'monetary_value' THEN k.monetary_value END DESC,
            CASE WHEN :sort_by = 'frequency' THEN k.frequency END DESC
        LIMIT :limit
    """
    params["sort_by"] = sort_by
    try:
        results = db.execute(text(base_query), params).fetchall()
        customers = [
            CustomerSegmentStat(
                customer_id=row.customer_id,
                customer_name=row.customer_name,
                customer_phone=row.customer_phone,
                last_purchase_date=row.last_purchase_date,
                recency_days=row.recency_days,
                frequency=row.frequency,
                monetary_value=round(row.monetary_value, 2)
            ) for row in results
        ]
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a query: {e}")


# 12. Endpoint de Lojas (Fica igual)
@app.get("/api/v1/stores", response_model=List[StoreSchema])
def get_stores(db: Session = Depends(get_db)):
    try:
        query = text("SELECT id, name FROM stores WHERE is_active = true ORDER BY name LIMIT 50")
        results = db.execute(query).fetchall()
        stores = [StoreSchema(id=row.id, name=row.name) for row in results]
        return stores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a query: {e}")