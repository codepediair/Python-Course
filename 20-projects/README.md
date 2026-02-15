---
title: راهنمای استفاده از پروژه ها
author: "مهدی رضایی"
created: 2026-02-15
updated: 2026-02-15
tags:
  - python
  - course
  - project
  - programming
description: راهنمای استفاده از پروژه ها به صورت عملی و بسیار آسان با کمک نرم افزار vscode .
---

# راهنمای استفاده از پروژه ها
### برای دریافت تمام پروژه ها از این [لینک](https://github.com/codepediair/Python-Course/releases) استفاده کنید.

پوشه دانلود شده را از حالت فشرده خارج کنید.
حالا پروژه ای که برای تمرین لازم دارید رو داخل vscode باز کنید

> در vscode از منوی terminal گزینه new terminal رو بزنید و دستور زیر رو وارد کنید
```bash
python -m venv env
```
> در سیستمم عامل ویندوز سپس این دستور را بزنید
``` powershell
./env/Scripts/activate
```
> در سیستم عامل لینوکس و مک این دستور را بزنید
``` bash
source ./env/bin/activate
```

### در نهایت پکیج های لازم رو نصب میکنیم
برایراحتی کار شما هر پکیج های لازم برای هر پروژه به صورت جداگانه قرار گرفته تا شما بتونید به راحتی اون ها رو نصب و استفاده کنید

```bash
pip install -r requirements.txt
```

