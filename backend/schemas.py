# schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# 1. KpiResponse
class KpiResponse(BaseModel):
    total_revenue: float
    total_sales: int
    average_ticket: float
    class Config:
        from_attributes = True

# 2. ProductSaleStat
class ProductSaleStat(BaseModel):
    product_id: int
    product_name: str
    total_sold: float
    total_revenue: float
    class Config:
        from_attributes = True

# 3. TimeSeriesDataPoint
class TimeSeriesDataPoint(BaseModel):
    date: str
    group: Optional[str] = None
    value: float
    class Config:
        from_attributes = True

# 4. TimeSeriesResponse
class TimeSeriesResponse(BaseModel):
    start_date: date
    end_date: date
    time_unit: str
    metric: str
    data: List[TimeSeriesDataPoint]

# 5. ItemSaleStat
class ItemSaleStat(BaseModel):
    item_id: int
    item_name: str
    total_sold: float
    total_revenue: float
    class Config:
        from_attributes = True

# 6. DeliveryPerformanceStat
class DeliveryPerformanceStat(BaseModel):
    neighborhood: Optional[str] = "N/A"
    city: Optional[str] = "N/A"
    total_deliveries: int
    avg_delivery_minutes: float
    class Config:
        from_attributes = True

# 7. CustomerSegmentStat
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

# 8. StoreSCHEMA
class StoreSchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True