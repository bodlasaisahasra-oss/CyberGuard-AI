import streamlit as st
import re
import base64
import uuid
from pathlib import Path

from AI import ask_ai


APP_DIR = Path(__file__).parent


def build_dashboard_component():
        html_source = (APP_DIR / "index.html").read_text(encoding="utf-8")
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html_source, flags=re.IGNORECASE | re.DOTALL)
        if body_match is None:
                raise ValueError("index.html must contain a body element")

        html = body_match.group(1)
        robot_art = base64.b64encode(
                (APP_DIR / "assets" / "cyber-robot.svg").read_bytes()
        ).decode("ascii")
        html = html.replace(
                'src="assets/cyber-robot.svg"',
                f'src="data:image/svg+xml;base64,{robot_art}"',
        )

        css = (APP_DIR / "style.css").read_text(encoding="utf-8")
        css += """
.chat-messages {
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
    border: 1px solid rgba(133, 171, 194, .14);
    border-radius: 12px;
    background-color: #0b1119;
    background-image: radial-gradient(ellipse at 18% 0%, rgba(50, 147, 144, .13), transparent 42%), repeating-linear-gradient(0deg, transparent 0 31px, rgba(173, 201, 214, .025) 32px);
}
.chat-welcome { width: 100%; margin: auto; }
.message {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    width: fit-content;
    max-width: min(82%, 680px);
    animation: message-arrive .24s ease-out both;
}
.assistant-message { align-self: flex-start; }
.user-message { align-self: flex-end; flex-direction: row-reverse; }
.message-avatar {
    display: grid;
    flex: 0 0 30px;
    place-items: center;
    width: 30px;
    height: 30px;
    border: 1px solid rgba(84, 216, 200, .28);
    border-radius: 10px;
    background: #102a2b;
    color: #8ce0cf;
    font-size: 10px;
    font-weight: 700;
}
.user-message .message-avatar { border-color: rgba(111, 145, 255, .3); background: #172342; color: #b5c6ff; }
.message-body { min-width: 0; max-width: 100%; }
.message-meta { display: flex; align-items: center; gap: 9px; margin: 0 3px 5px; color: #8391a4; font-size: 10px; }
.message-meta strong { color: #c4d0da; font-weight: 600; }
.user-message .message-meta { justify-content: flex-end; }
.message-content {
    padding: 12px 15px;
    border: 1px solid rgba(84, 216, 200, .13);
    border-radius: 4px 13px 13px 13px;
    background: linear-gradient(145deg, rgba(21, 44, 46, .96), rgba(17, 30, 38, .98));
    color: #e3eceb;
    overflow-wrap: anywhere;
}
.user-message .message-content {
    border-color: rgba(111, 145, 255, .2);
    border-radius: 13px 4px 13px 13px;
    background: linear-gradient(145deg, #1d3158, #172542);
    color: #f0f3ff;
}
.message-content p { margin: 0 0 8px; line-height: 1.65; }
.message-content p:last-child { margin-bottom: 0; }
.message-content ul, .message-content ol { display: grid; gap: 7px; margin: 8px 0; padding-left: 20px; line-height: 1.6; }
.message-content li { padding-left: 3px; }
.assistant-message .message-content li::marker { color: #6bcfbd; }
.user-message .message-content p { white-space: pre-wrap; }
.pending-message .message-content { min-width: 72px; }
.top-avatar { cursor: pointer; transition: border-color .18s, background .18s, transform .18s; }
.top-avatar:hover, .top-avatar:focus-visible { border-color: var(--cyan); background: #16323a; transform: translateY(-1px); }
.profile-trigger { display: flex; align-items: center; gap: 3px; padding: 0; border: 0; background: transparent; color: var(--muted); cursor: pointer; }
.profile-trigger:hover .top-avatar, .profile-trigger:focus-visible .top-avatar { border-color: var(--cyan); background: #16323a; }
.profile-chevron { width: 13px; height: 13px; }
.login-layout { display: grid; grid-template-columns: minmax(230px, 1fr) minmax(320px, 440px); align-items: center; gap: 56px; max-width: 1000px; min-height: calc(100vh - 190px); margin: 0 auto; }
.login-intro .about-mark { margin-bottom: 24px; }
.login-intro h1 { margin: 14px 0 10px; font-family: 'Space Grotesk', sans-serif; font-size: 36px; }
.login-intro > p, .login-gate > p { color: var(--muted); line-height: 1.7; }
.login-panel { padding: 28px; }
.login-gate { display: grid; justify-items: start; gap: 12px; }
.login-gate h2, .login-form h2 { margin: 5px 0 0; font-family: 'Space Grotesk', sans-serif; font-size: 21px; }
.login-form { display: grid; gap: 10px; }
.login-form[hidden], .login-gate[hidden] { display: none; }
.login-form label { margin-top: 5px; color: #cbd5e3; font-size: 12px; font-weight: 600; }
.login-form input { width: 100%; min-height: 44px; padding: 0 12px; border: 1px solid var(--line-strong); border-radius: 8px; outline: none; background: #0b111b; color: var(--text); }
.login-form input:focus { border-color: var(--cyan); box-shadow: 0 0 0 3px rgba(84, 216, 232, .1); }
.login-form .primary-button { justify-self: start; margin-top: 8px; }
.password-field { position: relative; }
.password-field input { padding-right: 46px; }
.password-visibility { position: absolute; top: 5px; right: 5px; display: grid; place-items: center; width: 34px; height: 34px; border: 0; border-radius: 6px; background: transparent; color: var(--muted); cursor: pointer; }
.password-visibility:hover { background: var(--panel-2); color: var(--text); }
.password-visibility svg { width: 17px; height: 17px; }
.login-status { min-height: 18px; margin: 0; color: var(--amber); font-size: 11px; line-height: 1.6; }
.login-demo-note { margin: 0; color: var(--subtle); font-size: 10px; line-height: 1.6; }
.plans-section { max-width: 1000px; margin: 26px auto 40px; }
.plans-heading { margin-bottom: 16px; }
.plans-heading h2 { margin: 5px 0; font-family: 'Space Grotesk', sans-serif; font-size: 21px; }
.plans-heading p, .plan-card > p:not(.plan-price) { color: var(--muted); font-size: 11px; line-height: 1.55; }
.plans-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.plan-card { display: flex; flex-direction: column; align-items: flex-start; min-height: 250px; padding: 17px; border: 1px solid var(--line); border-radius: 10px; background: var(--panel); color: var(--text); }
.plan-card.plan-featured { border-color: rgba(84, 216, 232, .38); background: linear-gradient(150deg, rgba(18, 48, 53, .5), var(--panel) 65%); }
.plan-card.selected { box-shadow: 0 0 0 2px rgba(84, 216, 232, .25); }
.plan-kind { color: var(--cyan); font-size: 9px; font-weight: 700; letter-spacing: 1px; }
.plan-card h3 { margin: 8px 0 0; font-family: 'Space Grotesk', sans-serif; font-size: 17px; }
.plan-price { margin: 5px 0; font-size: 13px; font-weight: 700; }
.plan-card ul { display: grid; gap: 7px; margin: 6px 0 16px; padding-left: 17px; color: var(--muted); font-size: 10px; line-height: 1.4; }
.plan-card li::marker { color: var(--cyan); }
.plan-card button { margin-top: auto; }
.plan-status { min-height: 18px; margin: 10px 0 0; color: var(--muted); font-size: 10px; }
.theme-switch { display: flex; gap: 5px; padding: 4px; border: 1px solid var(--line); border-radius: 9px; background: rgba(128, 150, 164, .08); }
.theme-choice { display: grid; place-items: center; width: 36px; height: 34px; border: 1px solid transparent; border-radius: 6px; background: transparent; color: var(--muted); cursor: pointer; }
.theme-choice svg { width: 16px; height: 16px; }
.theme-choice[aria-pressed="true"] { border-color: var(--line-strong); background: var(--panel-2); color: var(--text); }
.notification-wrap { position: relative; }
.notification-count { position: absolute; top: -4px; right: -4px; display: grid; place-items: center; min-width: 15px; height: 15px; padding: 0 3px; border: 1px solid var(--bg); border-radius: 9px; background: #d95b69; color: #fff; font-size: 8px; font-weight: 700; }
.notification-count[hidden] { display: none; }
.notification-panel { position: absolute; z-index: 30; top: calc(100% + 10px); right: -46px; width: min(360px, calc(100vw - 30px)); padding: 15px; border: 1px solid var(--line-strong); border-radius: 12px; background: var(--panel); color: var(--text); box-shadow: 0 18px 50px rgba(0, 0, 0, .3); }
.notification-panel[hidden] { display: none; }
.notification-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; padding: 3px 2px 12px; border-bottom: 1px solid var(--line); }
.notification-heading > div { display: grid; gap: 4px; }
.notification-heading strong { font-size: 14px; }
.notification-heading small, .notification-list small { color: var(--muted); font-size: 10px; }
.notification-heading .text-button { padding: 2px 0; color: var(--cyan); font-size: 10px; }
.notification-list { display: grid; gap: 2px; margin: 5px 0 0; padding: 0; list-style: none; }
.notification-list li { display: grid; grid-template-columns: 30px minmax(0, 1fr); gap: 10px; padding: 11px 7px; border-radius: 8px; }
.notification-list li.unread { background: rgba(84, 216, 232, .07); }
.notification-icon { display: grid; place-items: center; width: 28px; height: 28px; border: 1px solid var(--line); border-radius: 8px; color: var(--cyan); }
.notification-icon svg { width: 15px; height: 15px; }
.notification-list li > div { min-width: 0; }
.notification-list li strong { font-size: 11px; }
.notification-list li p { margin: 4px 0; color: var(--muted); font-size: 10px; line-height: 1.5; }
:host(.theme-light) .notification-panel { background: #fff; color: var(--text); box-shadow: 0 18px 50px rgba(17, 38, 45, .18); }
.assessment-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-bottom: 18px; }
.assessment-grid[hidden], .quiz-shell[hidden] { display: none; }
.assessment-card { position: relative; display: grid; align-content: start; gap: 7px; min-height: 98px; padding: 14px; border: 1px solid var(--line); border-radius: 10px; background: var(--panel); color: var(--text); text-align: left; cursor: pointer; transition: border-color .16s, transform .16s, background .16s; }
.assessment-card:hover, .assessment-card:focus-visible { transform: translateY(-2px); border-color: var(--cyan); background: var(--panel-2); }
.assessment-number { color: var(--cyan); font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; }
.assessment-card strong { padding-right: 20px; font-size: 12px; }
.assessment-card small { color: var(--muted); font-size: 10px; }
.assessment-arrow { position: absolute; top: 13px; right: 12px; color: var(--subtle); }
.assessment-arrow svg { width: 15px; height: 15px; }
.quiz-topline .text-button { display: inline-flex; align-items: center; gap: 5px; }
.quiz-topline .text-button svg { width: 14px; height: 14px; }
.guide-body { display: grid; gap: 12px; margin: 16px 0; color: var(--muted); line-height: 1.7; }
.guide-body p { margin: 0; }
.guide-references { margin: 16px 0; padding-top: 13px; border-top: 1px solid var(--line); }
.guide-references h3 { margin: 0 0 8px; font-size: 12px; }
.guide-references ul { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }
.guide-references a { display: inline-flex; align-items: center; gap: 6px; color: var(--cyan); font-size: 11px; line-height: 1.5; text-decoration: none; }
.guide-references a:hover { text-decoration: underline; }
.guide-references a svg { width: 13px; height: 13px; }
.secure-note { width: 100%; color: var(--text); text-align: left; cursor: pointer; transition: border-color .18s, background .18s, box-shadow .18s; }
.secure-note:hover, .secure-note:focus-visible, .secure-note.active { border-color: rgba(84, 216, 232, .5); background: linear-gradient(115deg, rgba(34, 116, 142, .2), rgba(95, 76, 167, .12)); box-shadow: 0 0 18px rgba(49, 172, 209, .12); }
.secure-note.active .secure-spark { color: var(--cyan); }
:host(.hub-active) .main-footer { display: none; }
.stay-aware-view.active { animation: hub-view-enter .35s ease-out both; }
.hub-page { position: relative; display: grid; gap: 24px; padding: 4px 1px 18px; background: radial-gradient(ellipse at 16% 2%, rgba(36, 146, 168, .08), transparent 30%), radial-gradient(ellipse at 90% 18%, rgba(106, 82, 180, .07), transparent 28%); container: stay-aware / inline-size; }
.hub-dashboard-grid { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(300px, .8fr); align-items: start; gap: 17px; }
.hub-primary-column, .hub-side-column, .hub-bottom-main, .hub-bottom-side { display: grid; align-content: start; gap: 16px; min-width: 0; }
.hub-hero { position: relative; display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(170px, .7fr); align-items: center; min-height: 302px; overflow: hidden; padding: 26px 28px; border-color: rgba(83, 171, 214, .2); background: radial-gradient(ellipse at 80% 50%, rgba(36, 173, 191, .16), transparent 34%), linear-gradient(132deg, rgba(12, 28, 47, .98), rgba(18, 20, 42, .96)); }
.hub-hero:after { position: absolute; inset: 0; pointer-events: none; border-radius: inherit; background: repeating-linear-gradient(0deg, transparent 0 42px, rgba(119, 172, 207, .025) 43px), repeating-linear-gradient(90deg, transparent 0 42px, rgba(119, 172, 207, .025) 43px); content: ''; }
.hub-hero-copy { position: relative; z-index: 1; max-width: 570px; }
.hub-hero-copy h1 { margin: 17px 0 10px; font-family: 'Space Grotesk', sans-serif; font-size: 36px; line-height: 1.14; }
.hub-hero-copy h1 > span:first-child { color: #edf7ff; }
.hub-hero-copy h1 strong { background: linear-gradient(95deg, #53e4ed, #86aaff 55%, #bf95ff); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hub-hero-shield { font-size: 25px; }
.hub-hero-copy h2 { margin: 0 0 9px; color: #d2e5f2; font-size: 14px; font-weight: 600; }
.hub-hero-copy > p { max-width: 490px; margin: 0; color: #9eafc2; font-size: 12px; line-height: 1.7; }
.hub-pill-row { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 18px; }
.hub-pill-row span { padding: 7px 10px; border: 1px solid rgba(130, 194, 214, .18); border-radius: 20px; background: rgba(150, 206, 221, .07); color: #c9e8f1; font-size: 10px; }
.hub-shield-scene { position: relative; display: grid; place-items: center; min-height: 235px; }
.hub-shield-orbit { position: absolute; width: 184px; aspect-ratio: 1; border: 1px solid rgba(73, 205, 235, .14); border-radius: 50%; box-shadow: 0 0 36px rgba(27, 168, 210, .1), inset 0 0 36px rgba(27, 168, 210, .08); }
.hub-shield-mark { position: relative; display: grid; place-items: center; width: 130px; height: 150px; color: #5bddeb; filter: drop-shadow(0 0 23px rgba(69, 205, 243, .48)); animation: hub-float 5s ease-in-out infinite; }
.hub-shield-mark > svg:first-child { position: absolute; width: 130px; height: 145px; stroke-width: 1.05; fill: rgba(46, 177, 209, .1); }
.hub-shield-mark > svg:last-child { z-index: 1; width: 43px; height: 43px; stroke-width: 1.5; }
.hub-shield-spark { position: absolute; width: 5px; height: 5px; border-radius: 50%; background: #a9f7ff; box-shadow: 0 0 15px #44dff1; }
.hub-spark-one { top: 23%; right: 20%; }.hub-spark-two { bottom: 24%; left: 14%; width: 3px; height: 3px; }
.hub-assistant { display: grid; grid-template-columns: 150px minmax(0, 1fr); align-items: center; gap: 16px; min-height: 170px; overflow: hidden; padding: 13px 19px; border-color: rgba(124, 128, 226, .19); background: linear-gradient(105deg, rgba(13, 28, 43, .98), rgba(25, 21, 48, .92)); }
.hub-robot-wrap { position: relative; display: grid; place-items: center; min-height: 135px; }
.hub-robot-wrap img { width: 142px; height: 135px; object-fit: contain; animation: hub-float 6s ease-in-out infinite; }
.hub-robot-shield { position: absolute; z-index: 1; top: 14px; right: 7px; display: grid; place-items: center; width: 31px; height: 31px; border: 1px solid rgba(79, 216, 232, .5); border-radius: 10px; background: #102c39; color: #69e2ef; box-shadow: 0 0 17px rgba(52, 206, 237, .25); }
.hub-robot-shield svg { width: 17px; height: 17px; }
.hub-assistant-copy { min-width: 0; }
.hub-assistant-copy > p { margin: 10px 0; color: #d5dfeb; font-size: 12px; line-height: 1.7; }
.hub-status { padding: 17px; border-color: rgba(68, 205, 173, .22); background: linear-gradient(155deg, rgba(10, 39, 42, .84), rgba(13, 25, 39, .98)); }
.hub-card-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
.hub-card-heading h2 { margin: 5px 0 0; font-family: 'Space Grotesk', sans-serif; font-size: 15px; }
.hub-status-live, .threat-feed-badge { display: inline-flex; align-items: center; gap: 5px; padding: 5px 7px; border: 1px solid rgba(90, 220, 180, .18); border-radius: 20px; color: #78ddb8; font-size: 8px; font-weight: 700; white-space: nowrap; }
.hub-status-live i, .threat-feed-badge i { width: 5px; height: 5px; border-radius: 50%; background: #5be2ad; box-shadow: 0 0 8px #5be2ad; animation: hub-live 2s ease-in-out infinite; }
.hub-status-main { display: flex; align-items: center; gap: 15px; margin: 18px 0 12px; }
.hub-score-ring { display: grid; place-items: center; width: 90px; aspect-ratio: 1; border-radius: 50%; background: conic-gradient(#52e0bd 0 85%, rgba(105, 133, 151, .17) 85% 100%); animation: hub-ring-in 1.1s ease-out both; }
.hub-score-ring > div { display: grid; place-content: center; width: 73px; aspect-ratio: 1; border-radius: 50%; background: #10252c; text-align: center; }
.hub-score-ring strong { color: #e5fff8; font-family: 'Space Grotesk', sans-serif; font-size: 21px; }
.hub-score-ring small { color: #88b4ad; font-size: 7px; }
.hub-protected { display: inline-flex; align-items: center; gap: 5px; color: #7ce0ba; font-size: 10px; font-weight: 700; }
.hub-protected svg { width: 14px; height: 14px; }
.hub-status-main p { margin: 7px 0 0; color: #9bafa9; font-size: 10px; }
.hub-actions-callout { display: flex; align-items: center; gap: 9px; margin: 9px 0 12px; padding: 9px 10px; border: 1px solid rgba(247, 184, 108, .14); border-radius: 8px; background: rgba(225, 152, 71, .06); }
.hub-actions-callout p { margin: 0; color: #c4cbd1; font-size: 10px; line-height: 1.5; }
.hub-actions-callout strong { color: #f5c578; }
.hub-full-button { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; min-height: 38px; font-size: 10px; }
.hub-full-button svg { width: 14px; height: 14px; }
.hub-threats { padding: 16px; }
.hub-threats .hub-card-heading { align-items: center; }
.threat-feed-badge { border-color: rgba(255, 114, 128, .16); color: #f7919b; font-size: 7px; }
.threat-feed-badge i { background: #ff7181; box-shadow: 0 0 8px #ff7181; }
.hub-threat-list { display: grid; gap: 2px; margin: 11px 0 7px; }
.hub-threat-list > button { display: grid; grid-template-columns: 8px minmax(0, 1fr) auto; align-items: center; gap: 8px; min-height: 31px; padding: 5px 2px; border: 0; border-bottom: 1px solid rgba(140, 160, 181, .07); background: transparent; color: #c6d1dc; text-align: left; cursor: pointer; }
.hub-threat-list > button:hover { color: #fff; }
.hub-threat-list > button > span:nth-child(2) { overflow: hidden; font-size: 9px; text-overflow: ellipsis; white-space: nowrap; }
.hub-threat-list strong { font-size: 8px; }
.hub-threat-note { margin: 6px 0 8px; color: var(--subtle); font-size: 8px; line-height: 1.4; }
.threat-dot { width: 6px; height: 6px; border-radius: 50%; }
.threat-high { background: #ff6e7e; box-shadow: 0 0 7px rgba(255, 110, 126, .5); }
.threat-medium { background: #f4b358; box-shadow: 0 0 7px rgba(244, 179, 88, .4); }
.threat-low { background: #5ccda6; box-shadow: 0 0 7px rgba(92, 205, 166, .4); }
.severity-high { color: #ff8490 !important; }.severity-medium { color: #edbe70 !important; }.severity-low { color: #75d5af !important; }
.hub-threats > .text-link { display: inline-flex; align-items: center; gap: 5px; font-size: 10px; }
.hub-threats > .text-link svg { width: 13px; height: 13px; }
.hub-tools-section, .hub-journey { min-width: 0; }
.hub-section-heading { display: flex; align-items: flex-end; justify-content: space-between; gap: 15px; margin-bottom: 14px; }
.hub-section-heading h2 { margin: 5px 0; font-family: 'Space Grotesk', sans-serif; font-size: 18px; }
.hub-section-heading p { margin: 0; color: var(--muted); font-size: 11px; }
.hub-section-index { color: var(--subtle); font-size: 8px; font-weight: 700; letter-spacing: .7px; white-space: nowrap; }
.hub-tools-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 11px; }
.hub-tool-card { position: relative; display: flex; flex-direction: column; align-items: flex-start; min-height: 185px; overflow: hidden; padding: 15px; border: 1px solid rgba(132, 165, 191, .15); border-radius: 11px; background: linear-gradient(150deg, rgba(18, 30, 48, .97), rgba(11, 18, 31, .98)); transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease; }
.hub-tool-card:before { position: absolute; right: -28px; bottom: -47px; width: 110px; height: 110px; border-radius: 50%; background: var(--tool-glow); opacity: .13; filter: blur(22px); content: ''; pointer-events: none; }
.hub-tool-card:hover { transform: translateY(-3px); border-color: color-mix(in srgb, var(--tool-accent) 55%, transparent); box-shadow: 0 11px 28px rgba(0, 0, 0, .22), 0 0 18px color-mix(in srgb, var(--tool-accent) 13%, transparent); }
.tool-threat { --tool-accent: #ff758e; --tool-glow: #fa385e; }.tool-privacy { --tool-accent: #b28bff; --tool-glow: #8a55f6; }.tool-device { --tool-accent: #50d7ed; --tool-glow: #178dcc; }.tool-wifi { --tool-accent: #f3b55f; --tool-glow: #ef8a2d; }.tool-emergency { --tool-accent: #5bd5a2; --tool-glow: #2cbf79; }.tool-accounts { --tool-accent: #7bafff; --tool-glow: #386ff1; }.tool-cleanup { --tool-accent: #69d5c2; --tool-glow: #2ab6aa; }.tool-calendar { --tool-accent: #c39aff; --tool-glow: #8654e8; }
.hub-new-badge { position: absolute; top: 13px; right: 12px; padding: 4px 6px; border: 1px solid color-mix(in srgb, var(--tool-accent) 35%, transparent); border-radius: 10px; color: var(--tool-accent); font-size: 7px; font-weight: 800; letter-spacing: .7px; animation: hub-badge 3s ease-in-out infinite; }
.hub-tool-icon { display: grid; place-items: center; width: 36px; height: 36px; margin-bottom: 10px; border: 1px solid color-mix(in srgb, var(--tool-accent) 30%, transparent); border-radius: 10px; background: color-mix(in srgb, var(--tool-accent) 9%, transparent); font-size: 18px; }
.hub-tool-card h3 { margin: 0 0 6px; padding-right: 25px; color: #e1eaf5; font-size: 12px; line-height: 1.4; }
.hub-tool-card p { margin: 0 0 12px; color: #96a5b7; font-size: 9px; line-height: 1.55; }
.hub-tool-card > button { display: inline-flex; align-items: center; gap: 6px; margin-top: auto; padding: 0; border: 0; background: transparent; color: var(--tool-accent); font-size: 9px; font-weight: 700; cursor: pointer; }
.hub-tool-card > button svg { width: 13px; height: 13px; transition: transform .18s ease; }
.hub-tool-card > button:hover svg { transform: translateX(3px); }
.hub-bottom-grid { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(250px, .8fr); align-items: start; gap: 16px; }
.hub-tip-card, .hub-journey { padding: 17px; }
.hub-tip-count { color: var(--muted); font-size: 9px; font-weight: 700; }
.hub-tip-content { display: grid; grid-template-columns: 100px minmax(0, 1fr); align-items: center; gap: 17px; min-height: 120px; }
.hub-phone-art { position: relative; display: grid; place-items: center; width: 78px; height: 94px; margin: 0 auto; border: 2px solid rgba(91, 209, 227, .52); border-radius: 15px; background: linear-gradient(150deg, #122e41, #101629); color: #79e1eb; box-shadow: 0 0 24px rgba(71, 202, 226, .14), inset 0 0 20px rgba(49, 177, 209, .11); transform: rotate(-5deg); }
.hub-phone-art > svg { width: 40px; height: 48px; stroke-width: 1.2; }
.hub-phone-art > span { position: absolute; right: -11px; bottom: 8px; display: grid; place-items: center; width: 29px; height: 29px; border: 1px solid rgba(93, 221, 183, .44); border-radius: 9px; background: #10342f; color: #80e1ba; }
.hub-phone-art > span svg { width: 15px; height: 15px; }
.hub-tip-copy h3 { margin: 0 0 7px; color: #e5edf7; font-family: 'Space Grotesk', sans-serif; font-size: 16px; }
.hub-tip-copy p { max-width: 440px; margin: 0; color: #a3b1c1; font-size: 11px; line-height: 1.65; }
.hub-tip-controls { display: flex; align-items: center; justify-content: center; gap: 12px; }
.hub-tip-controls > button { display: grid; place-items: center; width: 28px; height: 28px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel-2); color: var(--text); cursor: pointer; }
.hub-tip-controls > button svg { width: 14px; height: 14px; }
.hub-tip-dots { display: flex; align-items: center; gap: 6px; }
.hub-tip-dots button { width: 6px; height: 6px; padding: 0; border: 0; border-radius: 50%; background: #536178; cursor: pointer; }
.hub-tip-dots button[aria-current="true"] { width: 17px; border-radius: 5px; background: #54d8e8; }
.hub-journey .hub-section-heading { align-items: flex-start; }
.journey-track { display: grid; grid-template-columns: 1fr 15px 1fr 15px 1fr 15px 1fr 15px 1fr; align-items: start; gap: 5px; padding: 18px 0 6px; }
.journey-step { display: grid; justify-items: center; gap: 7px; min-width: 0; text-align: center; animation: hub-node-in .55s both; }
.journey-step:nth-of-type(3) { animation-delay: .12s; }.journey-step:nth-of-type(5) { animation-delay: .24s; }.journey-step:nth-of-type(7) { animation-delay: .36s; }.journey-step:nth-of-type(9) { animation-delay: .48s; }
.journey-node { display: grid; place-items: center; width: 37px; height: 37px; border: 1px solid rgba(81, 201, 217, .37); border-radius: 50%; background: #102531; color: #7ce1e8; box-shadow: 0 0 15px rgba(52, 181, 208, .12); }
.journey-node svg { width: 16px; height: 16px; }
.journey-step strong { max-width: 95px; color: #cbd7e3; font-size: 8px; line-height: 1.4; }
.journey-value { color: #82ded4; font-size: 10px; font-weight: 700; }
.journey-progress { width: 100%; height: 3px; overflow: hidden; border-radius: 3px; background: rgba(115, 135, 158, .16); }
.journey-progress i { display: block; width: var(--journey-progress); height: 100%; border-radius: inherit; background: linear-gradient(90deg, #48cedf, #a078ff); transform-origin: left; animation: hub-progress-in .9s ease-out both; }
.journey-connector { height: 1px; margin-top: 18px; background: linear-gradient(90deg, rgba(78, 206, 222, .55), rgba(141, 113, 235, .4)); }
.hub-motivation { position: relative; display: grid; align-content: center; min-height: 215px; overflow: hidden; padding: 22px; border-color: rgba(136, 126, 209, .22); background: radial-gradient(ellipse at 78% 18%, rgba(92, 124, 209, .25), transparent 34%), linear-gradient(145deg, #141d34, #111525 68%, #1b1733); }
.hub-motivation:after { position: absolute; right: -15px; bottom: -31px; width: 210px; height: 115px; border-radius: 50% 50% 0 0; background: linear-gradient(160deg, rgba(92, 118, 176, .18), rgba(16, 21, 39, .95)); clip-path: polygon(0 100%, 24% 36%, 44% 65%, 67% 13%, 100% 100%); content: ''; }
.hub-stars { position: absolute; top: 17px; right: 16px; color: #b4c8ef; font-size: 12px; opacity: .75; }
.hub-motivation .eyebrow, .hub-motivation h2, .hub-motivation button { position: relative; z-index: 1; }
.hub-motivation h2 { margin: 14px 0; color: #edf1ff; font-family: 'Space Grotesk', sans-serif; font-size: 22px; line-height: 1.12; }
.hub-motivation h2 span { color: #75dceb; }
.hub-ask-card { display: grid; grid-template-columns: 43px minmax(0, 1fr) 37px; align-items: center; gap: 11px; padding: 15px; }
.hub-ask-icon { display: grid; place-items: center; width: 40px; height: 40px; border: 1px solid rgba(77, 205, 223, .28); border-radius: 13px; background: rgba(60, 173, 204, .09); color: #73dfe9; }
.hub-ask-icon svg { width: 21px; height: 21px; }
.hub-ask-card h2 { margin: 3px 0; font-size: 14px; }
.hub-ask-card p { margin: 0; color: var(--muted); font-size: 10px; }
.hub-ask-card > button { display: grid; place-items: center; width: 37px; height: 37px; border: 1px solid rgba(71, 212, 228, .38); border-radius: 50%; background: linear-gradient(135deg, #164b62, #243f74); color: #dffaff; box-shadow: 0 0 15px rgba(58, 197, 221, .15); cursor: pointer; transition: transform .18s, box-shadow .18s; }
.hub-ask-card > button:hover { transform: translateX(2px); box-shadow: 0 0 21px rgba(58, 197, 221, .35); }
.hub-ask-card > button svg { width: 17px; height: 17px; }
.hub-footer { display: flex; align-items: center; justify-content: space-between; gap: 15px; padding: 12px 2px 0; border-top: 1px solid var(--line); color: var(--muted); font-size: 9px; }
.hub-footer i { margin: 0 5px; color: var(--cyan); font-style: normal; }
.hub-dialog { position: fixed; inset: 50% auto auto 50%; width: min(560px, calc(100vw - 28px)); max-width: 560px; max-height: min(82vh, 760px); margin: 0; padding: 23px; overflow: auto; transform: translate(-50%, -50%); border: 1px solid rgba(86, 189, 213, .28); border-radius: 14px; background: #0c1522; color: #e5edf7; box-shadow: 0 24px 90px rgba(0, 0, 0, .6), 0 0 34px rgba(35, 156, 191, .1); }
.hub-dialog::backdrop { background: rgba(3, 7, 15, .72); backdrop-filter: blur(5px); }
.hub-dialog[open] { display: block; animation: hub-dialog-in .18s ease-out both; }
.hub-dialog h2 { margin: 7px 40px 15px 0; color: #edf5fc; font-family: 'Space Grotesk', sans-serif; font-size: 20px; }
.hub-dialog-close { position: absolute; top: 13px; right: 13px; }
.hub-dialog-intro, .hub-dialog-note { color: #aab8c8; font-size: 11px; line-height: 1.7; }
.hub-dialog-note { margin: 12px 0 0; color: var(--subtle); font-size: 9px; }
.hub-checklist, .hub-account-list, .hub-calendar-tasks { display: grid; gap: 7px; margin-top: 14px; }
.hub-check-row, .hub-calendar-task { display: flex; align-items: flex-start; gap: 10px; padding: 11px; border: 1px solid var(--line); border-radius: 9px; background: rgba(144, 176, 196, .035); cursor: pointer; }
.hub-check-row input, .hub-calendar-task input { flex: 0 0 auto; width: 15px; height: 15px; margin: 2px 0 0; accent-color: #51d8d9; }
.hub-check-row span { display: grid; gap: 4px; }
.hub-check-row strong { color: #dbe5ef; font-size: 11px; }
.hub-check-row small { color: #8d9eaf; font-size: 9px; line-height: 1.5; }
.hub-threat-detail-list, .hub-scenario-list { display: grid; gap: 7px; margin-top: 13px; }
.hub-threat-detail-row, .hub-scenario-button { display: grid; grid-template-columns: 8px minmax(0, 1fr) auto; align-items: center; gap: 10px; padding: 11px; border: 1px solid var(--line); border-radius: 9px; background: rgba(143, 169, 194, .04); color: var(--text); text-align: left; cursor: pointer; }
.hub-threat-detail-row:hover, .hub-scenario-button:hover { border-color: rgba(81, 205, 222, .34); background: rgba(81, 205, 222, .06); }
.hub-threat-detail-row > span:nth-child(2) { display: grid; gap: 4px; }
.hub-threat-detail-row strong, .hub-scenario-button span { color: #dfe8f2; font-size: 10px; }
.hub-threat-detail-row small { color: #91a0b1; font-size: 9px; line-height: 1.5; }
.hub-threat-detail-row > b { font-size: 9px; }
.hub-scenario-button { grid-template-columns: minmax(0, 1fr) 18px; }
.hub-scenario-button svg { width: 15px; height: 15px; color: var(--cyan); }
.hub-emergency-steps { display: grid; gap: 12px; padding-left: 22px; color: #cbd7e3; font-size: 11px; line-height: 1.65; }
.hub-emergency-steps li::marker { color: var(--cyan); font-weight: 700; }
.hub-risk-label { display: inline-flex; margin-bottom: 6px; font-size: 9px; font-weight: 700; text-transform: uppercase; }
.hub-safe-callout { display: flex; gap: 9px; margin-top: 12px; padding: 12px; border: 1px solid rgba(88, 208, 169, .18); border-radius: 8px; background: rgba(88, 208, 169, .05); color: #a9d9c5; font-size: 10px; line-height: 1.5; }
.hub-safe-callout svg { flex: 0 0 16px; width: 16px; height: 16px; color: #72d8ae; }
.hub-account-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 10px; border: 1px solid var(--line); border-radius: 8px; background: rgba(145, 173, 197, .035); }
.hub-account-row > span { display: flex; align-items: center; gap: 8px; color: #d7e2ee; font-size: 10px; }
.hub-account-row svg { width: 15px; height: 15px; color: var(--cyan); }
.hub-account-row select { max-width: 160px; padding: 7px 8px; border: 1px solid var(--line-strong); border-radius: 7px; background: #101c2a; color: #e2ebf2; font-size: 9px; }
.hub-calendar-grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; margin-top: 16px; }
.hub-calendar-day { display: grid; justify-items: center; gap: 5px; min-height: 57px; padding: 7px 3px; border: 1px solid var(--line); border-radius: 8px; background: #111d2a; color: #bdcad7; cursor: pointer; }
.hub-calendar-day small { color: #8e9eaf; font-size: 8px; }
.hub-calendar-day strong { font-size: 12px; }
.hub-calendar-day.selected { border-color: var(--cyan); background: rgba(51, 175, 203, .13); color: #fff; box-shadow: 0 0 12px rgba(55, 188, 212, .1); }
.hub-calendar-selected { margin: 15px 0 0; color: #cbd7e3; font-size: 11px; font-weight: 700; }
.hub-calendar-task { align-items: center; color: #cbd7e3; font-size: 10px; }
.hub-report-list { display: grid; gap: 5px; margin: 14px 0; }
.hub-report-row { display: flex; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid var(--line); color: #aab8c8; font-size: 10px; }
.hub-report-row strong { color: #75d9d9; }
.hub-dialog .primary-button { margin-top: 10px; }
.hub-dialog .text-link { display: inline-flex; align-items: center; gap: 6px; margin-top: 14px; }
.hub-dialog .text-link svg { width: 14px; height: 14px; }
.home-robot-bubble { position: absolute; z-index: 2; top: 57px; left: 13px; width: min(55%, 175px); padding: 8px 10px; border: 1px solid rgba(89, 210, 231, .2); border-radius: 10px 10px 10px 3px; background: rgba(8, 21, 33, .84); color: #d9f4fa; box-shadow: 0 5px 20px rgba(0, 0, 0, .2), 0 0 16px rgba(60, 199, 224, .08); font-size: 8px; line-height: 1.45; }
.home-robot-bubble:after { position: absolute; bottom: -5px; left: 7px; width: 8px; height: 8px; border-right: 1px solid rgba(89, 210, 231, .2); border-bottom: 1px solid rgba(89, 210, 231, .2); background: #0a1826; content: ''; transform: skewY(35deg); }
.assistant-card .robot-art { animation: hub-float 5.5s ease-in-out infinite; }
.home-tip-widget { display: grid; grid-template-columns: 40px minmax(0, 1fr) auto; align-items: center; gap: 13px; margin-top: 16px; padding: 13px 17px; border-color: rgba(71, 192, 218, .22); background: linear-gradient(100deg, rgba(13, 29, 45, .96), rgba(15, 24, 41, .96)); box-shadow: inset 0 1px rgba(255, 255, 255, .025), 0 7px 22px rgba(0, 0, 0, .1); }
.home-tip-icon { display: grid; place-items: center; width: 36px; height: 36px; border: 1px solid rgba(94, 214, 230, .23); border-radius: 10px; background: rgba(68, 188, 210, .09); color: #7de4eb; box-shadow: 0 0 16px rgba(56, 192, 219, .1); }
.home-tip-icon svg { width: 18px; height: 18px; }
.home-tip-copy { min-width: 0; }
.home-tip-copy .eyebrow { display: block; margin-bottom: 4px; color: #87bfd0; font-size: 8px; }
.home-tip-copy p { display: inline; margin: 0; color: #d4deea; font-size: 11px; line-height: 1.5; }
.home-tip-copy .text-link { display: inline-flex; align-items: center; gap: 4px; margin-left: 7px; color: #71dbe7; font-size: 9px; white-space: nowrap; }
.home-tip-copy .text-link svg { width: 12px; height: 12px; }
.home-tip-controls { display: flex; align-items: center; gap: 7px; }
.home-tip-controls > button { display: grid; place-items: center; width: 25px; height: 25px; border: 1px solid var(--line); border-radius: 7px; background: rgba(128, 160, 183, .06); color: #bdd0de; cursor: pointer; transition: border-color .16s, color .16s, background .16s; }
.home-tip-controls > button:hover { border-color: rgba(85, 212, 231, .45); background: rgba(69, 183, 210, .1); color: #8fe9f0; }
.home-tip-controls > button svg { width: 13px; height: 13px; }
.home-tip-dots { display: flex; align-items: center; gap: 4px; }
.home-tip-dots button { width: 5px; height: 5px; padding: 0; border: 0; border-radius: 5px; background: #46586e; cursor: pointer; }
.home-tip-dots button[aria-current="true"] { width: 13px; background: #58d7e6; box-shadow: 0 0 7px rgba(88, 215, 230, .42); }
.home-motivation-widget { position: relative; display: flex; align-items: center; justify-content: space-between; gap: 18px; min-height: 92px; overflow: hidden; margin-top: 14px; padding: 15px 20px; border-color: rgba(105, 128, 205, .2); background: linear-gradient(105deg, rgba(14, 25, 43, .97), rgba(18, 21, 43, .95) 72%, rgba(30, 24, 55, .9)); transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease; }
.home-motivation-widget:hover { transform: translateY(-2px); border-color: rgba(103, 185, 229, .36); box-shadow: 0 9px 25px rgba(0, 0, 0, .18), 0 0 17px rgba(81, 145, 214, .08); }
.home-motivation-widget > div:not(.home-mountain-art) { position: relative; z-index: 1; }
.home-motivation-widget h2 { margin: 5px 0 0; color: #e5ebf8; font-family: 'Space Grotesk', sans-serif; font-size: 16px; }
.home-motivation-widget h2 span { color: #75dbe8; }
.home-motivation-widget .eyebrow { color: #929fc0; font-size: 8px; }
.home-motivation-widget > button { position: relative; z-index: 2; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
.home-motivation-widget > button svg { width: 14px; height: 14px; }
.home-mountain-art { position: absolute; top: 0; right: 13%; bottom: 0; width: 32%; overflow: hidden; background: radial-gradient(ellipse at 68% 31%, rgba(133, 175, 255, .17), transparent 48%); }
.home-mountain-art:before, .home-mountain-art:after { position: absolute; right: -4%; bottom: 0; width: 108%; height: 68%; background: linear-gradient(150deg, rgba(59, 100, 150, .34), rgba(21, 36, 65, .78)); clip-path: polygon(0 100%, 28% 34%, 43% 59%, 69% 4%, 100% 100%); content: ''; }
.home-mountain-art:after { right: 17%; width: 83%; height: 44%; background: linear-gradient(150deg, rgba(68, 89, 151, .34), rgba(26, 30, 62, .83)); clip-path: polygon(0 100%, 32% 24%, 54% 58%, 79% 0, 100% 100%); }
.home-mountain-art span { position: absolute; z-index: 1; color: #c6ddff; font-size: 9px; text-shadow: 0 0 9px rgba(161, 204, 255, .75); }
.home-mountain-art span:nth-child(1) { top: 17px; left: 24%; }.home-mountain-art span:nth-child(2) { top: 29px; right: 13%; }.home-mountain-art span:nth-child(3) { top: 12px; right: 34%; }
:host(.reduce-motion) .assistant-card .robot-art { animation: none !important; }
@media (max-width: 760px) { .home-motivation-widget { min-height: 86px; padding: 13px 16px; } .home-mountain-art { right: 18%; width: 28%; } }
@media (max-width: 570px) {
    .home-robot-bubble { top: 48px; left: 10px; width: 52%; padding: 7px; font-size: 7px; }
    .home-tip-widget { grid-template-columns: 32px minmax(0, 1fr); gap: 9px; padding: 11px; }
    .home-tip-icon { width: 31px; height: 31px; }
    .home-tip-controls { grid-column: 2; justify-content: flex-end; }
    .home-tip-copy p { font-size: 10px; }
    .home-motivation-widget { gap: 8px; padding: 12px; }
    .home-motivation-widget h2 { font-size: 13px; }
    .home-motivation-widget > button { padding: 8px; font-size: 9px; }
    .home-mountain-art { right: 17%; width: 27%; opacity: .8; }
}
:host(.theme-light) .hub-hero-copy h1 > span:first-child,
:host(.theme-light) .hub-hero-copy h1 strong,
:host(.theme-light) .hub-tool-card h3,
:host(.theme-light) .hub-tool-card p,
:host(.theme-light) .hub-tip-copy h3,
:host(.theme-light) .hub-tip-copy p,
:host(.theme-light) .hub-dialog h2,
:host(.theme-light) .hub-dialog-intro,
:host(.theme-light) .hub-dialog-note,
:host(.theme-light) .hub-check-row strong,
:host(.theme-light) .hub-check-row small,
:host(.theme-light) .hub-threat-detail-row strong,
:host(.theme-light) .hub-threat-detail-row small,
:host(.theme-light) .hub-scenario-button span,
:host(.theme-light) .hub-emergency-steps,
:host(.theme-light) .hub-account-row > span,
:host(.theme-light) .hub-calendar-day,
:host(.theme-light) .hub-calendar-day small,
:host(.theme-light) .hub-calendar-selected,
:host(.theme-light) .hub-calendar-task,
:host(.theme-light) .hub-report-row { color: #000 !important; }
@keyframes hub-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
@keyframes hub-live { 50% { opacity: .38; box-shadow: 0 0 2px currentColor; } }
@keyframes hub-badge { 50% { box-shadow: 0 0 9px color-mix(in srgb, var(--tool-accent) 35%, transparent); } }
@keyframes hub-ring-in { from { opacity: .3; transform: rotate(-120deg) scale(.8); } to { opacity: 1; transform: rotate(0) scale(1); } }
@keyframes hub-node-in { from { opacity: 0; transform: translateX(-9px); } to { opacity: 1; transform: translateX(0); } }
@keyframes hub-progress-in { from { width: 0; } to { width: var(--journey-progress); } }
@keyframes hub-dialog-in { from { opacity: 0; transform: translate(-50%, -47%); } to { opacity: 1; transform: translate(-50%, -50%); } }
@keyframes hub-view-enter { from { opacity: 0; } to { opacity: 1; } }
@container stay-aware (max-width: 1000px) {
    .hub-dashboard-grid { grid-template-columns: minmax(0, 1fr); }
    .hub-primary-column { grid-template-columns: minmax(0, 1.2fr) minmax(0, .8fr); }
    .hub-side-column { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@container stay-aware (max-width: 680px) {
    .hub-primary-column, .hub-side-column, .hub-bottom-grid, .hub-bottom-side { grid-template-columns: minmax(0, 1fr); }
}
:host(.reduce-motion) .hub-page *, :host(.reduce-motion) .hub-page *:before, :host(.reduce-motion) .hub-page *:after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: .01ms !important;
}
:host(.theme-light) .assessment-card { background: #fff; color: var(--text); }
:host(.theme-light) {
    color-scheme: light;
    --bg: #edf3f4; --panel: #ffffff; --panel-2: #e4edef; --sidebar: #f6f9fa;
    --line: rgba(38, 66, 76, .12); --line-strong: rgba(38, 66, 76, .22);
    --text: #17272d; --muted: #596b72; --subtle: #77868b;
    --blue: #416ac2; --cyan: #087d82; --green: #19836d; --amber: #986300; --red: #ba3e52;
    color: var(--text); background: var(--bg);
}
:host(.theme-light) .sidebar { background: #f8fafb; border-color: var(--line); }
:host(.theme-light) .main-area, :host(.theme-light) .topbar { background: #edf3f4; color: var(--text); }
:host(.theme-light) .nav-link { color: #596b72; }
:host(.theme-light) .nav-link:hover, :host(.theme-light) .nav-link.active { color: #19343a; }
:host(.theme-light) .crumb, :host(.theme-light) .crumb strong,
:host(.theme-light) .page-heading h1, :host(.theme-light) .page-heading p,
:host(.theme-light) .section-heading h2, :host(.theme-light) .welcome-copy h1,
:host(.theme-light) .welcome-copy h2, :host(.theme-light) .panel h2,
:host(.theme-light) .panel h3 { color: var(--text); }
:host(.theme-light) .panel, :host(.theme-light) .assistant-card,
:host(.theme-light) .welcome-copy, :host(.theme-light) .feature-card,
:host(.theme-light) .chat-layout, :host(.theme-light) .login-panel {
    border-color: var(--line); background-color: #fff; color: var(--text);
}
:host(.theme-light) .chat-messages { background-color: #f4f8f8; }
:host(.theme-light) .message-content { color: #24383d; }
:host(.theme-light) .assistant-message .message-content { background: #e8f2f0; color: #24383d; }
:host(.theme-light) .user-message .message-content { background: #e8edfb; color: #23334f; }
:host(.theme-light) .login-form input { background: #fff; color: var(--text); }
:host(.theme-light) .score-summary p, :host(.theme-light) .card-text,
:host(.theme-light) .learning-card p, :host(.theme-light) .assistant-card p { color: var(--muted); }
:host(.theme-light), :host(.theme-light) :where(*) {
    background-color: #fff !important;
    background-image: none !important;
    color: #000 !important;
    font-weight: 600 !important;
}
:host(.theme-light) img, :host(.theme-light) svg, :host(.theme-light) path {
    background-color: transparent !important;
}
@keyframes message-arrive { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
@media (max-width: 760px) {
    .plans-grid { grid-template-columns: 1fr; }
    .plan-card { min-height: 0; }
    .hub-dashboard-grid, .hub-bottom-grid { grid-template-columns: 1fr; }
    .hub-primary-column { grid-template-columns: minmax(0, 1.2fr) minmax(0, .8fr); align-items: stretch; }
    .hub-side-column { grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; }
    .hub-tools-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .hub-bottom-side { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .hub-motivation { min-height: 190px; }
    .assessment-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .login-layout { grid-template-columns: 1fr; gap: 24px; align-content: center; min-height: auto; padding: 30px 0; }
    .login-intro h1 { font-size: 30px; }
}
@media (max-width: 570px) {
    .hub-page { gap: 18px; }
    .hub-primary-column, .hub-side-column, .hub-bottom-side { grid-template-columns: 1fr; }
    .hub-hero { grid-template-columns: minmax(0, 1fr) 90px; min-height: 0; padding: 19px 16px; }
    .hub-hero-copy h1 { font-size: 27px; }
    .hub-hero-copy h2 { font-size: 12px; }
    .hub-hero-copy > p { font-size: 10px; }
    .hub-shield-scene { min-height: 145px; }
    .hub-shield-orbit { width: 90px; }
    .hub-shield-mark { width: 74px; height: 93px; }
    .hub-shield-mark > svg:first-child { width: 76px; height: 91px; }
    .hub-shield-mark > svg:last-child { width: 28px; height: 28px; }
    .hub-pill-row { gap: 5px; }
    .hub-pill-row span { padding: 6px 7px; font-size: 8px; }
    .hub-assistant { grid-template-columns: 95px minmax(0, 1fr); gap: 9px; padding: 10px; }
    .hub-robot-wrap img { width: 94px; height: 108px; }
    .hub-robot-wrap { min-height: 108px; }
    .hub-assistant-copy > p { font-size: 10px; }
    .hub-tools-grid { gap: 8px; }
    .hub-tool-card { min-height: 178px; padding: 12px; }
    .hub-section-heading { align-items: flex-start; }
    .hub-section-index { display: none; }
    .hub-tip-content { grid-template-columns: 70px minmax(0, 1fr); gap: 11px; }
    .hub-phone-art { width: 58px; height: 76px; }
    .hub-phone-art > svg { width: 30px; height: 38px; }
    .hub-tip-copy h3 { font-size: 13px; }
    .hub-tip-copy p { font-size: 10px; }
    .journey-track { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 7px; overflow-x: auto; }
    .journey-connector { display: none; }
    .journey-step strong { font-size: 7px; }
    .journey-node { width: 31px; height: 31px; }
    .hub-footer { align-items: flex-start; flex-direction: column; }
    .hub-dialog { padding: 19px; }
    .assessment-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
    .message { max-width: 94%; }
    .message-content { padding: 10px 12px; }
    .login-panel { padding: 20px; }
}
"""
        css = re.sub(r"(?<![\w-]):root\b", ":host", css)
        css = re.sub(r"(?<![\w-])body(?![\w-])", ":host", css)

        javascript = (APP_DIR / "script.js").read_text(encoding="utf-8")
        javascript = javascript.replace(
                "document.addEventListener('DOMContentLoaded', initialize);", ""
        )
        javascript = re.sub(r"\bdocument\.", "root.", javascript)
        javascript = javascript.replace("root.body.", "root.host.")
        javascript = javascript.replace(
                "root.createElement(", "root.ownerDocument.createElement("
        )
        javascript = javascript.replace("window.lucide.createIcons();", "refreshIcons();")
        javascript = re.sub(r"^\s*root\.title = .*?$", "", javascript, flags=re.MULTILINE)

        component_javascript = f"""
export default function(component) {{
    const {{ data, parentElement, setTriggerValue }} = component;
    const root = parentElement;
    window.cyberguardSetTrigger = setTriggerValue;
    {javascript}

    function refreshIcons() {{
        if (!window.lucide) return;
        const placeholders = root.querySelectorAll('[data-lucide]');
        const iconRoot = root.ownerDocument.createElement('div');
        placeholders.forEach((placeholder) => iconRoot.append(placeholder.cloneNode()));
        root.ownerDocument.body.appendChild(iconRoot);
        window.lucide.createIcons();
        const renderedIcons = iconRoot.querySelectorAll('svg');
        placeholders.forEach((placeholder, index) => {{
            if (renderedIcons[index]) placeholder.replaceWith(renderedIcons[index].cloneNode(true));
        }});
        iconRoot.remove();
    }}

    if (!root.__cyberguardInitialized) {{
        initialize();
        root.__cyberguardInitialized = true;
    }}

    if (data?.response && data.response_id && localStorage.getItem('cyberguard.streamlitResponse') !== data.response_id) {{
        const messages = readChat();
        messages.push({{ role: 'assistant', text: data.response, time: formatTime() }});
        saveChat(messages);
        localStorage.setItem('cyberguard.streamlitResponse', data.response_id);
        renderChat();
    }}

    if (!window.lucide && !window.cyberguardLucideLoading) {{
        window.cyberguardLucideLoading = true;
        const iconScript = root.ownerDocument.createElement('script');
        iconScript.src = 'https://unpkg.com/lucide@0.468.0/dist/umd/lucide.min.js';
        iconScript.onload = () => {{
            window.cyberguardLucideLoading = false;
            refreshIcons();
        }};
        iconScript.onerror = () => {{ window.cyberguardLucideLoading = false; }};
        root.ownerDocument.head.appendChild(iconScript);
    }}
}}
"""

        return st.components.v2.component(
                "cyberguard_web_dashboard",
                html=html,
                css=css,
                js=component_javascript,
        )


