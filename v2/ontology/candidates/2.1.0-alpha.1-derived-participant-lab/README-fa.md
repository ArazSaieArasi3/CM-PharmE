# آزمایش گزینه‌های مشارکت‌کننده و نیازمندی‌های مستقل

پیشنهاد C در مقایسهٔ محدود فعلاً مناسب‌تر است، اما یک قرارداد رگرسیون را تغییر می‌دهد؛ پذیرش علمی انجام نشده است. نسخهٔ مبنا و چهار دامنه حفظ شده‌اند. PR305 همچنان پیش‌نویس است.

- نتیجهٔ مقایسه و تصمیم‌های باز: [decision-report-fa.md](decision-report-fa.md)
- تمام ۲۳ کار، تمام ایشوهای باز و درصدها: [work-status-fa.md](work-status-fa.md)
- ۱۶ نیاز پیشنهادی از منابع اصلی: [source-requirements-fa.md](source-requirements-fa.md)
- نقطهٔ ادامهٔ ماشینی: [continuation-checkpoint.json](continuation-checkpoint.json)
- اعداد قابل ممیزی: [summary.json](summary.json)

## بازتولید

از همین پوشه اجرا شود. `PYTHON` باید Python دارای rdflib 7.6.0، pyshacl 0.30.1 و owlready2 0.49 باشد. مسیرهای پارامترها را مطابق نصب خود تعیین کنید؛ Java 17، ECJ 3.39.0 و وابستگی‌های آرشیو لازم‌اند. Node با ontouml-js 1.0.0، schema 1.0.2، ajv 8.17.1 و ajv-formats 3.0.1 استفاده شده است.

```bash
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" build_lab.py "$ONTOUML_NODE_MODULES"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" run_legacy.py "$OLED_ARCHIVE" "$ECJ_JAR"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" run_semantics.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" run_temporal.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" build_requirements.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" finalize_lab.py
```

`OLED_ARCHIVE` باید نسخهٔ تغییرنیافتهٔ `42b926f6c2859dc87e49a96b8482eae28d02e7d5` باشد. شرح تهیهٔ وابستگی و محدودیت تبدیل در بستهٔ پیشین `2.1.0-alpha.1-detector-calibration` موجود است. `run_semantics.py --shacl-only` فقط شاهدهای SHACL را بازاجرا می‌کند و فایل HermiT قبلی را دست نمی‌زند.

خروج موفق اسکریپت‌ها یعنی مشاهدات با انتظارهای ازپیش‌بیان‌شده تطبیق دارند؛ به معنی پذیرش طرح یا عبور gate نیست. مقدار `regression_gate` هنوز `BLOCKED_PENDING_SEMANTIC_DECISION` است. خروجی اولیهٔ ۸۸/۸۹ محفوظ است و انتظار قدیمی تغییر نکرده است. ریزنر ۱۲/۱۲ و آزمون زمانی ۱۰/۱۰ صرفاً محدودهٔ خود را می‌پوشانند.

قواعد materialization و سه profile در `run_semantics.py` تعریف شده‌اند. فایل‌های `proposal-*.owl-delta.ttl` مستقل از قواعد عملیاتی، معنای کامل تصویر مشتق‌شده را بیان نمی‌کنند. فقط سه قاعدهٔ منتخب OCL بررسی شده؛ full validator، all modern nature و اجرای ۲۰ آشکارساز روی کل مدل انجام نشده است.

`repository-evidence.json` اسنپ‌شات ۳۰ ایشوی باز و شکست‌های CI برای head پیشین 34d23eb است؛ ادعای موفقیت CI برای commit این بسته ندارد. برای تکرار فقط آزمایش‌ها نیازی به تغییر آن اسنپ‌شات تاریخی نیست.

تمام خروجی‌های JSON، Turtle، Java و Python این پوشه آزمایشی‌اند؛ هیچ فایل انتالوژی قبلی و هیچ موتور رسمی اصلاح نشده است. هش فایل‌ها در `file-manifest.json` ثبت شده است.
