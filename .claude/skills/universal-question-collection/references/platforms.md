# Supported-host adaptation

These are capability requirements, not invented APIs. Platform availability changes. Read the actual tools' instructions each session.

| Host | Required discovery | Fallback |
|---|---|---|
| ChatGPT Work | Official connected browser integration, live tabs, supported observations and actions | Ask user to connect the desired browser when absent; never substitute an unrelated cloud session |
| Claude with browser control | Discover its installed browser/desktop tools and their permission rules | Use supported visible observations; do not assume ChatGPT locator methods exist |
| Claude Code | Confirm a browser connector or computer-use capability is installed and authorized | Shell access alone is not permission or a browser connection; request the missing connection |
| Other agents | Browser tool documentation, session inventory, read/click/wait and optional download capabilities | State missing capabilities precisely; preserve partial outputs |

AX trees, DOM snapshots, screenshots and ordinary UI locators are possible observation/action types. Use only those actually documented. Read rendered content, not hidden stores or private endpoints. Browser downloads may be on a remote host; verify where files landed before saying they exist on the user's computer. For images use supported page-asset export, visible-image download or a tightly cropped screenshot; otherwise record the missing dependency.

Stage 1 scripts require local Node.js 18+; check availability. They do not install connectors, authenticate, automate browsers or install this Skill. Without Node, follow the schema using available file tools and disclose that utility validation was unavailable. Stage 2 additionally needs Python 3.9+, PyMuPDF (`pip install pymupdf`) and Playwright with Chromium; `python3 scripts/stage2/stage2.py doctor` checks all of it.

For private Skill installation, inspect the current host UI. A Create/Upload flow may be under Plugins/Skills. Upload only the Skill package, inspect its permissions and privacy, then verify the resulting installed/created entry. Do not confuse local storage, an attachment in a chat, and account installation. Follow host confirmation requirements. Never publish or install into another product merely because it uses the same package format.
