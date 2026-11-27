import marimo

__generated_with = "0.14.17"
app = marimo.App(width="full")


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۱ | کتابخانه‌ها و فضای رویدادهای نشست
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _():
    import marimo as mo
    import html
    from src.hardware import detect_hardware
    from src.event_log import EventLog

    event_log = EventLog()
    return EventLog, detect_hardware, event_log, html, mo


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۲ | پوستهٔ گرافیکی فارسی و راست‌چین
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(mo):
    theme = mo.Html(
        """
        <style>
        :root { color-scheme: dark; }
        body, .markdown, .marimo, .prose { font-family: Vazirmatn, IRANSans, Tahoma, sans-serif; }
        .hero {
          direction:rtl; text-align:right; padding:28px 30px; border-radius:22px;
          background:radial-gradient(circle at 12% 15%,#174b3c 0,transparent 38%),
                     linear-gradient(135deg,#111d1a,#101820 60%,#13251f);
          border:1px solid #245342; color:#eefcf5; margin-bottom:14px;
        }
        .hero h1 { margin:0 0 8px; font-size:28px; color:#f3fff9; }
        .hero p { margin:0; color:#a9c8b9; font-size:14px; }
        .eyebrow { color:#55e6a8; font-size:12px; letter-spacing:1px; margin-bottom:10px; }
        .stat-grid { direction:rtl; display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; }
        .stat { background:#111c1a; border:1px solid #263c35; border-radius:16px; padding:16px; min-height:86px; text-align:right; }
        .stat .label { color:#8ca99b; font-size:12px; margin-bottom:10px; }
        .stat .value { color:#e8fff4; font-size:20px; font-weight:700; overflow-wrap:anywhere; }
        .card { direction:rtl; text-align:right; background:#111a20; border:1px solid #293943; border-radius:16px; padding:18px; margin:8px 0; }
        .muted { color:#9bb0a8; font-size:13px; line-height:1.9; }
        .pill { display:inline-block; padding:4px 10px; border-radius:30px; background:#173d31; color:#75efb8; font-size:11px; margin:3px; }
        .warning { direction:rtl; text-align:right; padding:13px 16px; border-radius:12px; background:#332719; border:1px solid #70502a; color:#f5d6a4; line-height:1.9; }
        .terminal { direction:ltr; text-align:left; white-space:pre-wrap; overflow-wrap:anywhere; background:#080e12; color:#9cebc1; border:1px solid #263d35; border-radius:14px; padding:16px; font:12px/1.9 ui-monospace,SFMono-Regular,Consolas,monospace; }
        </style>
        """
    )
    header = mo.md(
        """
        <div class="hero">
          <div class="eyebrow">DEVVV • MARIMO CONTROL CENTER</div>
          <h1>داشبورد مانیتورینگ سخت‌افزار</h1>
          <p>نمایش وضعیت سیستم، منابع و رویدادهای نشست در یک Notebook فارسی</p>
        </div>
        """
    )
    safety = mo.md(
        """
        <div class="warning"><b>حالت فقط‌خواندنی</b><br>
        این داشبورد صرفاً اطلاعات پایهٔ سیستم را نمایش می‌دهد. هیچ نرم‌افزار استخراجی دانلود یا اجرا نمی‌شود،
        هیچ اتصال استخری ساخته نمی‌شود و هیچ پردازش پس‌زمینه‌ای آغاز نخواهد شد.</div>
        """
    )
    return header, safety, theme


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۳ | جمع‌آوری خواندنی مشخصات و میزان مصرف منابع
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(detect_hardware):
    hardware = detect_hardware()
    return (hardware,)


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۴ | ثبت رویداد آزمایشی برای بررسی رابط لاگ
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(event_log, mo):
    add_demo_log = mo.ui.run_button(label="ثبت رویداد آزمایشی")
    if add_demo_log.value:
        event_log.add("رویداد آزمایشی با موفقیت ثبت شد.")
    log_lines = event_log.lines()
    return add_demo_log, log_lines


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۵ | ساخت ترمینال نمایشی و گزارش رویدادها
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(hardware, html, log_lines, mo):
    cpu = hardware.get("cpu_percent")
    ram = hardware.get("ram_percent")
    cpu_text = f"{cpu:.1f}%" if isinstance(cpu, (int, float)) else "نامشخص"
    ram_text = f"{ram:.1f}%" if isinstance(ram, (int, float)) else "نامشخص"
    terminal_text = (
        "$ system-panel --status\n"
        "mode: read-only\n"
        "background_jobs: 0\n"
        f"cpu_usage: {cpu_text}\n"
        f"ram_usage: {ram_text}\n"
        "status: monitoring-only"
    )
    terminal = mo.md('<div class="terminal">' + html.escape(terminal_text) + "</div>")
    log_text = "\n".join(log_lines[-20:]) or "هنوز رویدادی ثبت نشده است."
    logs = mo.md('<div class="terminal">' + html.escape(log_text) + "</div>")
    return logs, terminal


# ─────────────────────────────────────────────────────────────────────────────
# سلول ۶ | چیدمان نهایی تب‌ها و کارت‌های داشبورد
# ─────────────────────────────────────────────────────────────────────────────
@app.cell
def _(add_demo_log, hardware, header, logs, mo, safety, terminal, theme):
    def stat(label, value):
        return f'<div class="stat"><div class="label">{label}</div><div class="value">{value}</div></div>'

    ram_total = f'{hardware["ram_gb"]} GB' if hardware.get("ram_gb") else "نامشخص"
    disk_free = f'{hardware["disk_free_gb"]} GB' if hardware.get("disk_free_gb") else "نامشخص"
    cpu_usage = f'{hardware["cpu_percent"]:.1f}%' if isinstance(hardware.get("cpu_percent"), (int, float)) else "نامشخص"
    ram_usage = f'{hardware["ram_percent"]:.1f}%' if isinstance(hardware.get("ram_percent"), (int, float)) else "نامشخص"
    gpu = "، ".join(hardware.get("gpu_vendors", [])) or "شناسایی نشد"
    overview = mo.vstack(
        [
            mo.md(
                '<div class="stat-grid">'
                + stat("سیستم‌عامل", hardware["os"])
                + stat("پردازنده", hardware["cpu"][:36] or "نامشخص")
                + stat("هستهٔ منطقی", hardware.get("logical_cores") or "نامشخص")
                + stat("حافظهٔ RAM", ram_total)
                + stat("مصرف CPU", cpu_usage)
                + stat("مصرف RAM", ram_usage)
                + stat("فضای آزاد", disk_free)
                + stat("گرافیک", gpu)
                + '</div>'
            ),
            mo.md(
                f'<div class="card"><h3>جزئیات محیط</h3>'
                f'<p>معماری: {hardware["architecture"]} · نسخهٔ پایتون: {hardware["python"]}</p>'
                f'<p>سازندهٔ CPU: {hardware.get("cpu_vendor", "نامشخص")}</p>'
                f'<p class="muted">{hardware["gpu_note"]}</p>'
                f'<span class="pill">فقط‌خواندنی</span><span class="pill">بدون پردازش پس‌زمینه</span></div>'
            ),
            safety,
        ]
    )
    activity = mo.vstack(
        [
            mo.md("## ترمینال وضعیت"),
            terminal,
            mo.md("## گزارش رویدادها"),
            logs,
            add_demo_log,
        ]
    )
    tabs = mo.ui.tabs({"نمای کلی": overview, "ترمینال و لاگ‌ها": activity})
    mo.vstack([theme, header, tabs])
    return


if __name__ == "__main__":
    app.run()
