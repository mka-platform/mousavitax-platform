# API پرونده و خدمات — راهنمای سریع

## Endpoints جدید (v0.4.0)

| روش | مسیر | توضیح |
|-----|------|--------|
| GET | `/v1/services/catalog` | فهرست S01…S13 |
| POST | `/v1/triage` | سطح simple/medium/complex |
| POST | `/v1/cases` | تشکیل Tax Case |
| GET | `/v1/cases` | لیست پرونده‌ها (MVP) |
| GET | `/v1/cases/{id}` | جزئیات |
| POST | `/v1/cases/{id}/notes` | یادداشت |
| POST | `/v1/services/requests` | ثبت درخواست خدمت |
| GET | `/v1/services/requests` | لیست درخواست‌ها |

ذخیره موقت: `data/tax_cases.jsonl` و `data/service_requests.jsonl`

## نمونه PowerShell

```powershell
Invoke-RestMethod http://127.0.0.1:8000/v1/services/catalog

Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/v1/triage `
  -ContentType "application/json" `
  -Body '{"query":"اعتراض به برگ تشخیص سال 1402"}'

Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/v1/cases `
  -ContentType "application/json" `
  -Body '{"taxpayer_name":"آزمایشی","summary":"سؤال درباره سامانه مودیان","service_code":"S07","mobile":"09120000000"}'
```