WEB_DASHBOARD = build_dashboard_component()

st.set_page_config(
    page_title="CyberGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.stApp {
    background: #050b1c;
    color: white;
}

section[data-testid="stSidebar"] {
    background: #071329;
    border-right: 1px solid #172b52;
}

section[data-testid="stSidebar"] h1 {
    color: #ffffff;
}

.cyber-title {
    font-size: 38px;
    font-weight: 800;
    color: white;
}

.cyber-title span {
    color: #6575ff;
}

.subtitle {
    color: #aab6d3;
    font-size: 16px;
}

.card {
    background: linear-gradient(145deg, #0c1b3b, #08142d);
    border: 1px solid #203b70;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0px 0px 20px rgba(42, 88, 180, 0.08);
}

.card:hover {
    border-color: #536dff;
}

.card-title {
    font-size: 19px;
    font-weight: 700;
    color: white;
}

.card-text {
    color: #aebbd5;
    font-size: 14px;
}

.risk-high {
    background: #351327;
    border: 1px solid #e44872;
    border-radius: 15px;
    padding: 20px;
}

.risk-safe {
    background: #0c3029;
    border: 1px solid #20c997;
    border-radius: 15px;
    padding: 20px;
}

.score {
    font-size: 55px;
    font-weight: 800;
    color: #48e0c2;
}

.small-text {
    color: #9baaca;
}

.chat-user {
    background: #243b85;
    padding: 13px 18px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
}

.chat-bot {
    background: #102143;
    padding: 13px 18px;
    border-radius: 15px;
    margin: 8px 0;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:

    st.markdown("""
    <h2>🛡️ CyberGuard AI</h2>
    <p style="color:white;">Think Safe. Click Safe.</p>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🌐 Full Dashboard",
            "🏠 Home",
            "💬 Chatbot",
            "✉️ Phishing Detector",
            "🏆 Cybersecurity Quiz",
            "📖 Learning Center",
            "🛡️ Safety Score",
            "⚙️ Settings"
        ],
        index=0,
    )

    st.markdown("---")

    st.markdown("""
    <div class="card">
        🛡️ <b>Stay Aware</b><br>
        <span class="small-text">Stay Secure</span>
    </div>
    """, unsafe_allow_html=True)


if page == "🌐 Full Dashboard":
    st.markdown("""
    <style>
    section[data-testid="stSidebar"], header[data-testid="stHeader"] { display: none; }
    .stMainBlockContainer { max-width: none; padding: 0; }
    </style>
    """, unsafe_allow_html=True)
    response = st.session_state.get("dashboard_response", {})
    result = WEB_DASHBOARD(
        key="cyberguard_dashboard",
        data={
            "response": response.get("content"),
            "response_id": response.get("id"),
        },
        on_question_change=lambda: None,
    )

    if result.question:
        try:
            with st.spinner("CyberGuard is preparing a response..."):
                answer = ask_ai(result.question)
        except Exception:
            answer = (
                "The local AI service is unavailable. Start Ollama and make sure "
                "the llama3.2:3b model is installed, then try again."
            )

        st.session_state["dashboard_response"] = {
            "content": answer,
            "id": uuid.uuid4().hex,
        }
        st.rerun()


elif page == "🏠 Home":

    st.markdown(
        '<div class="cyber-title">Hello! 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="cyber-title">I\'m your <span>Cybersecurity Awareness Chatbot.</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">I\'m here to help you stay safe online. Ask me about cyber threats, scams, password safety, or use the tools below.</p>',
        unsafe_allow_html=True
    )

    st.write("")

    # Feature cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
        📧<br>
        <div class="card-title">Detect Phishing</div>
        <div class="card-text">Check suspicious emails, links or messages.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        🏆<br>
        <div class="card-title">Take a Quiz</div>
        <div class="card-text">Test your cybersecurity knowledge.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        📖<br>
        <div class="card-title">Learn & Grow</div>
        <div class="card-text">Explore cybersecurity topics.</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card">
        🛡️<br>
        <div class="card-title">Check Your Score</div>
        <div class="card-text">See how safe you are online.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="card">
        <h3>🤖 CyberGuard Assistant</h3>
        <p class="card-text">
        Your AI assistant for cybersecurity awareness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user_question = st.text_input(
        "Ask CyberGuard",
        placeholder="Type your message..."
    )

    if st.button("Send 🚀"):

        if user_question:

            question = user_question.lower()

            if "password" in question:
                answer = """
                🔐 **Password Safety**

                • Use a long, unique password  
                • Never reuse passwords  
                • Use a password manager  
                • Enable MFA wherever possible
                """

            elif "phishing" in question or "email" in question:
                answer = """
                🎣 **Phishing Safety**

                Check the sender, links, urgency, spelling and requests for personal information.
                Never click suspicious links before verifying them.
                """

            elif "otp" in question:
                answer = """
                🔑 **OTP Safety**

                Never share your OTP with anyone, even if they claim to be from your bank or company.
                """

            elif "virus" in question or "malware" in question:
                answer = """
                🦠 **Malware Safety**

                Keep your operating system and applications updated, avoid suspicious downloads,
                and use trusted security software.
                """

            else:
                answer = """
                🛡️ **CyberGuard says:**

                Stay cautious online. Don't click unknown links, don't share OTPs or passwords,
                enable MFA, and verify suspicious messages through official sources.
                """

            st.success(answer)

    st.info("💡 Try asking: Is this email safe? / How can I create a strong password?")


elif page == "💬 Chatbot":

    st.title("💬 CyberGuard AI Chatbot")

    st.write(
        "Ask questions about phishing, scams, passwords, malware, privacy and online safety."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="chat-user">
                👤 {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="chat-bot">
                🛡️ {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    question = st.chat_input("Ask CyberGuard anything...")

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        try:
            response = ask_ai(question)
        except Exception:
            response = (
                "The local AI service is unavailable. Start Ollama and make sure "
                "the llama3.2:3b model is installed, then try again."
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


elif page == "✉️ Phishing Detector":

    st.title("✉️ Phishing Detector")

    st.write(
        "Paste an email, SMS or message below and CyberGuard will check for common phishing indicators."
    )

    message = st.text_area(
        "Paste suspicious message",
        height=220,
        placeholder="Paste the email, SMS or message here..."
    )

    if st.button("🔍 Analyze Message"):

        if not message.strip():

            st.warning("Please paste a message first.")

        else:

            text = message.lower()

            risk_points = 0
            reasons = []

            urgency_words = [
                "urgent",
                "immediately",
                "within 24 hours",
                "account will be blocked",
                "act now"
            ]

            if any(word in text for word in urgency_words):
                risk_points += 2
                reasons.append("Uses urgent or threatening language.")

            if "http://" in text or "https://" in text or "www." in text:
                risk_points += 2
                reasons.append("Contains a link that should be verified.")

            sensitive_words = [
                "password",
                "otp",
                "credit card",
                "bank details",
                "pin",
                "cvv"
            ]

            if any(word in text for word in sensitive_words):
                risk_points += 3
                reasons.append("Requests sensitive information.")

            if "dear user" in text or "dear customer" in text:
                risk_points += 1
                reasons.append("Uses a generic greeting.")

            if risk_points >= 5:

                st.markdown("""
                <div class="risk-high">
                <h2>🔴 HIGH RISK</h2>
                <p>This message contains multiple suspicious indicators.</p>
                </div>
                """, unsafe_allow_html=True)

            elif risk_points >= 2:

                st.warning("🟡 SUSPICIOUS — Verify this message before taking action.")

            else:

                st.markdown("""
                <div class="risk-safe">
                <h2>🟢 LOW RISK</h2>
                <p>No major phishing indicators were detected.</p>
                </div>
                """, unsafe_allow_html=True)

            if reasons:

                st.subheader("⚠️ Why?")

                for reason in reasons:
                    st.write("•", reason)

            st.subheader("🛡️ What should you do?")

            st.write("""
            • Don't click suspicious links  
            • Don't share OTPs or passwords  
            • Verify the sender independently  
            • Use the organization's official website  
            • Report suspicious messages
            """)


elif page == "🏆 Cybersecurity Quiz":

    st.title("🏆 Cybersecurity Quiz")

    questions = [
        {
            "question": "You receive a message saying your bank account will be blocked unless you click a link. What should you do?",
            "options": [
                "Click the link immediately",
                "Reply with your account details",
                "Ignore it and verify through the official website",
                "Forward it to your friends"
            ],
            "answer": "Ignore it and verify through the official website"
        },
        {
            "question": "Should you share your OTP with someone claiming to be from your bank?",
            "options": [
                "Yes",
                "Only if they know your name",
                "Only during emergencies",
                "No"
            ],
            "answer": "No"
        },
        {
            "question": "Which is the strongest password?",
            "options": [
                "password123",
                "Sai2008",
                "MyDogName",
                "A long unique passphrase"
            ],
            "answer": "A long unique passphrase"
        },
        {
            "question": "What does MFA provide?",
            "options": [
                "An additional authentication layer",
                "Faster internet",
                "Free antivirus",
                "Extra storage"
            ],
            "answer": "An additional authentication layer"
        },
        {
            "question": "What should you do with a suspicious link?",
            "options": [
                "Click it to check",
                "Verify it before opening",
                "Forward it",
                "Enter your password"
            ],
            "answer": "Verify it before opening"
        }
    ]

    score = 0

    answers = []

    for i, q in enumerate(questions):

        st.subheader(f"Question {i + 1} of {len(questions)}")

        answer = st.radio(
            q["question"],
            q["options"],
            key=f"question_{i}"
        )

        answers.append(answer)

    if st.button("Submit Quiz 🚀"):

        for i, q in enumerate(questions):

            if answers[i] == q["answer"]:
                score += 1

        percentage = int((score / len(questions)) * 100)

        st.success(
            f"🎉 You scored {score}/{len(questions)} — {percentage}%"
        )

        if percentage >= 80:
            st.balloons()
            st.write("🟢 Excellent cybersecurity awareness!")

        elif percentage >= 50:
            st.write("🟡 Good start. Keep learning!")

        else:
            st.write("🔴 You should complete more cybersecurity training.")

elif page == "📖 Learning Center":

    st.title("📖 Cybersecurity Learning Center")

    topics = [
        ("🔐", "Password Security",
         "Create strong passwords and learn about password managers."),

        ("🎣", "Phishing",
         "Identify fake emails, messages and suspicious links."),

        ("📱", "Mobile Security",
         "Protect your phone, apps and personal information."),

        ("💳", "Online Payments",
         "Learn how to recognize payment scams and fake offers."),

        ("👥", "Social Engineering",
         "Understand how attackers manipulate people."),

        ("🦠", "Malware",
         "Learn about malicious software and how to avoid it."),

        ("🔒", "Privacy",
         "Protect your personal information online."),

        ("🤖", "AI-related Scams",
         "Understand deepfakes, AI impersonation and modern scams.")
    ]

    cols = st.columns(2)

    for i, topic in enumerate(topics):

        with cols[i % 2]:

            st.markdown(
                f"""
                <div class="card">
                <h3>{topic[0]} {topic[1]}</h3>
                <p class="card-text">{topic[2]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

elif page == "🛡️ Safety Score":

    st.title("🛡️ Your Cyber Safety Score")

    score = 82

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="card" style="text-align:center;">
            <div class="score">{score}/100</div>
            <h2>GOOD</h2>
            <p class="small-text">
            You're on the right track. Keep improving your habits.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown("""
        <div class="card">

        <h3>📊 Score Breakdown</h3>

        🔐 Password Security — <b>90/100</b>
        <br><br>

        🎣 Phishing Awareness — <b>75/100</b>
        <br><br>

        🔑 MFA Usage — <b>80/100</b>
        <br><br>

        🚨 Scam Awareness — <b>70/100</b>
        <br><br>

        📚 General Knowledge — <b>85/100</b>

        </div>
        """, unsafe_allow_html=True)

    st.subheader("💡 Recommendations")

    st.success("✅ Use unique passwords")
    st.success("✅ Enable MFA on important accounts")
    st.warning("⚠️ Improve phishing awareness")
    st.warning("⚠️ Complete the scam-awareness module")


elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.toggle("🔔 Security notifications", value=True)

    st.toggle("🌙 Dark mode", value=True)

    st.toggle("🤖 AI assistant", value=True)

    st.selectbox(
        "Language",
        ["English", "Telugu", "Hindi"]
    )

    st.success("Settings saved locally for this demo.")

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#7182a8;">
    🛡️ <b>CyberGuard AI</b><br>
    Cybersecurity isn't just a technology; it's a mindset.
    Stay alert. Stay safe.
    </div>
    """,
    unsafe_allow_html=True
)