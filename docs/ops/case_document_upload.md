# آپلود مدرک به پرونده (Tax Case)

## API

```
POST /v1/cases/{case_id}/documents
Content-Type: multipart/form-data

fields:
  file      = فایل (اجباری)
  doc_type  = assessment | return | invoice | contract | other
  title     = عنوان اختیاری
```

لیست:
```
GET /v1/cases/{case_id}/documents
GET /v1/cases/{case_id}   # شامل documents[]
```

## محدودیت MVP
- حداکثر ۱۵ مگابایت
- پسوندهای مجاز: pdf, png, jpg, jpeg, webp, gif, doc, docx, xls, xlsx, txt, md, csv
- ذخیره: `data/case_uploads/{case_id}/`
- متادیتا: `data/case_documents.jsonl`
- استخراج متن کامل PDF در فاز بعد (Document AI)

## ترتیب کار
1. ساخت پرونده → `POST /v1/cases` → برداشتن `id`
2. آپلود فایل با همان `id`
3. مشاهده با `GET /v1/cases/{id}/documents`

## PowerShell

```powershell
# ۱) پرونده
$case = Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/v1/cases `
  -ContentType "application/json; charset=utf-8" `
  -Body '{"taxpayer_name":"آزمایشی","summary":"برگ تشخیص برای بررسی","service_code":"S03","mobile":"09120000000"}'
$caseId = $case.id
$caseId

# ۲) آپلود
$path = "C:\Users\ziya\Documents\sample.pdf"   # مسیر فایل خودتان
curl.exe -X POST "http://127.0.0.1:8000/v1/cases/$caseId/documents" `
  -F "file=@$path" `
  -F "doc_type=assessment" `
  -F "title=برگ تشخیص"

# ۳) لیست
Invoke-RestMethod "http://127.0.0.1:8000/v1/cases/$caseId/documents"
```

## Swagger
http://127.0.0.1:8000/docs → بخش cases-services → `POST /v1/cases/{case_id}/documents`
