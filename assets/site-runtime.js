(function () {
  const config = window.ATLASFLOW_CONFIG || {};
  const canonicalOrigin = (config.canonicalOrigin || "").replace(/\/$/, "");
  const analyticsState = {
    measurementId: "",
    gtagConfigured: false,
    eventsSent: 0,
    lastEvent: "none",
    lastBeacon: "none",
    panel: null,
  };

  function ensureCanonical() {
    if (!canonicalOrigin) return;
    const path = window.location.pathname.endsWith("index.html")
      ? window.location.pathname.replace(/index\.html$/, "")
      : window.location.pathname;
    const canonicalHref = path === "/" ? `${canonicalOrigin}/` : `${canonicalOrigin}${path}`;

    let link = document.querySelector('link[rel="canonical"]');
    if (!link) {
      link = document.createElement("link");
      link.setAttribute("rel", "canonical");
      document.head.appendChild(link);
    }
    link.setAttribute("href", canonicalHref);

    if (config.redirectToCanonical === true) {
      const target = new URL(canonicalHref + window.location.search + window.location.hash);
      if (window.location.origin !== target.origin) {
        window.location.replace(target.toString());
      }
    }
  }

  function shouldShowGaPanel() {
    const analytics = config.analytics || {};
    const search = new URLSearchParams(window.location.search);
    return analytics.debugPanel === true || search.get("ga_debug") === "1";
  }

  function updateGaPanel() {
    if (!analyticsState.panel) return;
    const content = analyticsState.panel.querySelector("[data-ga-panel-content]");
    if (!content) return;
    const status = analyticsState.gtagConfigured ? "ready" : "not-ready";
    content.textContent =
      `GA status: ${status} | ID: ${analyticsState.measurementId || "unset"} | events: ${analyticsState.eventsSent} | last: ${analyticsState.lastEvent} | beacon: ${analyticsState.lastBeacon}`;
  }

  function getOrCreateClientId() {
    const key = "atlasflow_ga_cid";
    try {
      const existing = window.localStorage.getItem(key);
      if (existing) return existing;
      const created = `${Date.now()}.${Math.floor(Math.random() * 1e9)}`;
      window.localStorage.setItem(key, created);
      return created;
    } catch (error) {
      return `${Date.now()}.${Math.floor(Math.random() * 1e9)}`;
    }
  }

  function sendDebugCollectBeacon(eventName) {
    if (!analyticsState.measurementId) {
      analyticsState.lastBeacon = "no_measurement_id";
      updateGaPanel();
      return false;
    }
    const params = new URLSearchParams({
      v: "2",
      tid: analyticsState.measurementId,
      cid: getOrCreateClientId(),
      en: eventName,
      dl: window.location.href,
      dt: document.title,
      ul: navigator.language || "en-us",
      "ep.debug_mode": "1",
      "ep.page_path": window.location.pathname,
    });
    const url = `https://www.google-analytics.com/g/collect?${params.toString()}`;
    let sent = false;
    try {
      if (typeof navigator.sendBeacon === "function") {
        sent = navigator.sendBeacon(url);
      } else {
        fetch(url, { method: "GET", mode: "no-cors", keepalive: true });
        sent = true;
      }
      analyticsState.lastBeacon = sent ? "sent" : "blocked";
    } catch (error) {
      analyticsState.lastBeacon = "error";
      sent = false;
    }
    updateGaPanel();
    return sent;
  }

  function ensureGaPanel() {
    if (!shouldShowGaPanel() || analyticsState.panel) return;
    const panel = document.createElement("aside");
    panel.style.position = "fixed";
    panel.style.bottom = "12px";
    panel.style.right = "12px";
    panel.style.zIndex = "99999";
    panel.style.maxWidth = "420px";
    panel.style.background = "#102431";
    panel.style.color = "#f2f7fa";
    panel.style.padding = "12px";
    panel.style.border = "1px solid #255972";
    panel.style.borderRadius = "10px";
    panel.style.fontFamily = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    panel.style.fontSize = "12px";
    panel.innerHTML = `
      <strong style="display:block; margin-bottom:6px;">AtlasFlow GA Debug</strong>
      <div data-ga-panel-content style="line-height:1.45; margin-bottom:8px;">Initializing...</div>
      <button type="button" data-ga-panel-ping style="padding:6px 10px; border:0; border-radius:6px; background:#2f8bb8; color:#fff; cursor:pointer;">
        Send test event
      </button>
    `;
    document.body.appendChild(panel);
    const ping = panel.querySelector("[data-ga-panel-ping]");
    if (ping) {
      ping.addEventListener("click", function () {
        track("cw_debug_ping", { source: "ga_debug_panel", page_path: window.location.pathname });
        sendDebugCollectBeacon("cw_debug_ping_beacon");
      });
    }
    analyticsState.panel = panel;
    updateGaPanel();
  }

  function setupAnalytics() {
    const analytics = config.analytics || {};
    const measurementId = analytics.gaMeasurementId || "";
    const debugMode = analytics.debug === true;
    analyticsState.measurementId = measurementId;
    if (!measurementId) {
      updateGaPanel();
      return;
    }

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () {
      window.dataLayer.push(arguments);
    };

    const src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
    if (!document.querySelector(`script[src="${src}"]`)) {
      const tag = document.createElement("script");
      tag.async = true;
      tag.src = src;
      document.head.appendChild(tag);
    }

    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      anonymize_ip: true,
      debug_mode: debugMode,
    });
    analyticsState.gtagConfigured = true;
    updateGaPanel();
  }

  function track(eventName, params) {
    const analytics = config.analytics || {};
    const payload = { ...(params || {}) };
    if (analytics.debug === true) {
      payload.debug_mode = true;
    }
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, payload);
    }
    analyticsState.eventsSent += 1;
    analyticsState.lastEvent = eventName;
    updateGaPanel();
    if (analytics.debug) {
      console.log("[atlasflow-track]", eventName, payload);
    }
  }

  function exposeDebugApi() {
    window.ATLASFLOW_DEBUG = {
      track: function (eventName, params) {
        track(eventName, params || {});
      },
      analyticsStatus: function () {
        return {
          measurementId: analyticsState.measurementId,
          gtagConfigured: analyticsState.gtagConfigured,
          eventsSent: analyticsState.eventsSent,
          lastEvent: analyticsState.lastEvent,
          lastBeacon: analyticsState.lastBeacon,
        };
      },
      beaconPing: function () {
        return sendDebugCollectBeacon("cw_debug_ping_beacon_console");
      },
    };
  }

  function showFormStatus(form, kind, message) {
    let el = form.querySelector('[data-form-status]');
    if (!el) {
      el = document.createElement("p");
      el.setAttribute("data-form-status", "true");
      el.style.marginTop = "0.7rem";
      el.style.fontWeight = "700";
      form.appendChild(el);
    }
    el.style.color = kind === "error" ? "#9a1d1d" : "#1d6a42";
    el.textContent = message;
  }

  function formTypeToEndpoint(type) {
    const forms = config.forms || {};
    if (type === "contact") return forms.contactEndpoint || "";
    if (type === "newsletter") return forms.newsletterEndpoint || "";
    if (type === "strategy_call") return forms.strategyCallEndpoint || "";
    return "";
  }

  function buildProviderPayload(formType, fields) {
    const forms = config.forms || {};
    const subjectMap = forms.subjectByType || {};
    const subject = subjectMap[formType] || `AtlasFlow ${formType} submission`;
    const merged = {
      ...fields,
      form_type: formType,
      page_path: window.location.pathname,
      submitted_at: new Date().toISOString(),
      _subject: subject,
      _captcha: "false",
      _template: "table",
    };
    return merged;
  }

  async function readJsonSafe(response) {
    try {
      return await response.json();
    } catch (error) {
      return null;
    }
  }

  function normalizeProviderSuccess(json) {
    if (!json || typeof json !== "object" || !('success' in json)) {
      return null;
    }
    const value = json.success;
    if (typeof value === "boolean") return value;
    if (typeof value === "string") return value.trim().toLowerCase() === "true";
    if (typeof value === "number") return value > 0;
    return null;
  }

  function extractProviderMessage(json) {
    if (!json || typeof json !== "object") return "";
    if (typeof json.message === "string") return json.message.trim();
    if (typeof json.error === "string") return json.error.trim();
    return "";
  }

  function buildMailtoHref(formType, payload) {
    const fallbackEmail = config.fallbackEmail || "";
    const subject = payload._subject || `AtlasFlow ${formType} inquiry`;
    const lines = Object.entries(payload)
      .filter(([key]) => !key.startsWith("_"))
      .map(([key, value]) => `${key}: ${value}`);
    const body = lines.join("\n");
    return `mailto:${encodeURIComponent(fallbackEmail)}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formType = form.getAttribute("data-form-type") || "unknown";

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const data = new FormData(form);
    const fields = Object.fromEntries(data.entries());
    const payload = buildProviderPayload(formType, fields);
    const endpoint = formTypeToEndpoint(formType);
    const formsConfig = config.forms || {};

    track("form_submit_attempt", { form_type: formType, page_path: window.location.pathname });

    if (formsConfig.mode === "email_fallback") {
      showFormStatus(
        form,
        "error",
        `Live form backend is temporarily offline. Opening your email client instead. If nothing opens, email ${(config.fallbackEmail || "the support address")} directly.`
      );
      track("form_submit_blocked", { form_type: formType, reason: "email_fallback" });
      window.location.href = buildMailtoHref(formType, payload);
      return;
    }

    if (!endpoint) {
      showFormStatus(
        form,
        "error",
        `Submission endpoint not configured yet. Use fallback: ${(config.fallbackEmail || "set fallbackEmail in assets/site-config.js")}.`
      );
      track("form_submit_blocked", { form_type: formType, reason: "no_endpoint" });
      return;
    }

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(payload),
      });
      const providerJson = await readJsonSafe(response);
      if (!response.ok) {
        const providerMessage = extractProviderMessage(providerJson);
        throw new Error(providerMessage || `HTTP ${response.status}`);
      }
      const providerSuccess = normalizeProviderSuccess(providerJson);
      const providerMessage = extractProviderMessage(providerJson);
      if (providerSuccess === false) {
        throw new Error(providerMessage || "Provider rejected the submission.");
      }
      form.reset();
      showFormStatus(form, "ok", "Thanks. Your submission has been received.");
      track("form_submit_success", { form_type: formType, page_path: window.location.pathname });
    } catch (error) {
      const reason = error instanceof Error && error.message ? error.message : "unknown_error";
      showFormStatus(
        form,
        "error",
        `Could not submit right now. Please email ${(config.fallbackEmail || "the support address")}.`
      );
      track("form_submit_error", { form_type: formType, page_path: window.location.pathname, reason });
    }
  }

  function setupForms() {
    const forms = document.querySelectorAll("form[data-form-type]");
    forms.forEach((form) => {
      form.setAttribute("novalidate", "novalidate");
      form.addEventListener("submit", handleFormSubmit);
    });
  }

  function setupCtaTracking() {
    const clickable = document.querySelectorAll("a.btn, button.btn");
    clickable.forEach((el) => {
      el.addEventListener("click", () => {
        const label = (el.textContent || "").trim().slice(0, 80);
        const href = el.tagName.toLowerCase() === "a" ? (el.getAttribute("href") || "") : "";
        track("cta_click", { label, href, page_path: window.location.pathname });
      });
    });
  }

  exposeDebugApi();
  ensureGaPanel();
  setupAnalytics();
  ensureCanonical();
  setupForms();
  setupCtaTracking();
  track("page_view", { page_path: window.location.pathname, page_title: document.title });
})();
