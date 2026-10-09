# بستهٔ آزمایشی PROV، دامنهٔ هدف و NDC

این بسته از `bdc0a00` ادامه می‌دهد. نسخهٔ native و قرارداد C تغییر نکرده‌اند. تمام نتایج پیشنهادهای قابل داوری‌اند؛ PR305 همچنان draft است.

سه خروجی: نگاشت جهت‌دار PROV، هفت سناریوی مستقل برای دو والد باز، و نگاشت پنج رکورد واقعی NDC به هفت مشاهدهٔ بسته‌بندی. گزارش تصمیم در `decision-report-fa.md` و همهٔ ۲۳ کار و ۳۰ ایشوی باز در `work-status-fa.md` ثبت شده است.

بازتولید در محیط دارای Python، Java، rdflib، pyshacl و owlready2 (نسخه‌ها در runtime.json):

```bash
export PYTHONDONTWRITEBYTECODE=1
python run_reasoner.py
python run_targets.py
python run_ndc.py
python run_regression.py
python audit_fields.py
python finalize.py
```

دستورات را در همین پوشه اجرا کنید. آزمون‌ها از snapshotهای ذخیره‌شده استفاده می‌کنند؛ فراخوانی دوبارهٔ API الزاماً همان پنج رکورد را نمی‌دهد. URL، Accept، زمان، حجم و checksum بازیابی در sources ثبت شده‌اند؛ درخواست PROV با `Accept: text/turtle` و NDC با `Accept: application/json` انجام شد.

`sources/prov-o-20130430.ttl` فایل اصلی و دست‌نخوردهٔ W3C است. پروفایل استدلال فقط دو اعلان AnnotationProperty متعارض را حذف می‌کند و تمام سه‌تایی‌های دیگر را نگه می‌دارد؛ جزئیات در prov-adapter.json است. این تبدیل مجوز ادعای «تأیید کامل PROV یا OWL2 DL» نیست. PROV-CONSTRAINTS اجرا نشده است. شکست خام ۳۵/۳۶ و نتایج اولیهٔ واسطی حفظ شده‌اند.

دادهٔ NDC فقط برای پژوهش نگاشت است. labeler، دستهٔ بازاریابی و تاریخ‌ها ادعاهای منبع‌اند؛ مجوز یا هویت مستقل را ثابت نمی‌کنند. شناسه‌های labeler در سطح ردیف منبع باقی مانده‌اند و نام مشابه باعث ادغام نشده است. تاریخ محصول و بسته مجزا است. نمونهٔ قبلی ۷۶۸ ردیفی فقط عدم پسرفت را بررسی می‌کند.

منابع رسمی: [PROV-O 2013](https://www.w3.org/TR/2013/REC-prov-o-20130430/)، [نسخهٔ Turtle پین‌شده](https://www.w3.org/ns/prov-o-20130430)، [OWL2 typing](https://www.w3.org/TR/owl-syntax/#Typing_Constraints_of_OWL_2_DL)، [ICH Q9(R1)، اصلاح ۲۰۲۵](https://database.ich.org/sites/default/files/ICH_Q9%28R1%29_Guideline_Step4_2025_0115.pdf)، [openFDA NDC](https://open.fda.gov/apis/drug/ndc/)، [FDA NDC](https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory).

حقوق فایل PROV متعلق به W3C و مؤلفان آن است؛ نسخهٔ منبع دست‌نخورده حفظ شده و تبدیل آزمایشی از اصل جداست. شرایط دادهٔ openFDA در meta پاسخ اصلی باقی مانده است. ICH فقط پشتوانهٔ بررسی زمینه‌های متنوع ریسک است؛ سناریوهای این بسته ساختهٔ پژوهش حاضرند و تأیید ICH محسوب نمی‌شوند.
