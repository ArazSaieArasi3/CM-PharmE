# CM-PharmE v2.1 — آزمایش رجیستری و زمینهٔ گزارش‌دهی

بستهٔ مستقل و نپذیرفته، ادامه از `a83471c`. چهار دامنهٔ محل بحث حفظ می‌شوند. هیچ فایل انتالوژی قبلی تغییر نکرده است.

- [گزارش تصمیم و محدودیت‌ها](decision-report-fa.md)
- [تطبیق ۱۶ پیشنهاد با ۲۴ نیاز قبلی](reconciliation-fa.md)
- [تمام ۲۳ کار، ایشوهای باز و درصدها](work-status-fa.md)
- [خلاصهٔ ماشینی](summary.json) و [نقطهٔ ادامه](continuation-checkpoint.json)
- [ردیابی نیاز به شاهد و تصمیم](traceability.json)

برای بازتولید از همین پوشه با Python دارای rdflib 7.6.0، pyshacl 0.30.1 و owlready2 0.49 اجرا شود؛ Java 17 برای HermiT لازم است:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" build_contracts.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" run_lab.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" run_reasoner.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" audit_mapping.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" run_real_regression.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" finalize_lab.py
```

`run_lab.py --no-regression` فقط شاهدهای جدید را اجرا می‌کند. `run_reasoner.py` با نام caseهای مشخص فقط همان موارد را بازاجرا و سایر نتایج را حفظ می‌کند؛ اجرای بدون آرگومان کل ۱۳ مورد را بازسازی می‌کند. برای بازتولید کامل از دستورهای بالا استفاده کنید.

نتیجهٔ موفق اسکریپت‌ها، پذیرش علمی نیست. ۱۶ نیاز، پوشش مثبت/منفی محدود دارند؛ ۳۹ عنوان کاری به معنی استخراج جامع همهٔ نیازها نیست. قواعد `p:` پروفایل داده و پاسخ‌گویی‌اند و هنوز به native نگاشت کامل ندارند. پرسش‌ها فقط روی گراف ارائه‌شده اجرا می‌شوند؛ شاهدهای HermiT جداگانه برای ادعاهای محدود عدم‌استنتاج آمده‌اند.

پروتوتایپ applicability در محدودهٔ اطلاعات ورودی و پس از کنترل profile قابل استفاده است؛ ناقص‌بودن اطلاعات می‌تواند UNKNOWN بدهد. این خروجی تشخیص واقعی انطباق حقوقی نیست. namespace PROV در fixtureها به معنی import یا تأیید کامل استاندارد PROV نیست.

خروجی ناموفق اول، به‌علاوهٔ fixtureهای فاقد mandate، برای ممیزی نگه داشته شده است. همهٔ داده‌های جدید مصنوعی‌اند؛ نمونهٔ واقعی قدیمی فقط عدم پسرفت را می‌سنجد. اختلاف قرارداد C و شکست W6 همچنان باز است.
