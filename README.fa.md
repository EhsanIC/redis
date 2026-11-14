<p align="center"><a href="README.md">English</a> | <b>فارسی</b></p>

<div dir="rtl">

# ساخت کلون Redis با پایتون

</div>

<p align="center">
  <a href="https://app.codecrafters.io/users/EhsanIC">
    <img src="https://backend.codecrafters.io/progress/redis/52edac4e-c367-4015-9ef5-4f44b1e9d729" alt="CodeCrafters progress" width="100%"/>
  </a>
</p>

<div dir="rtl">

یک کلونِ دست‌ساز از Redis در پایتون — بدون فریم‌ورک، فقط با سوکت‌های خام و یک event loop تک‌نخ که خودم نوشتم.

</div>

![Demo](docs/demo.gif)
<!-- [placeholder] یک دموی کوتاه را در مسیر docs/demo.gif قرار دهید -->

<div dir="rtl">

## ✨ امکانات

- [x] `PING` / `ECHO`
- [x] `SET` با انقضا (`EX` / `PX`) و `GET` با انقضای lazy (هنگام خواندن)
- [x] لیست‌ها: `RPUSH`، `LPUSH`، `LRANGE`، `LLEN`، `LPOP`
- [x] `BLPOP` — خواندنِ مسدودکننده با صف انتظارِ per-key و timeout
- [x] `TYPE`
- [x] کدگذاری و کدگشاییِ دستیِ پروتکل RESP
- [x] event loop تک‌نخ روی سوکت‌های non-blocking
- [ ] `XADD` / streams — در دست ساخت

## 🚀 شروع سریع

ابتدا سرور را اجرا کنید:

</div>

```bash
git clone https://github.com/EhsanIC/redis
cd redis
./your_program.sh
```

<div dir="rtl">

سپس در ترمینال دیگری:

</div>

```text
redis-cli
127.0.0.1:6379> SET greeting "hello"
OK
127.0.0.1:6379> GET greeting
"hello"
127.0.0.1:6379> RPUSH mylist a b c
(integer) 3
```

<div dir="rtl">

## ⚙️ چطور کار می‌کند

**پروتکل.** کلاینت‌ها با RESP2 صحبت می‌کنند. بایت‌های ورودی با جداکنندهٔ CRLF تفکیک می‌شوند تا نام دستور و آرگومان‌هایش استخراج شود؛ پاسخ‌ها هم با هلپرهای کوچکی به‌صورت دستی کدگذاری می‌شوند (bulk string، عدد صحیح، آرایه، simple string و خطا).

**همزمانی.** یک نخ (thread) واحد یک event loop غیرمسدودکننده را اجرا می‌کند: پذیرش اتصال‌های جدید، منقضی‌کردن کلاینت‌های مسدودی که زمان‌شان تمام شده، بررسی تک‌تک کلاینت‌های متصل برای دادهٔ ورودی، ارسال دستور به هندلر، و برگرداندن پاسخ. نه thread دارد و نه asyncio — دقیقاً همان ساختاری که خود Redis استفاده می‌کند.

**ذخیره‌سازی.** دیکشنری‌های سادهٔ پایتون، یکی برای هر نوع داده: رشته‌ها (`key → [value, expire_at]`)، لیست‌ها و streamها. انقضا به‌صورت lazy است: `GET` بررسی می‌کند آیا مهلت کلید تمام شده یا نه، و در آن صورت یک null bulk string برمی‌گرداند.

**دستورهای مسدودکننده.** `BLPOP` کلاینت را در یک صف انتظار per-key همراه با deadline ثبت می‌کند. وقتی `RPUSH` یا `LPUSH` عنصری اضافه می‌کنند، اولین منتظرِ صف بلافاصله سرو می‌شود؛ و اگر timeout برسد، حلقهٔ اصلی یک آرایهٔ null برمی‌گرداند.

### ساختار پروژه

</div>

```text
.
├── app/
│   ├── main.py        # نقطهٔ ورود برنامه
│   ├── server.py      # event loop: پذیرش / انقضا / بررسی / پاسخ
│   ├── commands.py    # dispatch دستورها و پیاده‌سازی‌ها
│   ├── helpers.py     # کدگذاری/کدگشایی RESP و ابزارهای انقضا
│   ├── waiters.py     # ثبت کلاینت‌های مسدودشده برای BLPOP
│   └── test.py
├── your_program.sh
└── codecrafters.yml
```

<div dir="rtl">

## 🧪 تست کردن

اجرای مجموعه‌تست‌های چالش:

</div>

```bash
codecrafters test
```

<div dir="rtl">

یا به‌صورت دستی با `redis-cli` و اتصال به `./your_program.sh` تست کنید. برای ارسال نهایی:

</div>

```bash
codecrafters submit
```

<div dir="rtl">

## 📚 چیزهایی که یاد گرفتم

- پروتکل RESP2، بایت به بایت
- چطور یک event loop تک‌نخ بدون thread از پس چندین کلاینت برمی‌آید
- اینکه Redis دستورهای مسدودکنندهٔ لیست را چطور پیاده می‌کند (صف انتظار + deadline)
- تفاوت انقضای lazy و active برای کلیدها
- تزریق وابستگی (dependency injection) — `main()` اجزا را می‌سازد و به `Server` پاس می‌دهد، نه اینکه `Server` خودش وابستگی‌هایش را بسازد
- <!-- [placeholder] هر چیز دیگری که شخصاً در این مسیر یاد گرفتید -->

## 🔧 چیزهایی که دوست دارم بهتر کنم

- حذف کد مرده و کامنت‌های آزمایشی — گیت تاریخچه را نگه می‌دارد
- استفاده از `is None` به‌جای `== None` (طبق PEP 8)
- یک هلپر واحد `resp_int(n)` به‌جای کدهای تکراریِ پاسخ عددی
- جایگزینی ساختار خام `[value, expire_at]` با یک dataclass کوچک
- یکدست‌سازی مقداردهی دیکشنری‌ها (استفادهٔ سراسری از `setdefault`)
- تکمیل `XADD`: اعتبارسنجی ID، تولید خودکار ID، چند جفت field-value و دستور `XRANGE`

## 🙏 قدردانی

این پروژه در چالش [Build Your Own Redis از CodeCrafters](https://codecrafters.io/challenges/redis) ساخته شده — اسکلت چالش از آنِ CodeCrafters است، **اما پیاده‌سازی کاملاً کار خودم است.**

</div>
