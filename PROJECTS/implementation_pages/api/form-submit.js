export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  const siteOrigin = "https://implementationpages.vercel.app";

  if (req.method !== "POST") {
    res.status(405).json({ success: false, error: "Method not allowed." });
    return;
  }

  const body = typeof req.body === "string" ? safeJsonParse(req.body) : (req.body || {});
  const formType = String(body.form_type || "").trim().toLowerCase();
  const allowed = new Set(["contact", "newsletter", "strategy_call"]);

  if (!allowed.has(formType)) {
    res.status(400).json({ success: false, error: "Unsupported form type." });
    return;
  }

  try {
    const refererPath = typeof body.page_path === "string" && body.page_path.trim()
      ? body.page_path.trim()
      : "/contact.html";
    const providerResponse = await fetch("https://formsubmit.co/ajax/growth@atlasflow.co.za", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Origin: siteOrigin,
        Referer: `${siteOrigin}${refererPath}`,
      },
      body: JSON.stringify(body),
    });

    const text = await providerResponse.text();
    const data = safeJsonParse(text);

    if (!providerResponse.ok) {
      res.status(providerResponse.status).json({
        success: false,
        error: extractErrorMessage(data) || `Provider HTTP ${providerResponse.status}`,
        provider_status: providerResponse.status,
      });
      return;
    }

    if (data && typeof data === "object" && "success" in data) {
      res.status(200).json(data);
      return;
    }

    res.status(200).json({ success: true, provider_raw: text });
  } catch (error) {
    res.status(502).json({
      success: false,
      error: error instanceof Error ? error.message : "Upstream submission failed.",
    });
  }
}

function safeJsonParse(value) {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function extractErrorMessage(data) {
  if (!data || typeof data !== "object") return "";
  if (typeof data.message === "string") return data.message.trim();
  if (typeof data.error === "string") return data.error.trim();
  return "";
}
