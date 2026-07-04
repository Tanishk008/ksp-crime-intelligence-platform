import { useState, useEffect } from 'react';
import { CREST_SRC } from './assets/crest';
import './App.css';

/* ============================================================
   ICONS — consistent stroke system, 24px grid, 1.75 stroke
   ============================================================ */
export const ICONS = {
  search: <><circle cx="10.5" cy="10.5" r="6.5"/><line x1="20.5" y1="20.5" x2="15.3" y2="15.3"/></>,
  bell: <><path d="M6 16.5v-5a6 6 0 1 1 12 0v5l2 2H4l2-2z"/><path d="M10 20a2 2 0 0 0 4 0"/></>,
  user: <><circle cx="12" cy="8" r="4"/><path d="M4 20.5c0-4.2 4-6.5 8-6.5s8 2.3 8 6.5"/></>,
  chevronDown: <><polyline points="6 9 12 15 18 9"/></>,
  chevronRight: <><polyline points="9 6 15 12 9 18"/></>,
  globe: <><circle cx="12" cy="12" r="9"/><line x1="3" y1="12" x2="21" y2="12"/><path d="M12 3c3 3.6 3 14.4 0 18M12 3c-3 3.6-3 14.4 0 18"/></>,
  mic: <><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><line x1="12" y1="18" x2="12" y2="22"/></>,
  send: <><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></>,
  workspace: <><path d="M4 5h16v11H8l-4 4V5z"/></>,
  network: <><circle cx="6" cy="6" r="2.3"/><circle cx="18" cy="6" r="2.3"/><circle cx="12" cy="18" r="2.3"/><line x1="8.1" y1="7.1" x2="15.9" y2="7.1"/><line x1="7" y1="8.1" x2="10.8" y2="15.8"/><line x1="17" y1="8.1" x2="13.2" y2="15.8"/></>,
  map: <><path d="M12 22s7-7.6 7-12.6A7 7 0 1 0 5 9.4C5 14.4 12 22 12 22z"/><circle cx="12" cy="9.4" r="2.2"/></>,
  cases: <><path d="M3 6.5h6l2 2h10v10.5H3V6.5z"/></>,
  reports: <><path d="M6.5 2h9l5 5v15h-14V2z"/><line x1="9" y1="12" x2="16.5" y2="12"/><line x1="9" y1="16" x2="16.5" y2="16"/></>,
  admin: <><path d="M12 2.2l8 3v6c0 5-3.5 8.7-8 11-4.5-2.3-8-6-8-11v-6l8-3z"/></>,
  settings: <><circle cx="12" cy="12" r="3"/><path d="M19.4 12a7.4 7.4 0 0 0-.1-1.2l2-1.5-2-3.4-2.3.9a7.3 7.3 0 0 0-2-1.2L14.6 3H9.4l-.6 2.6a7.3 7.3 0 0 0-2 1.2l-2.3-.9-2 3.4 2 1.5a7.4 7.4 0 0 0 0 2.4l-2 1.5 2 3.4 2.3-.9c.6.5 1.3.9 2 1.2L9.4 21h5.2l.6-2.6c.7-.3 1.4-.7 2-1.2l2.3.9 2-3.4-2-1.5c.1-.4.1-.8.1-1.2z"/></>,
  menu: <><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></>,
  x: <><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></>,
  filter: <><polygon points="4 4 20 4 14 12.5 14 19 10 21 10 12.5 4 4"/></>,
  download: <><path d="M12 3v12"/><polyline points="7 11 12 16 17 11"/><path d="M5 19h14"/></>,
  plus: <><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></>,
  panel: <><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="15" y1="4" x2="15" y2="20"/></>,
  zoomIn: <><circle cx="10.5" cy="10.5" r="6.5"/><line x1="20.5" y1="20.5" x2="15.3" y2="15.3"/><line x1="10.5" y1="7.5" x2="10.5" y2="13.5"/><line x1="7.5" y1="10.5" x2="13.5" y2="10.5"/></>,
  zoomOut: <><circle cx="10.5" cy="10.5" r="6.5"/><line x1="20.5" y1="20.5" x2="15.3" y2="15.3"/><line x1="7.5" y1="10.5" x2="13.5" y2="10.5"/></>,
  layers: <><polygon points="12 3 21 8 12 13 3 8 12 3"/><polyline points="3 15 12 20 21 15"/><polyline points="3 11.5 12 16.5 21 11.5"/></>,
};

export function Ic({ name, cls = 'ic' }: { name: keyof typeof ICONS; cls?: string }) {
  return (
    <svg className={cls} viewBox="0 0 24 24">
      {ICONS[name]}
    </svg>
  );
}

/* ============================================================
   REUSABLE UI COMPONENTS
   ============================================================ */

interface PanelBlockProps {
  label: string;
  head?: string;
  headRight?: React.ReactNode;
  cls?: string;
  children?: React.ReactNode;
}

function PanelBlock({ label, head, headRight, cls = '', children }: PanelBlockProps) {
  return (
    <div className={`panel-block ${cls}`}>
      <span className="structure-tag">{label}</span>
      {head && (
        <div className="block-head">
          <h4>{head}</h4>
          {headRight}
        </div>
      )}
      {children}
    </div>
  );
}

function Badge({ text, kind = 'neutral' }: { text: string; kind?: string }) {
  return (
    <span className={`badge badge-${kind}`}>
      <span className="dot"></span>
      {text}
    </span>
  );
}

function Chip({ text }: { text: React.ReactNode }) {
  return <span className="chip" dangerouslySetInnerHTML={{ __html: String(text) }}></span>;
}

interface BtnProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  text: React.ReactNode;
  kind?: 'primary' | 'secondary' | 'ghost';
  extra?: React.ReactNode;
}

function Btn({ text, kind = 'secondary', extra, ...props }: BtnProps) {
  const cls = kind === 'primary' ? 'btn btn-primary' : kind === 'ghost' ? 'btn btn-ghost' : 'btn';
  return (
    <button className={cls} {...props}>
      {extra}
      {text}
    </button>
  );
}

function Confidence({ n, labelText }: { n: number; labelText?: string }) {
  const segs = [];
  for (let i = 1; i <= 5; i++) {
    segs.push(<span key={i} className={`seg ${i <= n ? 'on' : ''}`}></span>);
  }
  return (
    <span className="confidence">
      <span className="segs">{segs}</span>
      {labelText && <span className="lbl">{labelText}</span>}
    </span>
  );
}

interface TableProps {
  headers: string[];
  rows: React.ReactNode[][];
}

