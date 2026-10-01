/* HaqSetu prototype UI. Vanilla JS only: the API remains the source of truth. */
(function () {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const knownStatuses = new Set([
    "promising_signal_verify_officially",
    "needs_information",
    "not_matched_on_screening",
    "verify_official_criteria",
  ]);

  const text = {
    en: {
      lowBandwidth: "Low data",
      eyebrow: "Evidence-first benefits navigation",
      heroTitle: "Find the support you may be missing.",
      heroLead: "Describe your situation once. HaqSetu screens government schemes, shows the evidence behind every signal, and gives you a clear next step.",
      officialSources: "Official sources",
      privacyFirst: "Privacy-first",
      bilingual: "English + हिंदी",
      stepOne: "Step 1 · Tell us about yourself",
      profileHeading: "Build your screening profile",
      profileSubhead: "Only share broad facts needed to compare scheme criteria.",
      required: "Required",
      tryScenario: "Try a sample profile",
      farmerScenario: "Small farmer",
      vendorScenario: "Street vendor",
      seniorScenario: "Senior citizen",
      studentScenario: "Student",
      nameLabel: "Name",
      optional: "Optional",
      namePlaceholder: "How should we address you?",
      nameHint: "Not used for matching and never included in logs.",
      stateLabel: "State / UT",
      selectState: "Select your state",
      ageLabel: "Age",
      years: "years",
      occupationLabel: "Occupation",
      occupationPlaceholder: "e.g. small farmer",
      incomeLabel: "Monthly household income",
      categoryLabel: "Social category",
      selectCategory: "Select category",
      landLabel: "Landholding",
      hectares: "hectares",
      disabilityLabel: "Person with disability",
      disabilityHint: "Include this only if relevant to the person seeking support.",
      needsLabel: "What support are you looking for?",
      needsPlaceholder: "Tell us in your own words — for example: I need help with crop insurance and healthcare for my family.",
      needsHint: "Write naturally in English or Hindi. Separate multiple needs with commas.",
      privacyTitle: "Your privacy is part of the design",
      privacyBody: "Do not enter Aadhaar, bank details, OTPs, passwords, or document numbers. Broad profile facts are enough for this preliminary screening.",
      noSubmission: "Screening only. Nothing is submitted to any department.",
      analyze: "Analyze my options",
      agentTrace: "Agent trace",
      traceHeading: "How HaqSetu reasons",
      traceIntro: "A transparent, step-by-step screening — not a black-box decision.",
      intakeAgent: "Intake agent",
      intakeDesc: "Structures only the profile facts needed for screening.",
      discoveryAgent: "Scheme discovery",
      discoveryDesc: "Ranks relevant programmes from the seeded catalogue.",
      evidenceAgent: "Evidence checker",
      evidenceDesc: "Tests each rule and keeps unmatched evidence visible.",
      planAgent: "Action planner",
      planDesc: "Builds a cautious next-step plan with official sources.",
      waiting: "Waiting",
      working: "Working",
      complete: "Complete",
      traceError: "Needs attention",
      ready: "Ready",
      deterministic: "Deterministic by design",
      deterministicBody: "The same profile produces the same explainable result.",
      stepTwo: "Step 2 · Your screening report",
      resultsHeading: "A clearer path to your benefits",
      readiness: "Profile readiness",
      readinessTitle: "Your profile is ready for screening",
      readinessIncomplete: "A few facts still need verification",
      readinessNote: "This measures screening completeness, not the probability of official approval.",
      schemesReviewed: "schemes reviewed",
      sourcesAttached: "official sources",
      timeSaved: "estimated saved",
      rankedMatches: "Ranked matches",
      matchesHeading: "Schemes worth checking",
      screeningOnly: "Screening only",
      recommended: "Recommended",
      actionHeading: "Your action plan",
      counterfactual: "Counterfactual check",
      missingHeading: "What could change the result?",
      missingIntro: "These details need official verification and may change a scheme's status.",
      allFacts: "No additional profile facts were flagged. Confirm current documents and deadlines on the official source.",
      consentLabel: "You stay in control",
      consentHeading: "Review before taking action",
      consentBody: "HaqSetu never submits an application. You can prepare a draft checklist only after confirming your consent.",
      consentCheckbox: "I understand this is guidance, and I consent to preparing a local draft.",
      prepareDraft: "Prepare draft checklist",
      neverSubmit: "No automatic submission · No credentials requested",
      draftTitle: "Your local draft checklist",
      draftBody: "Use this as a conversation aid. Open each official source and confirm the current process before sharing anything.",
      draftNext: "Next steps",
      feedbackHeading: "Was this screening useful?",
      feedbackSubhead: "Your anonymous feedback helps improve the prototype.",
      yesHelpful: "Yes, helpful",
      notYet: "Not yet",
      feedbackPlaceholder: "Tell us what would make this better (optional)",
      sendFeedback: "Send feedback",
      feedbackThanks: "Thank you — anonymous feedback received for the demo.",
      footerTagline: "A bridge from questions to verified next steps.",
      footerDisclaimer: "Prototype for preliminary screening. Government portals and departments remain authoritative.",
      statusPromising: "Promising signal · Verify",
      statusNeeds: "Needs information",
      statusNoMatch: "Not matched on screen",
      statusVerify: "Check official criteria",
      evidence: "View rule evidence",
      hideEvidence: "Hide rule evidence",
      source: "Official source",
      verified: "Last verified",
      documents: "Documents to confirm",
      matched: "matched",
      notMatched: "not matched",
      missing: "missing",
      signalToVerify: "Signal to verify",
      whyItMatters: "Why it matters",
      errorGeneric: "We could not complete the screening. Check that the HaqSetu API is running and try again.",
      errorValidation: "Please complete the required fields before analyzing.",
      noFeedback: "Choose whether this was helpful first.",
    },
    hi: {
      lowBandwidth: "कम डेटा",
      eyebrow: "साक्ष्य-आधारित लाभ नेविगेशन",
      heroTitle: "जिस सहायता से आप वंचित हो सकते हैं, उसे खोजें।",
      heroLead: "अपनी स्थिति एक बार बताएं। HaqSetu सरकारी योजनाओं की प्रारम्भिक स्क्रीनिंग करता है, हर संकेत के पीछे साक्ष्य दिखाता है और अगला कदम बताता है।",
      officialSources: "आधिकारिक स्रोत",
      privacyFirst: "गोपनीयता पहले",
      bilingual: "English + हिंदी",
      stepOne: "चरण 1 · अपने बारे में बताएं",
      profileHeading: "स्क्रीनिंग प्रोफ़ाइल बनाएं",
      profileSubhead: "योजना की शर्तों की तुलना के लिए केवल सामान्य जानकारी साझा करें।",
      required: "ज़रूरी",
      tryScenario: "एक नमूना प्रोफ़ाइल आज़माएं",
      farmerScenario: "छोटे किसान",
      vendorScenario: "स्ट्रीट वेंडर",
      seniorScenario: "वरिष्ठ नागरिक",
      studentScenario: "छात्र",
      nameLabel: "नाम",
      optional: "वैकल्पिक",
      namePlaceholder: "हम आपको किस नाम से बुलाएं?",
      nameHint: "मिलान के लिए उपयोग नहीं होता और लॉग में शामिल नहीं किया जाता।",
      stateLabel: "राज्य / केंद्र शासित प्रदेश",
      selectState: "राज्य चुनें",
      ageLabel: "उम्र",
      years: "वर्ष",
      occupationLabel: "व्यवसाय",
      occupationPlaceholder: "जैसे छोटा किसान",
      incomeLabel: "मासिक पारिवारिक आय",
      categoryLabel: "सामाजिक श्रेणी",
      selectCategory: "श्रेणी चुनें",
      landLabel: "भूमि",
      hectares: "हेक्टेयर",
      disabilityLabel: "दिव्यांग व्यक्ति",
      disabilityHint: "इसे तभी चुनें जब सहायता चाहने वाले व्यक्ति के लिए प्रासंगिक हो।",
      needsLabel: "आपको किस सहायता की तलाश है?",
      needsPlaceholder: "अपने शब्दों में बताएं — जैसे: मुझे फसल बीमा और परिवार के लिए स्वास्थ्य सहायता चाहिए।",
      needsHint: "अंग्रेज़ी या हिंदी में सामान्य रूप से लिखें। कई ज़रूरतों को अल्पविराम से अलग करें।",
      privacyTitle: "आपकी गोपनीयता हमारे डिज़ाइन का हिस्सा है",
      privacyBody: "आधार, बैंक विवरण, OTP, पासवर्ड या दस्तावेज़ संख्या न लिखें। इस प्रारम्भिक स्क्रीनिंग के लिए सामान्य प्रोफ़ाइल जानकारी पर्याप्त है।",
      noSubmission: "केवल स्क्रीनिंग। किसी विभाग को कुछ जमा नहीं किया जाता।",
      analyze: "मेरे विकल्पों का विश्लेषण करें",
      agentTrace: "एजेंट ट्रेस",
      traceHeading: "HaqSetu कैसे सोचता है",
      traceIntro: "पारदर्शी, चरण-दर-चरण स्क्रीनिंग — ब्लैक-बॉक्स निर्णय नहीं।",
      intakeAgent: "इंटेक एजेंट",
      intakeDesc: "स्क्रीनिंग के लिए केवल ज़रूरी प्रोफ़ाइल तथ्य व्यवस्थित करता है।",
      discoveryAgent: "योजना खोज",
      discoveryDesc: "कैटलॉग से प्रासंगिक कार्यक्रमों को रैंक करता है।",
      evidenceAgent: "साक्ष्य जाँचकर्ता",
      evidenceDesc: "हर नियम जाँचता है और न मिले साक्ष्य को भी दिखाता है।",
      planAgent: "कार्य योजनाकार",
      planDesc: "आधिकारिक स्रोतों के साथ सावधान अगला कदम बनाता है।",
      waiting: "प्रतीक्षा",
      working: "काम जारी",
      complete: "पूरा",
      traceError: "ध्यान दें",
      ready: "तैयार",
      deterministic: "जानबूझकर नियतात्मक",
      deterministicBody: "एक ही प्रोफ़ाइल से वही समझने योग्य परिणाम मिलता है।",
      stepTwo: "चरण 2 · आपकी स्क्रीनिंग रिपोर्ट",
      resultsHeading: "लाभों तक पहुंचने का स्पष्ट रास्ता",
      readiness: "प्रोफ़ाइल तैयारी",
      readinessTitle: "आपकी प्रोफ़ाइल स्क्रीनिंग के लिए तैयार है",
      readinessIncomplete: "कुछ तथ्यों का सत्यापन अभी बाकी है",
      readinessNote: "यह स्क्रीनिंग की पूर्णता बताता है, आधिकारिक स्वीकृति की संभावना नहीं।",
      schemesReviewed: "योजनाएं देखीं",
      sourcesAttached: "आधिकारिक स्रोत",
      timeSaved: "अनुमानित बचत",
      rankedMatches: "रैंक किए गए मिलान",
      matchesHeading: "जिन योजनाओं को जांचना चाहिए",
      screeningOnly: "केवल स्क्रीनिंग",
      recommended: "सुझाव",
      actionHeading: "आपकी कार्य योजना",
      counterfactual: "काउंटरफैक्चुअल जाँच",
      missingHeading: "परिणाम क्या बदल सकता है?",
      missingIntro: "इन विवरणों का आधिकारिक सत्यापन ज़रूरी है और इनसे योजना की स्थिति बदल सकती है।",
      allFacts: "प्रोफ़ाइल में कोई अतिरिक्त तथ्य चिन्हित नहीं हुआ। आधिकारिक स्रोत पर वर्तमान दस्तावेज़ और समय-सीमा की पुष्टि करें।",
      consentLabel: "नियंत्रण आपके हाथ में",
      consentHeading: "कार्रवाई से पहले समीक्षा करें",
      consentBody: "HaqSetu कभी आवेदन जमा नहीं करता। सहमति देने के बाद ही स्थानीय ड्राफ्ट चेकलिस्ट तैयार की जा सकती है।",
      consentCheckbox: "मैं समझता/समझती हूं कि यह मार्गदर्शन है और स्थानीय ड्राफ्ट तैयार करने की सहमति देता/देती हूं।",
      prepareDraft: "ड्राफ्ट चेकलिस्ट बनाएं",
      neverSubmit: "स्वचालित जमा नहीं · क्रेडेंशियल नहीं मांगे जाते",
      draftTitle: "आपकी स्थानीय ड्राफ्ट चेकलिस्ट",
      draftBody: "इसे बातचीत के सहायक के रूप में उपयोग करें। कुछ भी साझा करने से पहले हर आधिकारिक स्रोत खोलकर वर्तमान प्रक्रिया की पुष्टि करें।",
      draftNext: "अगले कदम",
      feedbackHeading: "क्या यह स्क्रीनिंग उपयोगी थी?",
      feedbackSubhead: "आपकी गुमनाम प्रतिक्रिया प्रोटोटाइप को बेहतर बनाने में मदद करती है।",
      yesHelpful: "हां, उपयोगी",
      notYet: "अभी नहीं",
      feedbackPlaceholder: "इसे बेहतर बनाने के लिए क्या बदलें? (वैकल्पिक)",
      sendFeedback: "प्रतिक्रिया भेजें",
      feedbackThanks: "धन्यवाद — डेमो के लिए गुमनाम प्रतिक्रिया मिल गई।",
      footerTagline: "सवालों से सत्यापित अगले कदम तक एक पुल।",
      footerDisclaimer: "प्रारम्भिक स्क्रीनिंग का प्रोटोटाइप। सरकारी पोर्टल और विभाग ही अंतिम प्राधिकरण हैं।",
      statusPromising: "संभावना · सत्यापित करें",
      statusNeeds: "जानकारी आवश्यक",
      statusNoMatch: "स्क्रीनिंग पर मेल नहीं",
      statusVerify: "आधिकारिक शर्तें जांचें",
      evidence: "नियम का साक्ष्य देखें",
      hideEvidence: "नियम का साक्ष्य छिपाएं",
      source: "आधिकारिक स्रोत",
      verified: "अंतिम सत्यापन",
      documents: "पुष्टि किए जाने वाले दस्तावेज़",
      matched: "मिला",
      notMatched: "नहीं मिला",
      missing: "अनुपलब्ध",
      signalToVerify: "जांचने वाला संकेत",
      whyItMatters: "यह क्यों ज़रूरी है",
      errorGeneric: "स्क्रीनिंग पूरी नहीं हो सकी। HaqSetu API चल रही है या नहीं जांचें और फिर प्रयास करें।",
      errorValidation: "विश्लेषण से पहले ज़रूरी फ़ील्ड पूरे करें।",
      noFeedback: "पहले बताएं कि यह उपयोगी था या नहीं।",
    },
  };

  let language = "en";
  let latestAnalysis = null;
  let traceTimer = null;
  let elapsedTimer = null;
  let analysisStartedAt = 0;

  // A static server on port 3000/5173 can host frontend/ while FastAPI runs on 8000.
  // FastAPI static mounts and same-origin deployments use the required relative path.
  const apiOrigin = ["3000", "5173"].includes(window.location.port) ? "http://127.0.0.1:8000" : "";

  function t(key) {
    return (text[language] && text[language][key]) || text.en[key] || key;
  }

  function escapeHTML(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function setLanguage(next) {
    language = next === "hi" ? "hi" : "en";
    document.documentElement.lang = language;
    $$('[data-i18n]').forEach((element) => {
      const key = element.dataset.i18n;
      if (text[language][key]) element.textContent = text[language][key];
    });
    $$('[data-i18n-placeholder]').forEach((element) => {
      const key = element.dataset.i18nPlaceholder;
      if (text[language][key]) element.placeholder = text[language][key];
    });
    $$('.language-option').forEach((button) => {
      const active = button.dataset.lang === language;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    if (latestAnalysis) renderAnalysis(latestAnalysis);
    updateNeedCount();
  }

  function value(id) {
    const element = document.getElementById(id);
    return element ? element.value.trim() : "";
  }

  function splitNeeds(raw) {
    return raw.split(/[,،;\n]+/).map((item) => item.trim()).filter(Boolean).slice(0, 20);
  }

  function formProfile() {
    const needsRaw = value("needs");
    return {
      name: value("name") || null,
      state: value("state"),
      age: Number(value("age")),
      occupation: value("occupation"),
      monthly_income: Number(value("income")),
      social_category: value("category"),
      landholding: Number(value("landholding") || 0),
      disability: $("#disability").checked,
      needs: splitNeeds(needsRaw),
      language,
    };
  }

  function setField(id, fieldValue) {
    const element = document.getElementById(id);
    if (element) element.value = fieldValue;
  }

  function applyScenario(name) {
    const scenarios = {
      farmer: { state: "Madhya Pradesh", age: 42, occupation: "small farmer", income: 12000, category: "OBC", landholding: 1.4, disability: false, needs: "income support, crop insurance, health" },
      vendor: { state: "Uttar Pradesh", age: 35, occupation: "street vendor", income: 15000, category: "SC", landholding: 0, disability: false, needs: "working capital loan, healthcare" },
      senior: { state: "Rajasthan", age: 68, occupation: "agricultural worker", income: 8000, category: "General", landholding: 0, disability: true, needs: "pension, health support" },
      student: { state: "Bihar", age: 19, occupation: "student", income: 8000, category: "OBC", landholding: 0, disability: false, needs: "post matric scholarship, education" },
    };
    const scenario = scenarios[name];
    if (!scenario) return;
    setField("state", scenario.state);
    setField("age", scenario.age);
    setField("occupation", scenario.occupation);
    setField("income", scenario.income);
    setField("category", scenario.category);
    setField("landholding", scenario.landholding);
    setField("needs", scenario.needs);
    $("#disability").checked = scenario.disability;
    $$(".scenario-chip").forEach((button) => button.classList.toggle("is-selected", button.dataset.scenario === name));
    updateNeedCount();
    $("#formAlert").hidden = true;
    $("#state").dispatchEvent(new Event("change", { bubbles: true }));
    $("#needs").focus({ preventScroll: true });
  }

  function updateNeedCount() {
    const needs = $("#needs");
    if (needs) $("#needCount").textContent = `${needs.value.length} / 500`;
  }

  function resetTrace() {
    clearTimeout(traceTimer);
    clearInterval(elapsedTimer);
    traceTimer = null;
    elapsedTimer = null;
    $$("#agentTimeline li").forEach((item) => {
      item.classList.remove("is-active", "is-complete", "is-error");
      const status = $(".agent-status", item);
      if (status) status.textContent = t("waiting");
    });
    $("#traceElapsed").textContent = t("ready");
  }

  function setTraceStep(index, state) {
    const steps = $$("#agentTimeline li");
    steps.forEach((item, itemIndex) => {
      item.classList.remove("is-active", "is-complete", "is-error");
      const status = $(".agent-status", item);
      if (!status) return;
      if (state === "error" && itemIndex === index) {
        item.classList.add("is-error");
        status.textContent = t("traceError");
      } else if (itemIndex < index || state === "complete") {
        item.classList.add("is-complete");
        status.textContent = t("complete");
      } else if (itemIndex === index) {
        item.classList.add("is-active");
        status.textContent = t("working");
      } else {
        status.textContent = t("waiting");
      }
    });
  }

  function startTrace() {
    resetTrace();
    analysisStartedAt = Date.now();
    setTraceStep(0, "active");
    elapsedTimer = window.setInterval(() => {
      const elapsed = (Date.now() - analysisStartedAt) / 1000;
      $("#traceElapsed").textContent = `${elapsed.toFixed(1)}s`;
    }, 100);
    const steps = [
      { index: 1, delay: 380 },
      { index: 2, delay: 720 },
      { index: 3, delay: 1050 },
    ];
    let cursor = 0;
    const advance = () => {
      if (cursor >= steps.length) return;
      const current = steps[cursor++];
      traceTimer = window.setTimeout(() => {
        setTraceStep(current.index, "active");
        advance();
      }, current.delay - (cursor > 1 ? steps[cursor - 2].delay : 0));
    };
    advance();
  }

  function finishTrace(success) {
    clearTimeout(traceTimer);
    clearInterval(elapsedTimer);
    traceTimer = null;
    elapsedTimer = null;
    if (success) {
      setTraceStep(4, "complete");
      const elapsed = (Date.now() - analysisStartedAt) / 1000;
      $("#traceElapsed").textContent = `${elapsed.toFixed(1)}s`;
    } else {
      setTraceStep(0, "error");
      $("#traceElapsed").textContent = t("traceError");
    }
  }

  async function apiRequest(path, options) {
    const response = await fetch(`${apiOrigin}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options && options.headers ? options.headers : {}) },
    });
    let payload = null;
    try { payload = await response.json(); } catch (_) { /* keep a generic error */ }
    if (!response.ok) {
      const error = new Error("API request failed");
      error.status = response.status;
      error.payload = payload;
      throw error;
    }
    return payload;
  }

  function setLoading(isLoading) {
    const button = $("#analyzeButton");
    button.disabled = isLoading;
    button.classList.toggle("is-loading", isLoading);
    $(".button-label", button).textContent = isLoading ? (language === "hi" ? "विश्लेषण हो रहा है…" : "Analyzing…") : t("analyze");
    $("#profileForm").setAttribute("aria-busy", String(isLoading));
  }

  function showFormError(message) {
    const alert = $("#formAlert");
    alert.textContent = message;
    alert.hidden = false;
    alert.focus({ preventScroll: true });
  }

  function clearFormError() { $("#formAlert").hidden = true; }

  function statusLabel(status) {
    if (status === "promising_signal_verify_officially") return t("statusPromising");
    if (status === "needs_information") return t("statusNeeds");
    if (status === "not_matched_on_screening") return t("statusNoMatch");
    return t("statusVerify");
  }

  function evidenceResultLabel(result) {
    if (result === "matched") return t("matched");
    if (result === "missing") return t("missing");
    return t("notMatched");
  }

  function safeStatus(status) { return knownStatuses.has(status) ? status : "verify_official_criteria"; }

  function renderSchemeCard(scheme, evidence, citation, rank) {
    const status = safeStatus(scheme.screening_status || (evidence && evidence.status));
    const rules = evidence && Array.isArray(evidence.evidence) ? evidence.evidence : [];
    const docs = evidence && Array.isArray(evidence.required_documents) ? evidence.required_documents : [];
    const source = citation && citation.source ? citation.source : (scheme.source || {});
    const tags = Array.isArray(scheme.tags) ? scheme.tags : [];
    const evidenceRows = rules.length
      ? rules.map((rule) => `<li class="evidence-item"><span class="evidence-dot ${escapeHTML(rule.result)}">${rule.result === "matched" ? "✓" : rule.result === "missing" ? "?" : "×"}</span><div><strong>${escapeHTML(rule.field)} · ${escapeHTML(evidenceResultLabel(rule.result))}</strong><p>${escapeHTML(rule.explanation || "")}</p></div></li>`).join("")
      : `<li class="evidence-item"><span class="evidence-dot missing">?</span><div><strong>${escapeHTML(t("missing"))}</strong><p>${escapeHTML(t("readinessNote"))}</p></div></li>`;
    const documentRow = docs.length ? `<div class="documents"><strong>${escapeHTML(t("documents"))}:</strong> ${escapeHTML(docs.join("; "))}</div>` : "";
    const lastVerified = source.last_verified ? `<span class="source-meta">${escapeHTML(t("verified"))}: ${escapeHTML(source.last_verified)} · ${escapeHTML(source.freshness || "manual verification required")}</span>` : "";
    return `<article class="scheme-card" data-scheme-id="${escapeHTML(scheme.id)}">
      <div class="scheme-card-top">
        <span class="scheme-rank">0${rank}</span>
        <div class="scheme-identity"><h4>${escapeHTML(scheme.name || "Government scheme")}</h4><p class="scheme-ministry">${escapeHTML(scheme.ministry || "Government programme")}</p></div>
        <span class="status-badge status-${status}">${escapeHTML(statusLabel(status))}</span>
      </div>
      <p class="scheme-summary">${escapeHTML(scheme.summary || "")}</p>
      <div class="scheme-tags">${tags.slice(0, 4).map((tag) => `<span>${escapeHTML(tag)}</span>`).join("")}</div>
      <div class="scheme-divider"></div>
      <div class="scheme-bottom">
        <button type="button" class="evidence-toggle" aria-expanded="false"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="m5 7 5 5 5-5"/></svg><span>${escapeHTML(t("evidence"))}</span></button>
        ${source.url ? `<a class="official-link" href="${escapeHTML(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(t("source"))}<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M11 4h5v5M16 4l-7 7M16 11v5H4V4h5"/></svg></a>` : ""}
      </div>
      <div class="evidence-panel" hidden><ul class="evidence-list">${evidenceRows}</ul>${documentRow}${lastVerified}</div>
    </article>`;
  }

  function renderActionPlan(actions) {
    const element = $("#actionPlan");
    if (!Array.isArray(actions) || !actions.length) {
      element.innerHTML = `<li>${escapeHTML(t("allFacts"))}</li>`;
      return;
    }
    element.innerHTML = actions.map((action) => `<li>${escapeHTML(action.step || "")}</li>`).join("");
  }

  function renderMissingFacts(missing, counterfactuals) {
    const element = $("#missingFacts");
    const facts = Array.isArray(missing) ? missing : [];
    const whatIf = Array.isArray(counterfactuals) ? counterfactuals : [];
    if (!facts.length && !whatIf.length) {
      element.innerHTML = `<p class="all-set">${escapeHTML(t("allFacts"))}</p>`;
      return;
    }
    const factGroups = facts.slice(0, 6).map((entry) => {
      const facts = Array.isArray(entry.facts) ? [...new Set(entry.facts)] : [];
      return `<div class="missing-group"><strong>${escapeHTML(entry.scheme_name || "Scheme")}</strong><ul>${facts.slice(0, 5).map((fact) => `<li>${escapeHTML(fact)}</li>`).join("")}</ul></div>`;
    }).join("");
    const counterfactualRows = whatIf.slice(0, 8).map((item) => `<div class="counterfactual-row"><div class="counterfactual-top"><span class="counterfactual-dot">↗</span><strong>${escapeHTML(item.scheme_name || "Scheme")}</strong></div><p><b>${escapeHTML(t("signalToVerify"))}:</b> ${escapeHTML(item.signal || "")}</p><p class="counterfactual-why"><b>${escapeHTML(t("whyItMatters"))}:</b> ${escapeHTML(item.why_it_matters || "")}</p></div>`).join("");
    element.innerHTML = `${factGroups}${counterfactualRows ? `<div class="counterfactual-list"><span class="counterfactual-label">${escapeHTML(t("counterfactual"))}</span>${counterfactualRows}</div>` : ""}`;
  }

  function renderAnalysis(payload) {
    latestAnalysis = payload;
    const trace = payload && payload.trace ? payload.trace : {};
    const retrieved = Array.isArray(trace.retrieved_schemes) ? trace.retrieved_schemes : [];
    const evidence = new Map((Array.isArray(trace.eligibility_evidence) ? trace.eligibility_evidence : []).map((item) => [item.scheme_id, item]));
    const citations = new Map((Array.isArray(trace.citations) ? trace.citations : []).map((item) => [item.scheme_id, item]));
    $("#schemeCards").innerHTML = retrieved.map((scheme, index) => renderSchemeCard(scheme, evidence.get(scheme.id), citations.get(scheme.id), index + 1)).join("");
    const score = Math.max(0, Math.min(100, Number(trace.readiness_score) || 0));
    $("#scoreValue").textContent = String(score);
    $("#scoreRing").style.setProperty("--score", score);
    $("#scoreRing").setAttribute("aria-label", `${t("readiness")}: ${score} / 100`);
    $("#scoreBar").style.width = `${score}%`;
    $("#readinessTitle").textContent = score >= 65 ? t("readinessTitle") : t("readinessIncomplete");
    $("#readinessNote").textContent = trace.readiness_note || t("readinessNote");
    $("#reportDisclaimer").textContent = payload.disclaimer || t("footerDisclaimer");
    $("#schemeCount").textContent = String(retrieved.length);
    $("#citationCount").textContent = String(Array.isArray(trace.citations) ? trace.citations.length : 0);
    $("#timeSaved").textContent = trace.estimated_time_saved || `${Number(trace.estimated_time_saved_minutes) || 0}m`;
    $("#analysisId").textContent = payload.analysis_id ? `ID ${payload.analysis_id}` : "";
    renderActionPlan(trace.action_plan);
    renderMissingFacts(trace.missing_facts, trace.counterfactuals);
    $("#consentCheck").checked = false;
    $("#draftButton").disabled = true;
    $("#draftOutput").hidden = true;
    $("#feedbackStatus").textContent = "";
    $("#results").hidden = false;
  }

  function prepareDraft() {
    if (!latestAnalysis || !latestAnalysis.trace) return;
    const trace = latestAnalysis.trace;
    const schemes = (trace.retrieved_schemes || []).slice(0, 3);
    const sources = (trace.citations || []).slice(0, 3);
    const names = new Set(schemes.map((scheme) => scheme.name));
    const steps = (trace.action_plan || []).map((action) => action.step).filter(Boolean);
    const items = [...steps, ...sources.map((source) => `${source.name}: ${source.source && source.source.title ? source.source.title : t("source")}`)];
    $("#draftOutput").innerHTML = `<h4>${escapeHTML(t("draftTitle"))}</h4><p>${escapeHTML(t("draftBody"))}</p><ul>${items.slice(0, 7).map((item) => `<li>${escapeHTML(item)}</li>`).join("")}</ul>`;
    $("#draftOutput").hidden = false;
    $("#draftOutput").scrollIntoView({ behavior: document.body.classList.contains("low-bandwidth") ? "auto" : "smooth", block: "nearest" });
    // Referencing names keeps this panel useful even if an API omits action steps.
    if (!items.length && names.size) $("#draftOutput").innerHTML += `<p>${escapeHTML([...names].join(", "))}</p>`;
  }

  async function analyze(event) {
    event.preventDefault();
    clearFormError();
    const form = $("#profileForm");
    if (!form.checkValidity()) {
      showFormError(t("errorValidation"));
      form.reportValidity();
      return;
    }
    const profile = formProfile();
    setLoading(true);
    startTrace();
    try {
      const result = await apiRequest("/api/analyze", { method: "POST", body: JSON.stringify({ profile }) });
      if (!result || !result.trace) throw new Error("Incomplete response");
      finishTrace(true);
      renderAnalysis(result);
      window.setTimeout(() => $("#results").scrollIntoView({ behavior: document.body.classList.contains("low-bandwidth") ? "auto" : "smooth", block: "start" }), 60);
    } catch (error) {
      finishTrace(false);
      showFormError(t("errorGeneric"));
    } finally {
      setLoading(false);
    }
  }

  async function sendFeedback(event) {
    event.preventDefault();
    const form = $("#feedbackForm");
    const selected = $("input[name='helpful']:checked", form);
    const status = $("#feedbackStatus");
    if (!selected) { status.textContent = t("noFeedback"); status.className = "feedback-status error"; return; }
    const helpful = selected.value === "true";
    const button = $(".text-button", form);
    button.disabled = true;
    try {
      await apiRequest("/api/feedback", { method: "POST", body: JSON.stringify({ analysis_id: latestAnalysis && latestAnalysis.analysis_id, helpful, rating: helpful ? 5 : 2, comment: value("feedbackComment") || null }) });
      status.textContent = t("feedbackThanks");
      status.className = "feedback-status success";
      form.reset();
    } catch (_) {
      status.textContent = t("errorGeneric");
      status.className = "feedback-status error";
    } finally { button.disabled = false; }
  }

  function toggleBandwidth() {
    const enabled = !document.body.classList.contains("low-bandwidth");
    document.body.classList.toggle("low-bandwidth", enabled);
    $("#bandwidthToggle").setAttribute("aria-pressed", String(enabled));
    try { localStorage.setItem("haqsetu-low-bandwidth", String(enabled)); } catch (_) { /* privacy-friendly fallback */ }
  }

  document.addEventListener("DOMContentLoaded", () => {
    let lowBandwidth = false;
    try { lowBandwidth = localStorage.getItem("haqsetu-low-bandwidth") === "true"; } catch (_) { /* no storage */ }
    if (lowBandwidth) { document.body.classList.add("low-bandwidth"); $("#bandwidthToggle").setAttribute("aria-pressed", "true"); }
    setLanguage("en");
    resetTrace();
    $("#profileForm").addEventListener("submit", analyze);
    $("#feedbackForm").addEventListener("submit", sendFeedback);
    $("#needs").addEventListener("input", updateNeedCount);
    $("#bandwidthToggle").addEventListener("click", toggleBandwidth);
    $("#consentCheck").addEventListener("change", (event) => { $("#draftButton").disabled = !event.target.checked; });
    $("#draftButton").addEventListener("click", prepareDraft);
    $$(".language-option").forEach((button) => button.addEventListener("click", () => setLanguage(button.dataset.lang)));
    $$(".scenario-chip").forEach((button) => button.addEventListener("click", () => applyScenario(button.dataset.scenario)));
    $("#schemeCards").addEventListener("click", (event) => {
      const button = event.target.closest(".evidence-toggle");
      if (!button) return;
      const card = button.closest(".scheme-card");
      const panel = $(".evidence-panel", card);
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      panel.hidden = expanded;
      card.classList.toggle("is-expanded", !expanded);
      $("span", button).textContent = expanded ? t("evidence") : t("hideEvidence");
    });
  });
})();
