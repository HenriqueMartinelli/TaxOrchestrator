import io
import pandas as pd
import pytest
import time

def make_sample_excel():
    """
    Gera em memória um Excel válido com:
      - order 1001: 2 itens
      - order 2002: 1 item
    """
    df = pd.DataFrame({
        'order_id': ['1001', '1001', '2002'],
        'product_id': ['P001', 'P002', 'P003'],
        'quantity': [2, 1, 5],
        'unit_price': [10.0, 20.0, 5.0],
        'product_type': ['A', 'B', 'A'],
        'category_fiscal': ['CAT1', 'CAT2', 'CAT1'],
        'origin_state': ['SP', 'MG', 'SP'],
        'destination_state': ['RJ', 'SP', 'RJ'],
    })
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf

def test_process_and_list_and_get(client):
    buf = make_sample_excel()
    files = {
        'file': (
            'app/resources/sample_orders.xlsx',
            buf,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    }
    resp = client.post("/api/v1/orders/process", files=files)
    assert resp.status_code == 202
    assert resp.json() == {"message": "Processing started"}

    time.sleep(1.5)  # ou mais se necessário (ex: 3 segundos)

    # 2) LIST: sem filtro (deve retornar 2 pedidos distintos)
    resp = client.get("/api/v1/orders?status=PROCESSED&limit=10")
    
    assert resp.status_code == 200
    body = resp.json()
    assert "orders" in body
    assert isinstance(body["orders"], list)

    ids = {o["order_id"] for o in body["orders"]}
    assert ids == {"1001", "2002"}

    # 3) GET 
    resp = client.get("/api/v1/orders/1001")
    assert resp.status_code == 200
    o = resp.json()
    assert o["order_id"] == "1001"
    assert isinstance(o["items"], list)
    assert len(o["items"]) == 2

    # 4) GET not found
    resp = client.get("/api/v1/orders/does_not_exist")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Order not found"}

def test_invalid_extension(client):
    resp = client.post(
        "/api/v1/orders/process",
        files={"file": ("bad.txt", io.BytesIO(b"foo"), "text/plain")}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Somente arquivos .xls ou .xlsx são permitidos"
