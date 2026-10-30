"""Capture the actual locally built Zen window through Marionette."""
import base64
import json
import os
from pathlib import Path
import sys
import time

from marionette_driver.marionette import Marionette

ROOT = Path('/home/luap/zen-desktop')
OUT = ROOT / '.surfer/validation'
label = sys.argv[1]
os.environ['DISPLAY'] = ':99'
os.environ['MOZ_ENABLE_WAYLAND'] = '0'
prefs = {
    'zen.welcome-screen.seen': True,
    'zen.updates.show-update-notification': False,
    'browser.shell.checkDefaultBrowser': False,
    'browser.startup.page': 0,
    'browser.startup.homepage': 'about:blank',
    'datareporting.policy.dataSubmissionPolicyBypassNotification': True,
    'zen.view.use-single-toolbar': False,
    'zen.view.sidebar-expanded': True,
    'zen.tabs.vertical.right-side': True,
    'zen.view.compact.hide-tabbar': True,
    'zen.view.compact.hide-toolbar': False,
    'zen.view.hide-window-controls': True,
    'zen.workspaces.continue-where-left-off': False,
}
m = Marionette(bin=str(ROOT / 'engine/obj-x86_64-pc-linux-gnu/dist/bin/zen'),
               prefs=prefs, app_args=['--remote-allow-system-access'],
               startup_timeout=120)
try:
    m.start_session()
    old_handles = set(m.window_handles)
    m.set_context('chrome')
    m.execute_script('gBrowser.selectedTab = gBrowser.addTrustedTab("about:blank")')
    m.switch_to_window(next(h for h in m.window_handles if h not in old_handles))
    m.set_context('content')
    m.navigate('about:preferences')
    m.set_context('chrome')
    m.set_window_rect(x=0, y=0, width=1280, height=800)
    time.sleep(16)
    print(m.execute_script('return {title: document.title, ready: !!window.gZenCompactModeManager, attrs: document.documentElement.getAttributeNames()}'), flush=True)
    results = []
    for state, enabled in [('expanded', False), ('compact', True), ('reopened', False)]:
        m.execute_script('if (gZenCompactModeManager.preference !== arguments[0]) document.getElementById("cmd_toggleCompactModeIgnoreHover").doCommand()', [enabled])
        for _ in range(100):
            if m.execute_script('return gZenCompactModeManager.preference === arguments[0] && !document.documentElement.hasAttribute("zen-compact-animating")', [enabled]):
                break
            time.sleep(.1)
        else:
            raise RuntimeError('Compact mode did not settle')
        time.sleep(1)
        metrics = m.execute_script('''
          const ids = ['zen-toggle-compact-mode', 'zen-sidebar-top-buttons-customization-target', 'navigator-toolbox', 'PanelUI-button'];
          return Object.fromEntries(ids.map(id => {
            const el = document.getElementById(id), r = el.getBoundingClientRect();
            return [id, {x:r.x, y:r.y, width:r.width, height:r.height, parent:el.parentElement.id}];
          }));
        ''')
        results.append({'state': state, 'metrics': metrics})
        (OUT / f'{label}-{state}.png').write_bytes(base64.b64decode(m.screenshot()))
        print(state, metrics, flush=True)
    (OUT / f'{label}-metrics.json').write_text(json.dumps(results, indent=2))
finally:
    if m.session:
        m.quit()
    m.cleanup()
