# schemas.py (ATUALIZADO)
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# 1. KpiResponse (Fica igual)
class KpiResponse(BaseModel):
    total_revenue: float
    total_sales: int
    average_ticket: float
    class Config:
        from_attributes = True

# 2. ProductSaleStat (Fica igual)
class ProductSaleStat(BaseModel):
    product_id: int
    product_name: str
    total_sold: float
    total_revenue: float
    class Config:
        from_attributes = True

# 3. TimeSeriesDataPoint (Fica igual)
class TimeSeriesDataPoint(BaseModel):
    date: str
    group: Optional[str] = None
    value: float
    class Config:
        from_attributes = True

# 4. TimeSeriesResponse (Fica igual)
class TimeSeriesResponse(BaseModel):
    start_date: date
    end_date: date
    time_unit: str
    metric: str
    data: List[TimeSeriesDataPoint]

# 5. ItemSaleStat (Fica igual)
class ItemSaleStat(BaseModel):
    item_id: int
    item_name: str
    total_sold: float
    total_revenue: float
    class Config:
        from_attributes = True

# 6. DeliveryPerformanceStat (Fica igual)
class DeliveryPerformanceStat(BaseModel):
    neighborhood: Optional[str] = "N/A"
    city: Optional[str] = "N/A"
    total_deliveries: int
    avg_delivery_minutes: float
    class Config:
        from_attributes = True

# 7. CustomerSegmentStat (Fica igual)
class CustomerSegmentStat(BaseModel):
    customer_id: int
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    last_purchase_date: date
    recency_days: int
    frequency: int
    monetary_value: float
    class Config:
        from_attributes = True

# 8. NOVO SCHEMA (Para a lista de lojas)
class StoreSchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True