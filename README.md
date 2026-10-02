# AI Destekli Bilgi Asistanı

Bu proje, kurgusal bir müşteri destek ekibi için geliştirilmiş Türkçe bir RAG (Retrieval-Augmented Generation) servisidir.

Servis, `documents/` klasöründeki bilgi dokümanlarını arar, kullanıcı sorularını yalnızca ilgili dokümanlardaki bilgilere göre yanıtlar ve kullanılan doküman ile bölümü kaynak olarak döndürür.

## Kullanılan Teknolojiler

- Python 3.12
- FastAPI
- PostgreSQL + pgvector
- SQLAlchemy + Alembic
- Ollama
- Docker Compose

## Proje Yapısı

```text
app/            API ve RAG servisleri
documents/      Bilgi dokümanları
evaluation/     Evaluation senaryoları ve sonuçları
alembic/        Veritabanı migration dosyaları
compose.yml     Docker servisleri
```

## Çalıştırma

Projeyi klonladıktan sonra repository root dizininde:

```bash
cp .env.example .env
docker compose up -d --build
```

Ollama modellerini hazırlayın:

```bash
docker compose --profile setup run --rm ollama-init
```

Veritabanı migration'larını çalıştırın:

```bash
docker compose exec api alembic upgrade head
```

Dokümanları veritabanına aktarın:

```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest
```

Servisin çalıştığını kontrol etmek için:

```bash
curl http://localhost:8000/health
```

Beklenen cevap:

```json
{
  "status": "ok"
}
```

## Swagger

API endpoint'lerini Swagger üzerinden görüntüleyebilir ve doğrudan test edebilirsiniz:

http://127.0.0.1:8000/docs

Swagger üzerinden `/api/v1/ask` endpoint'ine Türkçe sorular gönderilebilir.

## API Kullanımı

Soru sormak için:

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"Teslim aldığım ürünü geri göndermek için kaç gün içinde başvuru yapmalıyım?"}'
```

Örnek cevap:

```json
{
  "status": "answered",
  "answer": "Teslim tarihinden itibaren 30 gün içinde iade talebi oluşturabilirsiniz.",
  "sources": [
    {
      "filename": "02-iade-guncel.md",
      "title": "İade Prosedürü (Güncel)",
      "section": "İade süresi",
      "version": 2
    }
  ]
}
```

Dokümanlarda yeterli bilgi bulunmuyorsa API standart bir mesaj döndürür:

```json
{
  "status": "insufficient_information",
        "answer": "Bu soruyu yanıtlamak için mevcut dokümanlarda yeterli bilgi bulunmuyor.",
  "sources": []
}
```

## Evaluation

Projede normal, cevapsız ve çelişkili kaynak senaryolarını kapsayan 12 evaluation case bulunmaktadır.

Evaluation çalıştırmak için:

```bash
docker compose exec api python evaluation/run.py
```

Test senaryoları:

[`evaluation/cases.json`](evaluation/cases.json)

Son evaluation sonucu:

[`evaluation/results.md`](evaluation/results.md)

Evaluation sırasında beklenen durum, cevap içeriği ve kaynak versiyonu API'nin gerçek çıktısıyla karşılaştırılır.

## Notlar

- Bilgi kaynağı olarak `documents/` altındaki 10 kurgusal doküman kullanılmaktadır.
- Dokümanlar bölüm bazında embedding'e dönüştürülür ve pgvector üzerinde saklanır.
- Arama cosine distance kullanılarak yapılır.
- Yalnızca `active` durumundaki dokümanlar cevap üretiminde kullanılır.
- Eski iade prosedürleri `deprecated` olarak saklanır ancak retrieval sırasında kullanılmaz.
- Böylece güncel iade prosedürü eski prosedürlere göre önceliklendirilir.
- Yeterli bilgi bulunmayan sorularda `insufficient_information` döndürülür.
- Model tarafından döndürülen kaynaklar backend tarafında doğrulanır; geçerli bir kaynak olmadan başarılı cevap döndürülmez.
- Chat modeli için `temperature` değeri `0.2` olarak ayarlanmıştır.
- Proje küçük bir case study olduğu için vector index, Redis, queue, authentication ve UI eklenmemiştir.

## RAG Akışı

```text
Markdown Dokümanları
        ↓
Document Parser
        ↓
Embedding
        ↓
PostgreSQL + pgvector

Kullanıcı Sorusu
        ↓
Embedding
        ↓
Relevant Chunk Retrieval
        ↓
Ollama
        ↓
Cevap + Kaynaklar
```