function Table({ headers, rows }: TableProps) {
  return (
    <div className="table-wrap">
      <table className="table">
        <thead>
          <tr>
            {headers.map((h, i) => (
              <th key={i}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, ri) => (
            <tr key={ri}>
              {r.map((c, ci) => (
                <td key={ci}>{c}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Pagination({ text }: { text: string }) {
  return (
    <div className="pagination">
      <span>{text}</span>
      <div className="pg-btns">
        <button><Ic name="chevronRight" cls="ic-sm" /></button>
        <button className="on">1</button>
        <button>2</button>
        <button style={{ transform: 'scaleX(-1)' }}><Ic name="chevronRight" cls="ic-sm" /></button>
      </div>
    </div>
  );
}

interface FieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  placeholder: string;
}

function Field({ label, placeholder, type = 'text', ...props }: FieldProps) {
  return (
    <div className="field">
      <label>{label}</label>
      <input className="input" type={type} placeholder={placeholder} {...props} />
    </div>
  );
}

function Kv({ rows }: { rows: [string, React.ReactNode][] }) {
  return (
    <div>
      {rows.map(([k, v], i) => (
        <div className="kv" key={i}>
          <span className="k">{k}</span>
          <span className="v">{v}</span>
        </div>
      ))}
    </div>
  );
}

function PlaceholderCanvas({ iconName, label, note, height = '360px' }: { iconName: keyof typeof ICONS; label: string; note?: string; height?: string }) {
  return (
    <div className="placeholder-canvas" style={{ height }}>
      <div className="pc-icon"><Ic name={iconName} cls="ic-lg" /></div>
      <div className="pc-label">{label}</div>
      {note && <div className="pc-note">{note}</div>}
    </div>
  );
}

/* ============================================================
   NAVIGATION ITEMS
   ============================================================ */
const NAV_ITEMS = [
  { id: 'workspace', label: 'Investigation Workspace', icon: 'workspace' as keyof typeof ICONS },
  { id: 'search', label: 'Search', icon: 'search' as keyof typeof ICONS },
  { id: 'network', label: 'Network Explorer', icon: 'network' as keyof typeof ICONS },
  { id: 'map', label: 'Crime Map', icon: 'map' as keyof typeof ICONS },
  { id: 'cases', label: 'Cases', icon: 'cases' as keyof typeof ICONS },
  { id: 'profiles', label: 'Profiles', icon: 'user' as keyof typeof ICONS },
  { id: 'reports', label: 'Reports', icon: 'reports' as keyof typeof ICONS },
  { id: 'alerts', label: 'Alerts', icon: 'bell' as keyof typeof ICONS },
  { id: 'admin', label: 'Administration', icon: 'admin' as keyof typeof ICONS },
  { id: 'settings', label: 'Settings', icon: 'settings' as keyof typeof ICONS },
];

/* ============================================================
   SCREEN REGISTRY DEFINITIONS
   ============================================================ */
interface ScreenConfig {
  key: string;
  navLabel: string;
  shell: boolean;
  title?: string;
  breadcrumb?: string[];
  activeNav?: string;
  caseLabel?: string | null;
  subtitle?: string;
  actions?: { text: string; kind?: 'primary' | 'secondary' | 'ghost' }[];
  hideHead?: boolean;
}

const SCREENS: ScreenConfig[] = [
  { key: 'legend', navLabel: 'Design System', shell: false },
  { key: 'login', navLabel: 'Login', shell: false },
  { key: 'workspace', navLabel: 'Investigation Workspace', shell: true, title: 'Investigation Workspace', activeNav: 'workspace', caseLabel: 'CR-2024-04471', hideHead: true },
  { key: 'search', navLabel: 'Search', shell: true, title: 'Search', breadcrumb: ['Search'], activeNav: 'search', caseLabel: null },
  { key: 'case', navLabel: 'Case Profile', shell: true, title: 'Case Profile', breadcrumb: ['Cases', 'CR-2024-04471'], activeNav: 'cases', caseLabel: 'CR-2024-04471', hideHead: true },
  { key: 'entity', navLabel: 'Entity Profile', shell: true, title: 'Entity Profile', breadcrumb: ['Profiles', 'Raju Kumar'], activeNav: 'profiles', caseLabel: null, hideHead: true },
  { key: 'network', navLabel: 'Network Explorer', shell: true, title: 'Network Explorer', breadcrumb: ['Network Explorer', 'Context: CR-2024-04471'], activeNav: 'network', caseLabel: 'CR-2024-04471' },
  { key: 'timeline', navLabel: 'Timeline', shell: true, title: 'Timeline', breadcrumb: ['Cases', 'CR-2024-04471', 'Timeline'], activeNav: 'cases', caseLabel: 'CR-2024-04471', subtitle: 'Reached contextually from a case — not a top-level nav destination.' },
  { key: 'map', navLabel: 'Crime Map', shell: true, title: 'Crime Map', breadcrumb: ['Crime Map'], activeNav: 'map', caseLabel: null },
  { key: 'reports', navLabel: 'Reports', shell: true, title: 'Reports', breadcrumb: ['Reports'], activeNav: 'reports', caseLabel: null, actions: [{ text: 'New Report', kind: 'primary' }] },
  { key: 'alerts', navLabel: 'Alerts', shell: true, title: 'Alerts', breadcrumb: ['Alerts'], activeNav: 'alerts', caseLabel: null },
  { key: 'admin', navLabel: 'Administration', shell: true, title: 'Administration', breadcrumb: ['Administration'], activeNav: 'admin', caseLabel: null },
  { key: 'settings', navLabel: 'Settings', shell: true, title: 'Settings', breadcrumb: ['Settings'], activeNav: 'settings', caseLabel: null }
];

export function App() {
  const [currentScreen, setCurrentScreen] = useState<string>('legend');
  const [showAnnotations, setShowAnnotations] = useState<boolean>(false);
  
  // Scrim and Collapsible Overlays
  const [navOpen, setNavOpen] = useState<boolean>(false);
  const [panelOpen, setPanelOpen] = useState<boolean>(false);

  // Expanded reasoning sets
  const [expandedReasoning, setExpandedReasoning] = useState<Record<string, boolean>>({});

  // Active Tab Indices mapping
  const [activeTabs, setActiveTabs] = useState<Record<string, number>>({
    'case-tabs': 0,
    'admin-tabs': 0
  });

  // Selected row state for details drawer
  const [selectedCaseRow, setSelectedCaseRow] = useState<string | null>(null);

  // Sync annotations class to body for the CSS selector
  useEffect(() => {
    if (showAnnotations) {
      document.body.classList.add('show-annotations');
    } else {
      document.body.classList.remove('show-annotations');
    }
  }, [showAnnotations]);

  // Scrim Overlay Controllers
  const closeOverlays = () => {
    setNavOpen(false);
    setPanelOpen(false);
  };

  const handleScreenChange = (key: string) => {
    setCurrentScreen(key);
    closeOverlays();
    window.scrollTo(0, 0);
  };

  const toggleReasoning = (id: string) => {
    setExpandedReasoning(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const handleTabChange = (groupId: string, index: number) => {
    setActiveTabs(prev => ({
      ...prev,
      [groupId]: index
    }));
  };

  /* ============================================================
     RENDER REUSABLE INNER WORKSPACE BLOCKS & TEMPLATES
     ============================================================ */
  const renderReasoningToggle = (id: string, text: string) => {
    const isOpen = !!expandedReasoning[id];
    return (
      <>
        <div className={`reasoning-toggle ${isOpen ? 'open' : ''}`} onClick={() => toggleReasoning(id)}>
          <Ic name="chevronRight" cls="ic-sm chev" />
          <span>{isOpen ? 'Collapse reasoning trace' : 'Expand reasoning trace'}</span>
        </div>
        <div className={`reasoning-body ${isOpen ? 'open' : ''}`} id={id}>
          {text}
        </div>
      </>
    );
  };

  const renderTabsBlock = (groupId: string, tabs: string[], panes: React.ReactNode[]) => {
    const activeIndex = activeTabs[groupId] ?? 0;
    return (
      <>
        <div className="tabs">
          {tabs.map((t, idx) => (
            <div
              key={idx}
              className={`tab ${idx === activeIndex ? 'active' : ''}`}
              onClick={() => handleTabChange(groupId, idx)}
            >
              {t}
            </div>
          ))}
        </div>
        {panes.map((p, idx) => (
          <div key={idx} className={`tab-pane ${idx === activeIndex ? 'active' : ''}`}>
            {p}
          </div>
        ))}
      </>
    );
  };

  /* ============================================================
     SCREEN VIEW RENDERERS
     ============================================================ */

  const renderLegendView = () => (
    <div className="legend-wrap">
      <h1 style={{ fontSize: '23px', marginBottom: '4px', fontWeight: 700 }}>Design System Reference</h1>
      <p style={{ color: 'var(--n-500)', fontSize: '13px', marginBottom: '30px' }}>
        High-fidelity visual system derived from the official Karnataka State Police crest. This page documents the tokens — it is not a product screen.
      </p>

      <h2 className="section-h">Color — Primary (from the crest shield)</h2>
      <div className="legend-swatch">
        <div className="color-chip"><div className="sw" style={{ background: 'var(--navy-900)' }}></div><div className="cn">navy-900</div><div className="cv">#101A33</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--navy-700)' }}></div><div className="cn">navy-700</div><div className="cv">#1D2F5E</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--navy-600)' }}></div><div className="cn">navy-600</div><div className="cv">#26397A</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--navy-500)' }}></div><div className="cn">navy-500</div><div className="cv">#2F4A94</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--navy-100)' }}></div><div className="cn">navy-100</div><div className="cv">#E7EBF6</div></div>
      </div>
      <p style={{ fontSize: '12px', color: 'var(--n-500)', marginTop: '10px' }}>
        Used for: primary actions, active navigation, links, focus rings, selected rows. This is the only color used for interactive/functional state.
      </p>

      <h2 className="section-h" style={{ marginTop: '26px' }}>Signature accent (from the crest's gold ribbon)</h2>
      <div className="legend-swatch">
        <div className="color-chip"><div className="sw" style={{ background: 'var(--gold-500)' }}></div><div className="cn">gold-500</div><div className="cv">#B8862E</div></div>
      </div>
      <p style={{ fontSize: '12px', color: 'var(--n-500)', marginTop: '10px' }}>
        Used in exactly two places platform-wide: the 3px header hairline and the login card's top edge. Reserved as a signature touch — never used for interactive elements, to keep daily-use surfaces calm.
      </p>

      <h2 className="section-h" style={{ marginTop: '26px' }}>Semantic colors (status only — never decorative)</h2>
      <div className="legend-swatch">
        <div className="color-chip"><div className="sw" style={{ background: 'var(--success-600)' }}></div><div className="cn">success</div><div className="cv">from crest green</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--warning-600)' }}></div><div className="cn">warning</div><div className="cv">from crest gold</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--critical-600)' }}></div><div className="cn">critical</div><div className="cv">from crest maroon</div></div>
        <div className="color-chip"><div className="sw" style={{ background: 'var(--n-600)' }}></div><div className="cn">neutral</div><div className="cv">#565C66</div></div>
      </div>
      <p style={{ fontSize: '12px', color: 'var(--n-500)', marginTop: '10px' }}>
        Confidence indicators are deliberately <b>not</b> mapped to this scale — certainty is a neutral navy measure, not a status judgement (low confidence isn't an "error").
      </p>

      <h2 className="section-h" style={{ marginTop: '26px' }}>Typography</h2>
      <div style={{ font: '700 22px var(--font-ui)' }}>Aa — IBM Plex Sans (UI & headings)</div>
      <div className="kn" style={{ font: '600 20px "Noto Sans Kannada"', marginTop: '8px' }}>ಕರ್ನಾಟಕ ರಾಜ್ಯ ಪೊಲೀಸ್ — Noto Sans Kannada (paired for parity)</div>
      <div style={{ font: '600 15px var(--font-mono)', marginTop: '8px', color: 'var(--n-700)' }}>CR-2024-04471 — IBM Plex Mono (case numbers, codes, confidence)</div>
      <p style={{ fontSize: '12px', color: 'var(--n-500)', marginTop: '12px' }}>
        For production deployment on Karnataka SDC infrastructure, self-host these three font families rather than depending on an external CDN at runtime, consistent with the sovereign-infrastructure requirements established in the platform's architecture blueprint.
      </p>

      <h2 className="section-h" style={{ marginTop: '26px' }}>Component samples</h2>
      <div className="legend-swatch" style={{ marginBottom: '14px' }}>
        <Btn text="Primary Action" kind="primary" />{' '}
        <Btn text="Secondary Action" />{' '}
        <Btn text="Ghost" kind="ghost" />{' '}
        <Btn text="Disabled" disabled />
      </div>
      <div className="legend-swatch" style={{ marginBottom: '14px' }}>
        <Badge text="ACTIVE" kind="success" />{' '}
        <Badge text="PENDING FSL" kind="warning" />{' '}
        <Badge text="HIGH" kind="critical" />{' '}
        <Badge text="CLOSED" kind="neutral" />{' '}
        <Badge text="CASE MATCH" kind="info" />
      </div>
      <div style={{ marginBottom: '14px' }}>
        <Confidence n={4} labelText="High confidence" />
      </div>
      <div style={{ maxWidth: '340px' }}>
        <Field label="Input — default" placeholder="Placeholder text" />
      </div>
      <div style={{ maxWidth: '340px' }}>
        <div className="field">
          <label>Input — error state</label>
          <input className="input error" type="text" placeholder="Required field" />
          <div className="field-error"><span className="conflict-flag" style={{ width: '14px', height: '14px', fontSize: '9px' }}>!</span> This field has errors.</div>
        </div>
      </div>

      <h2 className="section-h" style={{ marginTop: '26px' }}>Shell invariants (unchanged from approved wireframe)</h2>
      <ul style={{ fontSize: '12.5px', color: 'var(--n-600)', lineHeight: 1.9 }}>
        <li>Header: 60px, crest + product name, case selector, spacer, language, notifications, profile — always in that order.</li>
        <li>Left navigation: fixed 10-item order, never added to or reordered. Collapses to an icon rail below 1200px, an off-canvas drawer below 768px.</li>
        <li>Right context panel: 328px, becomes an off-canvas overlay below 1024px.</li>
        <li>Only the visual system changed in this pass — information architecture, navigation order, and component placement are exactly as approved.</li>
      </ul>

      <h2 className="section-h" style={{ marginTop: '26px' }}>Reviewing structure labels</h2>
      <p style={{ fontSize: '12.5px', color: 'var(--n-500)' }}>
        Use the "Annotations" toggle in the reference bar above to overlay the component-boundary labels from the approved wireframe phase, for cross-reference during handoff.
      </p>
    </div>
  );

  const renderLoginView = () => (
    <div className="login-wrap">
      <div className="login-card">
        <img className="crest" src={CREST_SRC} alt="Karnataka State Police crest" />
        <h1>KSP Crime Intelligence Platform</h1>
        <div className="sub">Karnataka State Police &middot; SCRB</div>
        <Field label="Badge / Employee ID" placeholder="e.g. KSP-44210" />
        <Field label="Password" placeholder="••••••••" type="password" />
        <Btn text="Sign In" kind="primary" onClick={() => handleScreenChange('workspace')} />
        <div className="login-foot">Authorized personnel only<span className="sep">&middot;</span>All access is logged and audited</div>
      </div>
    </div>
  );

  const renderWorkspaceView = () => (
    <>
      <PanelBlock label="CONVERSATION PANEL">
        <div className="msg">
          <span className="avatar">SR</span>
          <div className="msg-bubble" style={{ maxWidth: '520px' }}>
            <div className="msg-meta">User</div>
            <div className="msg-body">Has this MO appeared elsewhere in Karnataka in 2024?</div>
          </div>
        </div>
        <div className="msg" style={{ maxWidth: '640px' }}>
          <span className="avatar ai">AI</span>
          <div className="msg-bubble">
            <div className="msg-meta">AI Response &nbsp;<Confidence n={3} labelText="Moderate" /></div>
            <div className="msg-body">3 similar cases found based on modus-operandi similarity: CR-2023-11201 (Tumkur), CR-2024-00892 (Mysuru), CR-2024-03107 (Bengaluru).</div>
            <div className="source-row">
              <span className="source-chip">IIF-1 &middot; CR-2023-11201</span>
              <span className="source-chip">IIF-1 &middot; CR-2024-00892</span>
              <span className="source-chip">IIF-1 &middot; CR-2024-03107</span>
            </div>
            {renderReasoningToggle(
              'rz_mo_similarity',
              'Matched on: weapon type (2/3), entry method (3/3), time-of-day window (2/3). Diagnosticity favors CR-2023-11201 most strongly — all three attributes align.'
            )}
          </div>
        </div>
        <div className="msg" style={{ maxWidth: '640px' }}>
          <span className="avatar ai">AI</span>
          <div className="msg-bubble">
            <div className="msg-meta">AI Response &nbsp;<Confidence n={4} labelText="High" /></div>
            <div className="msg-body">Phone CDR places the suspect in Whitefield at 21:40. This conflicts with a witness statement placing them at the scene at the same time.</div>
            <div className="conflict-box">
              <div className="conflict-head"><span className="conflict-flag">!</span> Conflicting evidence</div>
              <p>Source A (CDR) and Source B (Witness) cannot both be correct. Neither has been discounted.</p>
              <Btn text="Investigate conflict" kind="secondary" onClick={() => handleScreenChange('timeline')} />
            </div>
          </div>
        </div>
      </PanelBlock>

      <PanelBlock label="QUERY INPUT">
        <div className="query-bar">
          <div className="icon-btn-inline"><Ic name="mic" /></div>
          <input placeholder="Ask anything about this case — English or ಕನ್ನಡ" />
          <div className="icon-btn-inline primary"><Ic name="send" /></div>
        </div>
      </PanelBlock>

      <PanelBlock label="VISUALIZATION LAUNCHERS">
        <div className="filter-bar">
          <Btn text="← Timeline" onClick={() => handleScreenChange('timeline')} />
          <Btn text="Network &nearr;" onClick={() => handleScreenChange('network')} />
          <Btn text="Map &nearr;" onClick={() => handleScreenChange('map')} />
        </div>
      </PanelBlock>
    </>
  );

  const renderWorkspaceRight = () => (
    <>
      <PanelBlock label="CASE CONTEXT CARD" head="Overview">
        <Kv rows={[
          ['Case No.', 'CR-2024-04471'],
          ['Type', 'Robbery'],
          ['Status', <Badge text="ACTIVE" kind="success" />],
          ['IO', 'SI Ravi Kumar']
        ]} />
      </PanelBlock>

      <PanelBlock label="HYPOTHESIS LIST" head="Live Hypotheses">
        <div className="hyp-card">
          <span className="hyp-name">H1 — Known recidivist</span>
          <Confidence n={3} />
        </div>
        <div className="hyp-card">
          <span className="hyp-name">H2 — Organised group</span>
          <Confidence n={2} />
        </div>
        <div style={{ marginTop: '10px' }}>
          <Btn text="+ Add note" kind="ghost" />
        </div>
      </PanelBlock>

      <PanelBlock label="OPEN QUESTIONS" head="Open Questions">
        <div className="list">
          <div className="list-item">Weapon source unconfirmed</div>
          <div className="list-item">Third associate unidentified</div>
        </div>
      </PanelBlock>
    </>
  );

  const renderSearchView = () => (
    <>
      <PanelBlock label="GLOBAL SEARCH">
        <div className="search-bar">
          <Ic name="search" />
          <input placeholder="Search cases, suspects, MO, locations — English or ಕನ್ನಡ" />
          <Ic name="mic" />
        </div>
      </PanelBlock>

      <PanelBlock label="FILTERS">
        <div className="filter-bar">
          <span className="filter-chip">Type <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">Date Range <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">District <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">Status <Ic name="chevronDown" cls="ic-sm" /></span>
        </div>
      </PanelBlock>

      <div className="canvas-relative">
        <PanelBlock label="RESULTS">
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Case No.</th>
                  <th>Type</th>
                  <th>District</th>
                  <th>Status</th>
                  <th>Match Confidence</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr className={selectedCaseRow === 'CR-2024-04471' ? 'selected' : ''} onClick={() => setSelectedCaseRow('CR-2024-04471')}>
                  <td>CR-2024-04471</td>
                  <td>Robbery</td>
                  <td>Koramangala</td>
                  <td><Badge text="ACTIVE" kind="success" /></td>
                  <td><Confidence n={3} /></td>
                  <td><Btn text="Open" kind="ghost" onClick={() => handleScreenChange('case')} /></td>
                </tr>
                <tr className={selectedCaseRow === 'CR-2023-11201' ? 'selected' : ''} onClick={() => setSelectedCaseRow('CR-2023-11201')}>
                  <td>CR-2023-11201</td>
                  <td>Robbery</td>
                  <td>Tumkur</td>
                  <td><Badge text="CLOSED" kind="neutral" /></td>
                  <td><Confidence n={4} /></td>
                  <td><Btn text="Open" kind="ghost" onClick={() => handleScreenChange('case')} /></td>
                </tr>
                <tr className={selectedCaseRow === 'CR-2024-00892' ? 'selected' : ''} onClick={() => setSelectedCaseRow('CR-2024-00892')}>
                  <td>CR-2024-00892</td>
                  <td>Robbery</td>
                  <td>Mysuru</td>
                  <td><Badge text="ACTIVE" kind="success" /></td>
                  <td><Confidence n={4} /></td>
                  <td><Btn text="Open" kind="ghost" onClick={() => handleScreenChange('case')} /></td>
                </tr>
              </tbody>
            </table>
          </div>
          <Pagination text="Showing 1–10 of 47 results" />
        </PanelBlock>

        {selectedCaseRow && (
          <div className="drawer" style={{ display: 'block' }}>
            <span className="drawer-eyebrow">Row Detail</span>
            <div className="drawer-head">
              <b style={{ fontSize: '14px' }}>{selectedCaseRow}</b>
              <span className="drawer-close" onClick={() => setSelectedCaseRow(null)}>
                <Ic name="x" cls="ic-sm" />
              </span>
            </div>
            <Kv rows={[
              ['Type', 'Robbery'],
              ['District', selectedCaseRow === 'CR-2023-11201' ? 'Tumkur' : selectedCaseRow === 'CR-2024-00892' ? 'Mysuru' : 'Koramangala'],
              ['Status', <Badge text={selectedCaseRow === 'CR-2023-11201' ? 'CLOSED' : 'ACTIVE'} kind={selectedCaseRow === 'CR-2023-11201' ? 'neutral' : 'success'} />],
              ['MO Match', 'High']
            ]} />
            <div style={{ marginTop: '14px' }}>
              <Btn text="Open Full Case &nearr;" kind="primary" onClick={() => handleScreenChange('case')} />
            </div>
          </div>
        )}
      </div>
    </>
  );

  const renderCaseProfileView = () => (
    <>
      <PanelBlock label="CASE HEADER">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ fontSize: '16.5px', fontWeight: 700 }}>CR-2024-04471 — Robbery</div>
            <div style={{ color: 'var(--n-500)', marginTop: '3px', fontSize: '12.5px' }}>
              Koramangala P.S. &middot; Assigned: SI Ravi Kumar
            </div>
            <div style={{ marginTop: '9px' }}>
              <Badge text="ACTIVE" kind="success" />
            </div>
          </div>
          <div className="actions">
            <Btn text="Ask AI about this case" kind="secondary" onClick={() => handleScreenChange('workspace')} />
            <Btn text="Export PDF" kind="primary" />
          </div>
        </div>
      </PanelBlock>

      {renderTabsBlock(
        'case-tabs',
        ['Overview', 'Evidence', 'Entities', 'Timeline', 'Narrative'],
        [
          <div key="overview">
            <PanelBlock label="FACTS" head="Timeline Facts">
              <div className="list">
                <div className="list-item"><span>Incident reported 15-Sep-2024, Koramangala</span><span className="source-chip">FIR</span></div>
                <div className="list-item"><span>Suspect identified via witness statement</span><span className="source-chip">Case Diary</span></div>
                <div className="list-item"><span>Arrest made 30-Sep-2024</span><span className="source-chip">Case Diary</span></div>
              </div>
            </PanelBlock>
            <PanelBlock label="LINKED ENTITIES" head="Relationships">
              <div className="filter-bar">
                <Chip text="Raju Kumar — Accused" />
                <Chip text="Suresh M. — Associate" />
                <Chip text="9880-XXXX — Phone" />
              </div>
            </PanelBlock>
          </div>,
          <PanelBlock label="EXHIBITS" head="Artifact Ledger" key="evidence">
            <Table
              headers={['Exhibit ID', 'Type', 'Status', 'Chain of Custody']}
              rows={[
                ['EX-001', 'Weapon', <Badge text="LOGGED" kind="success" />, 'Verified'],
                ['EX-002', 'CCTV Footage', <Badge text="LOGGED" kind="success" />, 'Verified'],
                ['EX-003', 'Phone CDR', <Badge text="PENDING FSL" kind="warning" />, '—']
              ]}
            />
          </PanelBlock>,
          <PanelBlock label="ENTITIES" head="Associated Persons / Objects" key="entities">
            <div className="filter-bar">
              <Chip text="Raju Kumar" />
              <Chip text="Suresh M." />
              <Chip text="9880-XXXX" />
            </div>
          </PanelBlock>,
          <PanelBlock label="TIMELINE" head="Chronological Chain" key="timeline">
            <PlaceholderCanvas iconName="map" label="Timeline preview" note="Open the full Timeline view from Case Context for the interactive version." height="160px" />
          </PanelBlock>,
          <PanelBlock label="NARRATIVE" head="Narrative Record" key="narrative">
            <div style={{ fontSize: '12.5px', color: 'var(--n-700)', lineHeight: '1.7' }}>
              Full case narrative text renders here, sourced from the case diary and FIR, in the language it was originally recorded.
            </div>
          </PanelBlock>
        ]
      )}
    </>
  );

  const renderCaseProfileRight = () => (
    <>
      <PanelBlock label="QUICK STATS" head="Overview">
        <Kv rows={[
          ['Opened', '15-Sep-2024'],
          ['Days Open', '19'],
          ['Linked Cases', '3'],
          ['Exhibits', '3']
        ]} />
      </PanelBlock>
      <PanelBlock label="RELATED CASES" head="Associations">
        <div className="list">
          <div className="list-item">CR-2023-11201 <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>MO match</span></div>
          <div className="list-item">CR-2024-00892 <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>MO match</span></div>
        </div>
      </PanelBlock>
    </>
  );

  const renderEntityProfileView = () => (
    <>
      <PanelBlock label="IDENTITY">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ fontSize: '16.5px', fontWeight: 700 }}>
              Raju Kumar <span style={{ fontWeight: 400, color: 'var(--n-500)', fontSize: '12.5px' }}>— Person</span>
            </div>
            <div style={{ marginTop: '11px' }}>
              <Chip text="Raja K" />
              <Chip text="Raju Sh" />
              <Chip text="ರಾಜು ಕುಮಾರ" />
            </div>
            <div style={{ marginTop: '11px', color: 'var(--n-400)', fontSize: '12px' }}>
              DOB: ░░░░░░ &middot; restricted field
            </div>
          </div>
          <div className="actions">
            <Btn text="Export Profile" kind="secondary" />
          </div>
        </div>
      </PanelBlock>

      <div className="two-col">
        <div className="stack">
          <PanelBlock label="CASE HISTORY" head="Case Involvements">
            <Table
              headers={['Case No.', 'Type', 'Role', 'Date']}
              rows={[
                ['CR-2024-04471', 'Robbery', 'Accused', 'Sep 2024'],
                ['CR-2023-11201', 'Robbery', 'Accused', 'Nov 2023'],
                ['CR-2022-07834', 'Theft', 'Accused', 'Apr 2022']
              ]}
            />
          </PanelBlock>
          <PanelBlock label="ASK ABOUT THIS ENTITY">
            <div className="query-bar">
              <Ic name="mic" />
              <input placeholder="Ask anything about Raju Kumar" />
              <Ic name="send" />
            </div>
          </PanelBlock>
        </div>
        <div className="stack">
          <PanelBlock label="NETWORK PREVIEW" head="Mini Network">
            <PlaceholderCanvas iconName="network" label="Mini Network" height="150px" />
            <div style={{ marginTop: '12px' }}>
              <Btn text="Open Full Network &nearr;" kind="ghost" onClick={() => handleScreenChange('network')} />
            </div>
          </PanelBlock>
          <PanelBlock label="TIMELINE PREVIEW" head="Timeline Summary">
            <PlaceholderCanvas iconName="map" label="Mini Timeline" height="110px" />
            <div style={{ marginTop: '12px' }}>
              <Btn text="Open Full Timeline &nearr;" kind="ghost" onClick={() => handleScreenChange('timeline')} />
            </div>
          </PanelBlock>
        </div>
      </div>
    </>
  );

  const renderEntityProfileRight = () => (
    <PanelBlock label="RELATED" head="Direct Connections">
      <div className="list">
        <div className="list-item">Suresh M. <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>Associate</span></div>
        <div className="list-item">9880-XXXX <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>Shared phone</span></div>
      </div>
    </PanelBlock>
  );

  const renderNetworkExplorerView = () => (
    <>
      <PanelBlock label="GRAPH TOOLBAR">
        <div className="filter-bar">
          <span className="filter-chip"><Ic name="filter" cls="ic-sm" />Filter <Ic name="chevronDown" cls="ic-sm" /></span>
          <div className="search-bar" style={{ flex: 1, minWidth: '200px' }}>
            <Ic name="search" />
            <input placeholder="Find node" />
          </div>
          <Btn text="Fit" kind="ghost" />
          <Btn text="" kind="ghost" extra={<Ic name="zoomIn" cls="ic-sm" />} />
          <Btn text="" kind="ghost" extra={<Ic name="zoomOut" cls="ic-sm" />} />
          <Btn text="Export" kind="secondary" extra={<Ic name="download" cls="ic-sm" />} />
        </div>
      </PanelBlock>

      <PanelBlock label="NETWORK GRAPH">
        <PlaceholderCanvas
          iconName="network"
          label="Network Graph Canvas"
          note="[Case:4471] — ACCUSED_IN — [Raju K] — ASSOCIATE — [Suresh M] — SHARES_PHONE — [Phone:9945]"
          height="420px"
        />
      </PanelBlock>

      <PanelBlock label="LEGEND">
        <div className="filter-bar" style={{ color: 'var(--n-500)', fontSize: '12px' }}>
          ● multiple cases &nbsp;&nbsp; — solid edge = confirmed &nbsp;&nbsp; ┄ dashed edge = inferred
        </div>
      </PanelBlock>
    </>
  );

  const renderNetworkExplorerRight = () => (
    <>
      <PanelBlock label="SELECTED NODE" head="Node Details">
        <Kv rows={[
          ['Name', 'Raju Kumar'],
          ['Type', 'Person'],
          ['Cases', '3'],
          ['Aliases', '3']
        ]} />
      </PanelBlock>
      <PanelBlock label="RELATIONSHIPS" head="Links Summary">
        <div className="list">
          <div className="list-item">ASSOCIATE_OF <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>×2</span></div>
          <div className="list-item">ACCUSED_IN <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>×3</span></div>
        </div>
        <div style={{ marginTop: '12px' }}>
          <Btn text="View Profile &nearr;" kind="secondary" onClick={() => handleScreenChange('entity')} />
        </div>
      </PanelBlock>
    </>
  );

  const renderTimelineView = () => (
    <>
      <PanelBlock label="TIMELINE TOOLBAR">
        <div className="filter-bar">
          <span className="filter-chip">Date Range <Ic name="chevronDown" cls="ic-sm" /></span>
          <Btn text="Zoom In" kind="ghost" extra={<Ic name="zoomIn" cls="ic-sm" />} />
          <Btn text="Zoom Out" kind="ghost" extra={<Ic name="zoomOut" cls="ic-sm" />} />
          <Btn text="Export" kind="secondary" extra={<Ic name="download" cls="ic-sm" />} />
        </div>
      </PanelBlock>

      <PanelBlock label="TIMELINE">
        <PlaceholderCanvas
          iconName="map"
          label="Timeline Axis"
          note="Sep 2024 — 15-Sep Incident reported · 18-Sep Suspect identified · 22-Sep conflicting location evidence · 30-Sep Arrest"
          height="260px"
        />
      </PanelBlock>

      <PanelBlock label="EVENTS" head="Incidents Ledger">
        <div className="list">
          <div className="list-item">
            <span>15-Sep — Incident reported, Koramangala</span>
            <span className="source-chip">FIR</span>
          </div>
          <div className="list-item">
            <span>18-Sep — Suspect Raju K. identified</span>
            <span className="source-chip">Witness Stmt</span>
          </div>
          <div className="list-item">
            <span>
              <span className="conflict-flag" style={{ marginRight: '8px' }}>!</span>22-Sep — Conflicting location evidence
            </span>
            <span className="source-chip">CDR + Witness</span>
          </div>
          <div className="list-item">
            <span>30-Sep — Arrest made</span>
            <span className="source-chip">Case Diary</span>
          </div>
        </div>
      </PanelBlock>
    </>
  );

  const renderTimelineRight = () => (
    <PanelBlock label="EVENT DETAIL" head="Specific Fact Info">
      <Kv rows={[
        ['Date', '22-Sep-2024'],
        ['Source', 'Phone CDR'],
        ['Confidence', 'High'],
        ['Linked Case', 'CR-2024-04471']
      ]} />
    </PanelBlock>
  );

  const renderCrimeMapView = () => (
    <>
      <PanelBlock label="MAP TOOLBAR">
        <div className="filter-bar">
          <span className="filter-chip">Date Range <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">Incident Type <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">District <Ic name="chevronDown" cls="ic-sm" /></span>
          <Btn text="Export" kind="secondary" extra={<Ic name="download" cls="ic-sm" />} />
        </div>
      </PanelBlock>

      <PanelBlock label="CRIME MAP">
        <PlaceholderCanvas
          iconName="map"
          label="Map Canvas"
          note="Incident markers and hotspot heat-zone overlay render here (Leaflet + OpenStreetMap)"
          height="440px"
        />
      </PanelBlock>
    </>
  );

  const renderCrimeMapRight = () => (
    <>
      <PanelBlock label="LAYER TOGGLES" head="Operational Layers">
        <div className="list">
          <div className="list-item">Incidents <span style={{ color: 'var(--n-500)' }}>On</span></div>
          <div className="list-item">Hotspots <span style={{ color: 'var(--n-500)' }}>On</span></div>
          <div className="list-item">Station Boundaries <span style={{ color: 'var(--n-400)' }}>Off</span></div>
        </div>
      </PanelBlock>
      <PanelBlock label="HOTSPOT ALERT">
        <div className="card-head">
          <h4>Whitefield Area</h4>
          <Badge text="HIGH" kind="critical" />
        </div>
        <div style={{ fontSize: '12.5px', color: 'var(--n-600)', marginBottom: '10px' }}>
          +40% incidents this week
        </div>
        <Confidence n={4} labelText="High confidence" />
        <div style={{ marginTop: '12px' }}>
          <Btn text="Investigate &nearr;" kind="secondary" onClick={() => handleScreenChange('workspace')} />
        </div>
      </PanelBlock>
    </>
  );

  const renderReportsView = () => (
    <PanelBlock label="REPORTS">
      <Table
        headers={['Title', 'Case No.', 'Status', 'Created By', 'Date', '']}
        rows={[
          [
            'Cross-case MO summary',
            'CR-2024-04471',
            <Badge text="GENERATED" kind="success" />,
            'S. Ravi Kumar',
            '02-Jul-2026',
            <Btn text="Download" kind="ghost" extra={<Ic name="download" cls="ic-sm" />} />
          ],
          [
            'Network analysis brief',
            'CR-2024-04471',
            <Badge text="DRAFT" kind="neutral" />,
            'S. Ravi Kumar',
            '01-Jul-2026',
            <Btn text="Continue" kind="ghost" />
          ]
        ]}
      />
      <Pagination text="Showing 1–2 of 2 reports" />
    </PanelBlock>
  );

  const renderReportsRight = () => (
    <PanelBlock label="IN PROGRESS" head="Active Generation">
      <div style={{ fontSize: '12.5px', color: 'var(--n-600)', marginBottom: '12px' }}>
        Network analysis brief — compiling sourced findings&hellip;
      </div>
      <div style={{ height: '8px', borderRadius: '4px', background: 'var(--n-200)', overflow: 'hidden' }}>
        <div style={{ width: '62%', height: '100%', background: 'var(--navy-600)' }}></div>
      </div>
    </PanelBlock>
  );

  const renderAlertsView = () => (
    <>
      <PanelBlock label="FILTERS">
        <div className="filter-bar">
          <span className="filter-chip">Severity <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">District <Ic name="chevronDown" cls="ic-sm" /></span>
          <span className="filter-chip">Status <Ic name="chevronDown" cls="ic-sm" /></span>
        </div>
      </PanelBlock>
      <div className="card">
        <div className="card-head">
          <h4>Hotspot threshold crossed — Whitefield</h4>
          <Badge text="HIGH" kind="critical" />
        </div>
        <div style={{ fontSize: '12.5px', color: 'var(--n-600)', marginBottom: '9px' }}>
          +40% incidents vs. 4-week baseline
        </div>
        <Confidence n={4} />
        <div style={{ marginTop: '10px' }}>
          <Btn text="Acknowledge" kind="ghost" />
        </div>
      </div>
      <div className="card">
        <div className="card-head">
          <h4>Pattern spike — cross-case MO match</h4>
          <Badge text="MEDIUM" kind="warning" />
        </div>
        <div style={{ fontSize: '12.5px', color: 'var(--n-600)', marginBottom: '9px' }}>
          3 cases matched in 14 days
        </div>
        <Confidence n={3} />
        <div style={{ marginTop: '10px' }}>
          <Btn text="Acknowledge" kind="ghost" />
        </div>
      </div>
    </>
  );

  const renderAlertsRight = () => (
    <>
      <PanelBlock label="BASIS" head="Detection Parameters">
        <div style={{ fontSize: '12.5px', color: 'var(--n-600)', lineHeight: '1.6' }}>
          Aggregate incident count in a 2km radius exceeded the configured graduated threshold for a sustained 7-day window.
        </div>
      </PanelBlock>
      <PanelBlock label="RELATED CASES" head="Involved Narratives">
        <div className="list">
          <div className="list-item">CR-2024-04471</div>
          <div className="list-item">CR-2024-03107</div>
        </div>
      </PanelBlock>
    </>
  );

  const renderAdminView = () => {
    return renderTabsBlock(
      'admin-tabs',
      ['Users', 'Roles & Access', 'Audit Log'],
      [
        <div key="users">
          <PanelBlock label="USER MANAGEMENT">
            <Table
              headers={['Name', 'Badge No.', 'Role', 'Station', 'Status', '']}
              rows={[
                ['S. Ravi Kumar', 'KSP-44210', <Badge text="SI" kind="neutral" />, 'Koramangala PS', <Badge text="ACTIVE" kind="success" />, <Btn text="Edit" kind="ghost" />],
                ['A. Prakash', 'KSP-33019', <Badge text="INSPECTOR" kind="neutral" />, 'Whitefield PS', <Badge text="ACTIVE" kind="success" />, <Btn text="Edit" kind="ghost" />],
                ['M. Lakshmi', 'KSP-51002', <Badge text="ANALYST" kind="neutral" />, 'SCRB', <Badge text="ACTIVE" kind="success" />, <Btn text="Edit" kind="ghost" />]
              ]}
            />
          </PanelBlock>
          <div style={{ marginTop: '14px' }}>
            <Btn text="Add User" kind="primary" extra={<Ic name="plus" cls="ic-sm" />} />
          </div>
        </div>,
        <PanelBlock label="ROLE DEFINITIONS" key="roles">
          <div className="list">
            <div className="list-item">SI <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>Case-level access</span></div>
            <div className="list-item">Inspector <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>Station-level access</span></div>
            <div className="list-item">Analyst <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>Cross-case access</span></div>
            <div className="list-item">Auditor <span style={{ color: 'var(--n-500)', fontSize: '11.5px' }}>Log access only</span></div>
          </div>
        </PanelBlock>,
        <PanelBlock label="AUDIT LOG" key="logs">
          <Table
            headers={['Timestamp', 'User', 'Event', 'Detail']}
            rows={[
              ['02-Jul-2026 14:02', 'S. Ravi Kumar', 'QUERY', 'Cross-case MO similarity check'],
              ['02-Jul-2026 14:02', 'System', 'RESPONSE', <Badge text="LOGGED" kind="success" />],
              ['01-Jul-2026 09:41', 'M. Lakshmi', 'LOGIN', '—']
            ]}
          />
        </PanelBlock>
      ]
    );
  };

  const renderAdminRight = () => (
    <PanelBlock label="QUICK REFERENCE" head="Role Summary">
      <div className="list">
        <div className="list-item">4 roles configured</div>
        <div className="list-item">12 active users</div>
      </div>
    </PanelBlock>
  );

  const renderSettingsView = () => (
    <>
      <PanelBlock label="LANGUAGE PREFERENCE">
        <div className="field">
          <label>Default Language</label>
          <select className="input">
            <option>English</option>
            <option>ಕನ್ನಡ (Kannada)</option>
          </select>
        </div>
      </PanelBlock>
      <PanelBlock label="DISPLAY DENSITY">
        <div className="field">
          <label>Table &amp; List Density</label>
          <select className="input">
            <option>Comfortable</option>
            <option>Compact</option>
          </select>
        </div>
      </PanelBlock>
      <PanelBlock label="NOTIFICATION PREFERENCES">
        <div className="list">
          <div className="list-item">Hotspot alerts <span style={{ color: 'var(--n-500)' }}>On</span></div>
          <div className="list-item">New cross-case matches <span style={{ color: 'var(--n-500)' }}>On</span></div>
          <div className="list-item">Weekly summary email <span style={{ color: 'var(--n-400)' }}>Off</span></div>
        </div>
      </PanelBlock>
      <Btn text="Save Changes" kind="primary" />
    </>
  );

  // Selector for current view
  const renderScreenContent = () => {
    switch (currentScreen) {
      case 'legend':
        return renderLegendView();
      case 'login':
        return renderLoginView();
      case 'workspace':
        return renderWorkspaceView();
      case 'search':
        return renderSearchView();
      case 'case':
        return renderCaseProfileView();
      case 'entity':
        return renderEntityProfileView();
      case 'network':
        return renderNetworkExplorerView();
      case 'timeline':
        return renderTimelineView();
      case 'map':
        return renderCrimeMapView();
      case 'reports':
        return renderReportsView();
      case 'alerts':
        return renderAlertsView();
      case 'admin':
        return renderAdminView();
      case 'settings':
        return renderSettingsView();
      default:
        return renderLegendView();
    }
  };

  // Selector for current view's right panel
  const renderScreenRightPanel = () => {
    switch (currentScreen) {
      case 'workspace':
        return renderWorkspaceRight();
      case 'case':
        return renderCaseProfileRight();
      case 'entity':
        return renderEntityProfileRight();
      case 'network':
        return renderNetworkExplorerRight();
      case 'timeline':
        return renderTimelineRight();
      case 'map':
        return renderCrimeMapRight();
      case 'reports':
        return renderReportsRight();
      case 'alerts':
        return renderAlertsRight();
      case 'admin':
        return renderAdminRight();
      default:
        return null;
    }
  };

  const getScreenConfig = (): ScreenConfig => {
    return SCREENS.find(s => s.key === currentScreen) || SCREENS[0];
  };

  const activeConf = getScreenConfig();
  const hasRightPanel = !!renderScreenRightPanel();

  /* ============================================================
     LAYOUT BUILDERS
     ============================================================ */
  const renderHeader = (caseLabel: string | null | undefined) => {
    return (
      <header className="app-header">
        <div className="hamburger" onClick={() => setNavOpen(!navOpen)}>
          <Ic name="menu" />
        </div>
        <div className="brand" onClick={() => handleScreenChange('legend')} style={{ cursor: 'pointer' }}>
          <img className="crest" src={CREST_SRC} alt="Karnataka State Police crest" />
          <div className="brand-text">
            <span className="brand-name">KSP Crime Intelligence Platform</span>
            <span className="brand-sub">Karnataka State Police &middot; SCRB</span>
          </div>
        </div>
        <div className="header-divider"></div>
        <div className="case-selector" onClick={() => handleScreenChange('search')}>
          <Ic name="search" cls="ic-sm" />
          <span className="case-text">{caseLabel || 'No case selected'}</span>
          <Ic name="chevronDown" cls="ic-sm" />
        </div>
        <div className="header-spacer"></div>
        <div className="header-right">
          <div className="lang-select">
            <Ic name="globe" cls="ic-sm" />
            <span className="lang-text">EN&nbsp;/&nbsp;<span className="kn">ಕನ</span></span>
            <Ic name="chevronDown" cls="ic-sm" />
          </div>
          {hasRightPanel && (
            <div className="icon-btn panel-toggle-header" style={{ display: 'none' }} onClick={() => setPanelOpen(!panelOpen)}>
              <Ic name="panel" />
            </div>
          )}
          <div className="icon-btn" onClick={() => handleScreenChange('alerts')}>
            <Ic name="bell" />
            <span className="badge-dot">3</span>
          </div>
          <div className="profile-menu" onClick={() => handleScreenChange('settings')}>
            <span className="avatar">SR</span>
            <span className="who">
              S. Ravi Kumar<b>Sub-Inspector</b>
            </span>
            <Ic name="chevronDown" cls="ic-sm" />
          </div>
        </div>
      </header>
    );
  };

  const renderNav = (activeNav: string | undefined) => {
    return (
      <nav className={`app-nav ${navOpen ? 'open' : ''}`}>
        {NAV_ITEMS.map((n, idx) => (
          <div
            key={idx}
            className={`nav-item ${n.id === activeNav ? 'active' : ''}`}
            title={n.label}
            onClick={() => handleScreenChange(n.id)}
          >
            <span className="icon-slot"><Ic name={n.icon} /></span>
            <span>{n.label}</span>
          </div>
        ))}
      </nav>
    );
  };

  const breadcrumbHtml = activeConf.breadcrumb ? (
    <div className="breadcrumb">
      {activeConf.breadcrumb.map((b, idx, arr) => (
        <span key={idx}>
          {idx === arr.length - 1 ? <b>{b}</b> : <>{b}<span className="sep"><Ic name="chevronRight" cls="ic-sm" /></span></>}
        </span>
      ))}
    </div>
  ) : null;

  return (
    <div>
      {/* Meta Navigator */}
      <nav id="meta">
        <span className="meta-title">Hi-Fi Reference</span>
        {SCREENS.map((scr, idx) => (
          <button
            key={idx}
            className={`scr-btn ${currentScreen === scr.key ? 'on' : ''}`}
            onClick={() => handleScreenChange(scr.key)}
          >
            {scr.navLabel}
          </button>
        ))}
        <div className="meta-spacer"></div>
        <button
          id="annot-toggle"
          className={showAnnotations ? 'on' : ''}
          onClick={() => setShowAnnotations(!showAnnotations)}
        >
          Annotations: {showAnnotations ? 'On' : 'Off'}
        </button>
      </nav>

      {/* Main App Container */}
      <div id="root">
        {activeConf.shell ? (
          <div className="app-shell">
            {renderHeader(activeConf.caseLabel)}
            <div className="app-body">
              <div className={`scrim ${navOpen || panelOpen ? 'show' : ''}`} onClick={closeOverlays}></div>
              {renderNav(activeConf.activeNav)}
              <main className="app-main">
                {!activeConf.hideHead && (
                  <div className="page-head">
                    <div>
                      {breadcrumbHtml}
                      <h1>{activeConf.title}</h1>
                      {activeConf.subtitle && <p>{activeConf.subtitle}</p>}
                    </div>
                    {activeConf.actions && (
                      <div className="actions">
                        {activeConf.actions.map((a, i) => (
                          <Btn key={i} text={a.text} kind={a.kind} />
                        ))}
                      </div>
                    )}
                  </div>
                )}
                {renderScreenContent()}
              </main>
              {hasRightPanel && (
                <aside className={`app-panel ${panelOpen ? 'open' : ''}`}>
                  <div className="panel-title">
                    <h3>{currentScreen === 'workspace' ? 'Case Context Panel' : currentScreen === 'case' ? 'Case Stats' : currentScreen === 'entity' ? 'Related Entities' : currentScreen === 'network' ? 'Node Detail' : currentScreen === 'timeline' ? 'Selected Event' : currentScreen === 'map' ? 'Map Layers' : currentScreen === 'reports' ? 'Generation Status' : currentScreen === 'alerts' ? 'Alert Detail' : currentScreen === 'admin' ? 'Role Legend' : 'Panel'}</h3>
                    <span className="panel-close" onClick={() => setPanelOpen(false)}>
                      <Ic name="x" cls="ic-sm" />
                    </span>
                  </div>
                  {renderScreenRightPanel()}
                </aside>
              )}
            </div>
          </div>
        ) : (
          renderScreenContent()
        )}
      </div>
    </div>
  );
}

export default App;
