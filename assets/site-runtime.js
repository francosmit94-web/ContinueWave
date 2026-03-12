(function () {
  const config = window.ATLASFLOW_CONFIG || {};
  const canonicalOrigin = (config.canonicalOrigin || "").replace(/\/$/, "");

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

  function setupAnalytics() {
    const analytics = config.analytics || {};
    const measurementId = analytics.gaMeasurementId || "";
    if (!measurementId) return;

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
    window.gtag("config", measurementId, { anonymize_ip: true });
  }

  function track(eventName, params) {
    const payload = params || {};
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, payload);
    }
    if ((config.analytics || {}).debug) {
      console.log("[atlasflow-track]", eventName, payload);
    }
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

  async function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formType = form.getAttribute("data-form-type") || "unknown";

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const endpoint = formTypeToEndpoint(formType);
    const data = new FormData(form);
    const payload = {
      formType,
      page: window.location.pathname,
      submittedAt: new Date().toISOString(),
      fields: Object.fromEntries(data.entries()),
    };

    track("form_submit_attempt", { form_type: formType, page_path: window.location.pathname });

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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      form.reset();
      showFormStatus(form, "ok", "Thanks. Your submission has been received.");
      track("form_submit_success", { form_type: formType, page_path: window.location.pathname });
    } catch (error) {
      showFormStatus(
        form,
        "error",
        `Could not submit right now. Please email ${(config.fallbackEmail || "the support address")}.`
      );
      track("form_submit_error", { form_type: formType, page_path: window.location.pathname });
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

  setupAnalytics();
  ensureCanonical();
  setupForms();
  setupCtaTracking();
  track("page_view", { page_path: window.location.pathname, page_title: document.title });
})();
