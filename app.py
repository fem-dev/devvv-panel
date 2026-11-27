import marimo

__generated_with = "0.14.17"
app = marimo.App(width="full")


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۱ | واردکردن کتابخانه‌ها و ساخت فضای رویدادهای نشست
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _():
    import marimo as mo
    from src.hardware import detect_hardware
    from src.miner_catalog import MINERS, get_miner, recommend_miners
    from src.pool_config import PoolConfig, build_preview, validate_pool_config
    from src.event_log import EventLog
    from src.safe_runner import execution_status

    event_log = EventLog()
    return (
        event_log,
        EventLog,
        MINERS,
        PoolConfig,
        build_preview,
        detect_hardware,
        execution_status,
        get_miner,
        mo,
        recommend_miners,
        validate_pool_config,
    )


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۲ | پوستهٔ گرافیکی فارسی، RTL و تم تیره
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(mo):
    theme = mo.Html(
        """
        <style>
        :root { color-scheme: dark; }
        body, .markdown, .marimo, .prose { font-family: Vazirmatn, IRANSans, Tahoma, sans-serif; }
        .marimo { --primary: #24d18b; }
        .hero {
          direction: rtl; text-align: right; padding: 28px 30px; border-radius: 22px;
          background: radial-gradient(circle at 12% 15%, #174b3c 0, transparent 38%),
                      linear-gradient(135deg,#111d1a,#101820 60%,#13251f);
          border: 1px solid #245342; color: #eefcf5; margin-bottom: 14px;
        }
        .hero h1 { margin: 0 0 8px; font-size: 28px; color: #f3fff9; }
        .hero p { margin: 0; color: #a9c8b9; font-size: 14px; }
        .eyebrow { color:#55e6a8; font-size:12px; letter-spacing:1px; margin-bottom:10px; }
        .stat-grid { direction:rtl; display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:12px; }
        .stat {
          background:#111c1a; border:1px solid #263c35; border-radius:16px;
          padding:16px; min-height:84px; direction:rtl; text-align:right;
        }
        .stat .label { color:#8ca99b; font-size:12px; margin-bottom:10px; }
        .stat .value { color:#e8fff4; font-size:20px; font-weight:700; }
        .panel-card {
          direction:rtl; text-align:right; background:#111a20; border:1px solid #293943;
          border-radius:16px; padding:18px; margin:8px 0;
        }
        .panel-card h3 { color:#e8fff4; margin:0 0 8px; }
        .muted { color:#9bb0a8; font-size:13px; line-height:1.9; }
        .pill { display:inline-block; padding:4px 10px; border-radius:30px; background:#173d31; color:#75efb8; font-size:11px; margin:3px; }
        .warning {
          direction:rtl; text-align:right; padding:13px 16px; border-radius:12px;
          background:#332719; border:1px solid #70502a; color:#f5d6a4; line-height:1.9;
        }
        .terminal {
          direction:ltr; text-align:left; white-space:pre-wrap; overflow-wrap:anywhere;
          background:#080e12; color:#9cebc1; border:1px solid #263d35; border-radius:14px;
          padding:16px; font:12px/1.9 ui-monospace,SFMono-Regular,Consolas,monospace;
        }
        </style>
        """
    )
    header = mo.md(
        """
        <div class="hero">
          <div class="eyebrow">DEVVV • MARIMO CONTROL CENTER</div>
          <h1>پنل هوشمند مدیریت ماینر</h1>
          <p>بررسی سخت‌افزار، انتخاب نرم‌افزار سازگار و آماده‌سازی تنظیمات استخر — همه در همین Notebook</p>
        </div>
        """
    )
    safety = mo.md(
        """
        <div class="warning"><b>حالت امن فعال است</b><br>
        این نسخه فقط اطلاعات سیستم را می‌خواند و فرمان را برای بازبینی نمایش می‌دهد.
        هیچ ماینری دانلود یا اجرا نمی‌شود و هیچ پردازشی در پس‌زمینه شروع نخواهد شد.
        استخراج می‌تواند برق و گرمای زیادی مصرف کند؛ پیش از هر استفاده‌ای محدودیت‌های دستگاه را بررسی کنید.</div>
        """
    )
    return header, safety, theme


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۳ | تشخیص خواندنی سخت‌افزار و وضعیت محیط
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(detect_hardware):
    hardware = detect_hardware()
    return (hardware,)


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۴ | انتخاب ماینر و پیشنهاد بر اساس سخت‌افزار
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(MINERS, hardware, mo, recommend_miners):
    gpu_vendors = tuple(hardware.get("gpu_vendors", []))
    recommendations = recommend_miners(gpu_vendors, has_cpu=True)
    miner_options = [miner.name for miner in MINERS]
    miner_select = mo.ui.dropdown(
        options=miner_options,
        value="XMRig",
        label="نرم‌افزار موردنظر",
    )
    recommended_names = {miner.name for miner in recommendations}
    catalog_cards = []
    for miner in MINERS:
        badge = "پیشنهاد سازگار" if miner.name in recommended_names else "نیازمند بررسی"
        algos = "، ".join(miner.algorithms)
        hw = "، ".join(miner.hardware)
        catalog_cards.append(
            mo.md(
                f"""
                <div class="panel-card">
                  <h3>{miner.name} <span class="pill">{badge}</span></h3>
                  <div class="muted">{miner.description}</div>
                  <p><b>الگوریتم‌ها:</b> {algos}</p>
                  <p><b>سخت‌افزار:</b> {hw}</p>
                  <p class="muted">{miner.notes}</p>
                  <a href="{miner.official_url}" target="_blank" rel="noopener noreferrer">منبع رسمی پروژه ↗</a>
                </div>
                """
            )
        )
    catalog_view = mo.vstack(catalog_cards)
    return catalog_view, miner_select, recommendations, recommended_names


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۵ | فرم تنظیمات Pool و اعتبارسنجی ورودی‌ها
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(mo):
    pool_host = mo.ui.text(label="آدرس استخر (بدون https://)", value="pool.example.org")
    pool_port = mo.ui.text(label="پورت", value="3333")
    wallet = mo.ui.text(label="آدرس کیف پول / شناسه", value="")
    worker = mo.ui.text(label="نام Worker", value="worker01")
    pool_password = mo.ui.text(label="رمز استخر (اختیاری)", value="x", kind="password")
    algorithm = mo.ui.dropdown(
        options=["RandomX", "KawPow", "Autolykos", "Etchash", "Equihash"],
        value="RandomX",
        label="الگوریتم",
    )
    build_button = mo.ui.run_button(label="اعتبارسنجی و ساخت پیش‌نمایش")
    return (
        algorithm,
        build_button,
        pool_host,
        pool_password,
        pool_port,
        wallet,
        worker,
    )


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۶ | ساخت فرمان نمونه؛ متن نمایشی است و اجرا نمی‌شود
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(
    event_log,
    PoolConfig,
    algorithm,
    build_button,
    build_preview,
    get_miner,
    miner_select,
    pool_host,
    pool_password,
    pool_port,
    validate_pool_config,
    wallet,
    worker,
):
    preview_text = "هنوز پیش‌نمایشی ساخته نشده است."
    validation_errors = []
    if build_button.value:
        try:
            config = PoolConfig(
                host=pool_host.value.strip(),
                port=int(pool_port.value),
                wallet=wallet.value.strip(),
                worker=worker.value.strip(),
                password=pool_password.value or "x",
                algorithm=algorithm.value,
            )
            validation_errors = validate_pool_config(config)
            selected_miner = get_miner(miner_select.value)
            if selected_miner and algorithm.value not in selected_miner.algorithms:
                validation_errors.append(
                    f"الگوریتم {algorithm.value} در فهرست پشتیبانی {selected_miner.name} نیست."
                )
            if validation_errors:
                event_log.add("اعتبارسنجی تنظیمات ناموفق بود.", "WARNING")
            else:
                preview_text = build_preview(config, miner_select.value)
                event_log.add("تنظیمات معتبر است؛ پیش‌نمایش عمومی فرمان ساخته شد.")
        except (TypeError, ValueError):
            validation_errors = ["پورت باید یک عدد صحیح باشد."]
            event_log.add("مقدار پورت قابل تبدیل به عدد نیست.", "ERROR")
    else:
        event_log.add("فرم آماده است؛ برای اعتبارسنجی آن را ارسال کنید.")
    return event_log, preview_text, validation_errors


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۷ | ترمینال نمایشی، لاگ‌ها و وضعیت اجرای کنترل‌شده
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(execution_status, event_log, mo, preview_text, validation_errors):
    import html

    status = execution_status()
    if validation_errors:
        validation_view = mo.md(
            "**خطاهای اعتبارسنجی:**\n" + "\n".join(f"- {item}" for item in validation_errors)
        )
    elif preview_text != "هنوز پیش‌نمایشی ساخته نشده است.":
        validation_view = mo.md("تنظیمات معتبر هستند. فرمان زیر فقط یک قالب عمومی برای بازبینی است.")
    else:
        validation_view = mo.md("فرم را تکمیل کنید و دکمهٔ اعتبارسنجی را بزنید.")

    terminal_content = (
        "$ miner-panel --status\n"
        f'mode: {status["mode"]}\n'
        f'running: {str(status["running"]).lower()}\n'
        f'message: {status["message"]}\n\n'
        "$ command-preview\n"
        f"{preview_text}"
    )
    terminal = mo.md('<div class="terminal">' + html.escape(terminal_content) + "</div>")
    log_content = "\n".join(event_log.lines()[-15:]) or "هنوز رویدادی ثبت نشده است."
    logs = mo.md('<div class="terminal">' + html.escape(log_content) + "</div>")
    return logs, status, terminal, validation_view


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۸ | چیدمان نهایی تب‌ها و داشبورد
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(
    algorithm,
    catalog_view,
    header,
    hardware,
    logs,
    miner_select,
    mo,
    pool_host,
    pool_password,
    pool_port,
    safety,
    status,
    terminal,
    theme,
    validation_view,
    wallet,
    worker,
    build_button,
):
    def stat(label, value):
        return f'<div class="stat"><div class="label">{label}</div><div class="value">{value}</div></div>'

    ram = f'{hardware["ram_gb"]} GB' if hardware.get("ram_gb") else "نامشخص"
    cores = str(hardware.get("logical_cores") or "نامشخص")
    disk = f'{hardware["disk_free_gb"]} GB' if hardware.get("disk_free_gb") else "نامشخص"
    overview = mo.vstack(
        [
            mo.md(
                '<div class="stat-grid">'
                + stat("سیستم‌عامل", hardware["os"])
                + stat("پردازنده", hardware["cpu"][:34])
                + stat("هستهٔ منطقی", cores)
                + stat("حافظهٔ RAM", ram)
                + stat("فضای آزاد", disk)
                + stat("وضعیت ماینر", "متوقف / ایمن")
                + '</div>'
            ),
            mo.md(
                f'<div class="panel-card"><h3>مشخصات محیط</h3>'
                f'<p>معماری: {hardware["architecture"]} · پایتون: {hardware["python"]}</p>'
                f'<p>سازندهٔ CPU: {hardware.get("cpu_vendor", "نامشخص")}</p>'
                f'<p class="muted">{hardware["gpu_note"]}</p></div>'
            ),
            safety,
        ]
    )
    setup = mo.vstack(
        [
            mo.md("## تنظیمات استخر"),
            miner_select,
            pool_host,
            pool_port,
            wallet,
            worker,
            pool_password,
            algorithm,
            build_button,
            validation_view,
            terminal,
            mo.md("### گزارش رویدادها"),
            logs,
        ]
    )
    tabs = mo.ui.tabs(
        {
            "نمای کلی": overview,
            "کاتالوگ ماینرها": catalog_view,
            "تنظیمات و ترمینال": setup,
        }
    )
    mo.vstack([theme, header, tabs])
    return


if __name__ == "__main__":
    app.run()
