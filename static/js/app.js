/**
 * PulsePM Application Controller (V2 Product Feedback Intelligence Platform)
 * Handles smart multi-product selection, live Apple App Store review retrieval,
 * debounced search auto-suggest, opportunity scoring, customer voice extraction,
 * interactive 3-horizon roadmap modal, and executive product briefs.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements - Product Selector & Search
  const appSearchInput = document.getElementById('app-search-input');
  const btnSearchClear = document.getElementById('btn-search-clear');
  const searchResultsDropdown = document.getElementById('search-results-dropdown');
  const categoryTabs = document.getElementById('category-tabs');
  const popularAppsGrid = document.getElementById('popular-apps-grid');
  const btnToggleManual = document.getElementById('btn-toggle-manual');
  const manualInputBody = document.getElementById('manual-input-body');

  // DOM Elements - Manual Input Area
  const reviewsInput = document.getElementById('reviews-input');
  const detectedCounter = document.getElementById('detected-counter');
  const btnClear = document.getElementById('btn-clear');
  const btnAnalyze = document.getElementById('btn-analyze');

  // Loading, Alerts & Containers
  const loadingState = document.getElementById('loading-state');
  const loadingTitle = document.getElementById('loading-title');
  const loadingSubtitle = document.getElementById('loading-subtitle');
  const errorAlert = document.getElementById('error-alert');
  const errorMessage = document.getElementById('error-message');
  const provenanceBanner = document.getElementById('provenance-banner');
  const dashboardResults = document.getElementById('dashboard-results');

  // Provenance Banner Elements
  const provenanceIcon = document.getElementById('provenance-icon');
  const provenanceAppName = document.getElementById('provenance-app-name');
  const provenanceCategory = document.getElementById('provenance-category');
  const provenanceRating = document.getElementById('provenance-rating');
  const provenanceSource = document.getElementById('provenance-source');
  const provenanceSourceText = document.getElementById('provenance-source-text');
  const provenanceCountText = document.getElementById('provenance-count-text');
  const provenanceTimeText = document.getElementById('provenance-time-text');
  const btnSwitchApp = document.getElementById('btn-switch-app');

  // KPI Elements
  const kpiTotal = document.getElementById('kpi-total-reviews');
  const kpiNetSentiment = document.getElementById('kpi-net-sentiment');
  const kpiBreakdown = document.getElementById('kpi-sentiment-breakdown');
  const kpiDominantTheme = document.getElementById('kpi-dominant-theme');
  const kpiDominantCount = document.getElementById('kpi-dominant-count');
  const kpiTopRisk = document.getElementById('kpi-top-risk');
  const kpiRiskBadge = document.getElementById('kpi-risk-badge');

  // Section Containers
  const opportunitiesContainer = document.getElementById('opportunities-container');
  const userRequestsContainer = document.getElementById('user-requests-container');
  const requestTypeFilters = document.getElementById('request-type-filters');
  const roadmapNowCount = document.getElementById('roadmap-now-count');
  const roadmapNextCount = document.getElementById('roadmap-next-count');
  const roadmapLaterCount = document.getElementById('roadmap-later-count');
  const roadmapNowItems = document.getElementById('roadmap-now-items');
  const roadmapNextItems = document.getElementById('roadmap-next-items');
  const roadmapLaterItems = document.getElementById('roadmap-later-items');
  const painPointsContainer = document.getElementById('pain-points-container');
  const reviewsListContainer = document.getElementById('reviews-list-container');
  const sentimentFilters = document.getElementById('sentiment-filters');
  const themeFilterSelect = document.getElementById('theme-filter-select');
  const reviewSearch = document.getElementById('review-search');

  // Product Brief
  const briefWrapper = document.getElementById('brief-content-wrapper');
  const btnCopyBrief = document.getElementById('btn-copy-brief');
  const btnPrintBrief = document.getElementById('btn-print-brief');

  // Roadmap Modal Elements
  const roadmapModal = document.getElementById('roadmap-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const modalThemeBadge = document.getElementById('modal-theme-badge');
  const modalHorizonBadge = document.getElementById('modal-horizon-badge');
  const modalPosBadge = document.getElementById('modal-pos-badge');
  const modalItemTitle = document.getElementById('modal-item-title');
  const modalItemProblem = document.getElementById('modal-item-problem');
  const modalItemWant = document.getElementById('modal-item-want');
  const modalItemAction = document.getElementById('modal-item-action');
  const modalItemReason = document.getElementById('modal-item-reason');
  const modalItemMetric = document.getElementById('modal-item-metric');
  const modalItemCount = document.getElementById('modal-item-count');

  // State Management
  let curatedAppsList = [];
  let currentAnalysis = null;
  let activeCategoryFilter = 'all';
  let activeSentimentFilter = 'all';
  let activeThemeFilter = 'all';
  let activeSearchQuery = '';
  let activeRequestFilter = 'all';
  let searchDebounceTimer = null;

  // =========================================================================
  // 1. Initialize Curated Popular Apps & Category Filtering
  // =========================================================================
  async function loadCuratedApps() {
    try {
      const res = await fetch('/api/products/curated');
      if (!res.ok) throw new Error('Failed to load apps');
      const data = await res.json();
      curatedAppsList = data.products || [];
      renderPopularApps(curatedAppsList);
    } catch (err) {
      console.warn('Could not load curated apps:', err);
    }
  }

  function renderPopularApps(apps) {
    if (!popularAppsGrid) return;
    popularAppsGrid.innerHTML = '';

    const filtered = apps.filter(app => {
      if (activeCategoryFilter === 'all') return true;
      return app.category === activeCategoryFilter;
    });

    if (filtered.length === 0) {
      popularAppsGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted);">
          No apps found in this category.
        </div>
      `;
      return;
    }

    filtered.forEach(app => {
      const card = document.createElement('div');
      card.className = 'app-quick-card';
      card.setAttribute('data-id', app.product_id);
      card.setAttribute('data-name', app.product_name);
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      card.setAttribute('title', `Analyze public customer feedback for ${app.product_name}`);

      card.innerHTML = `
        <div class="app-card-top">
          <img class="app-icon" src="${escapeHtml(app.icon_url)}" alt="${escapeHtml(app.product_name)} Icon" loading="lazy" />
          <div class="app-card-text">
            <h3 class="app-name">${escapeHtml(app.product_name)}</h3>
            <span class="app-developer">${escapeHtml(app.developer || app.category)}</span>
          </div>
        </div>
        <div class="app-card-bottom">
          <span class="app-cat-tag">${escapeHtml(app.category)}</span>
          <span class="app-rating">⭐ ${app.rating || '4.5'}</span>
        </div>
        <div class="app-card-hover-action">
          <span>Analyze Feedback ➔</span>
        </div>
      `;

      card.addEventListener('click', () => {
        triggerProductAnalysis(app.product_id, app.product_name);
      });

      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerProductAnalysis(app.product_id, app.product_name);
        }
      });

      popularAppsGrid.appendChild(card);
    });
  }

  // Category Tabs Filter
  if (categoryTabs) {
    categoryTabs.addEventListener('click', (e) => {
      const btn = e.target.closest('.cat-pill');
      if (!btn) return;
      categoryTabs.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategoryFilter = btn.getAttribute('data-cat');
      renderPopularApps(curatedAppsList);
    });
  }

  // =========================================================================
  // 2. Search Autocomplete & Live Public App Store Query
  // =========================================================================
  if (appSearchInput) {
    appSearchInput.addEventListener('input', () => {
      const query = appSearchInput.value.trim();
      if (btnSearchClear) {
        btnSearchClear.classList.toggle('hidden', query.length === 0);
      }

      clearTimeout(searchDebounceTimer);
      if (query.length < 2) {
        hideSearchDropdown();
        return;
      }

      searchDebounceTimer = setTimeout(async () => {
        await executeAppSearch(query);
      }, 250);
    });

    appSearchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        hideSearchDropdown();
      }
    });
  }

  if (btnSearchClear) {
    btnSearchClear.addEventListener('click', () => {
      appSearchInput.value = '';
      btnSearchClear.classList.add('hidden');
      hideSearchDropdown();
      appSearchInput.focus();
    });
  }

  async function executeAppSearch(query) {
    try {
      searchResultsDropdown.innerHTML = `
        <div class="search-dropdown-loading">
          <div class="spinner-sm"></div>
          <span>Searching Apple App Store & Curated Products...</span>
        </div>
      `;
      searchResultsDropdown.classList.remove('hidden');

      const res = await fetch(`/api/products/search?q=${encodeURIComponent(query)}`);
      if (!res.ok) throw new Error('Search failed');
      const results = await res.json();

      renderSearchDropdownResults(results, query);
    } catch (err) {
      searchResultsDropdown.innerHTML = `
        <div class="search-dropdown-empty">Search unavailable. Try selecting a popular app below.</div>
      `;
    }
  }

  function renderSearchDropdownResults(results, query) {
    if (!results || results.length === 0) {
      searchResultsDropdown.innerHTML = `
        <div class="search-dropdown-empty">No products found matching "${escapeHtml(query)}".</div>
      `;
      return;
    }

    searchResultsDropdown.innerHTML = '';
    results.forEach(item => {
      const row = document.createElement('div');
      row.className = 'search-dropdown-item';
      row.setAttribute('tabindex', '0');

      row.innerHTML = `
        <img class="search-item-icon" src="${escapeHtml(item.icon_url || 'https://via.placeholder.com/48')}" alt="${escapeHtml(item.product_name)}" />
        <div class="search-item-info">
          <div class="search-item-title-row">
            <span class="search-item-name">${escapeHtml(item.product_name)}</span>
            <span class="search-item-source">${escapeHtml(item.source)}</span>
          </div>
          <div class="search-item-sub">
            <span>${escapeHtml(item.developer || item.category)}</span>
            <span>•</span>
            <span>⭐ ${item.rating || '4.5'}</span>
            <span>•</span>
            <span>${escapeHtml(item.category)}</span>
          </div>
        </div>
        <button class="btn btn-primary btn-sm search-item-btn">Analyze ➔</button>
      `;

      row.addEventListener('click', () => {
        hideSearchDropdown();
        appSearchInput.value = item.product_name;
        triggerProductAnalysis(item.product_id, item.product_name);
      });

      row.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          row.click();
        }
      });

      searchResultsDropdown.appendChild(row);
    });
  }

  function hideSearchDropdown() {
    if (searchResultsDropdown) searchResultsDropdown.classList.add('hidden');
  }

  // Close dropdown on outside click
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-bar-wrapper')) {
      hideSearchDropdown();
    }
  });

  // =========================================================================
  // 3. Automated Review Retrieval & Analysis Pipeline
  // =========================================================================
  async function triggerProductAnalysis(productId, productName) {
    hideError();
    dashboardResults.classList.add('hidden');
    provenanceBanner.classList.add('hidden');

    loadingState.classList.remove('hidden');
    loadingTitle.textContent = `Retrieving public reviews for ${productName}...`;
    loadingSubtitle.textContent = `Fetching latest reviews from Apple App Store RSS & running intelligence pipeline...`;

    // Smooth scroll to loading
    loadingState.scrollIntoView({ behavior: 'smooth', block: 'center' });

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: String(productId),
          product_name: productName,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to retrieve or analyze feedback.');
      }

      const data = await res.json();
      currentAnalysis = data;
      renderDashboard(data);

      // Render Provenance Banner
      renderProvenanceBanner(data);

      setTimeout(() => {
        provenanceBanner.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 120);

    } catch (err) {
      showError(`Analysis failed: ${err.message}`);
    } finally {
      loadingState.classList.add('hidden');
    }
  }

  function renderProvenanceBanner(data) {
    const meta = data.source_meta || {};
    provenanceAppName.textContent = data.product_name || meta.product_name || 'Customer App';
    provenanceCategory.textContent = data.product_category || meta.product_category || 'Consumer App';
    provenanceRating.textContent = meta.rating ? `⭐ ${meta.rating}` : '⭐ 4.6';

    if (data.product_icon_url || meta.product_icon_url) {
      provenanceIcon.src = data.product_icon_url || meta.product_icon_url;
      provenanceIcon.style.display = 'block';
    } else {
      provenanceIcon.style.display = 'none';
    }

    const isLive = meta.is_live_data !== false;
    if (isLive) {
      provenanceSource.className = 'provenance-source-badge live';
      provenanceSourceText.textContent = meta.source_name || 'Apple App Store (Public RSS)';
    } else {
      provenanceSource.className = 'provenance-source-badge fallback';
      provenanceSourceText.textContent = meta.source_name || 'Verified Dataset (Offline Mode)';
    }

    provenanceCountText.textContent = `${data.sentiment_summary.total_reviews} Reviews Analyzed`;
    provenanceTimeText.textContent = meta.fetch_timestamp ? `Fetched: ${meta.fetch_timestamp}` : 'Just now';

    provenanceBanner.classList.remove('hidden');
  }

  // Switch App Button
  if (btnSwitchApp) {
    btnSwitchApp.addEventListener('click', () => {
      const selectorSection = document.getElementById('product-selector-section');
      if (selectorSection) {
        selectorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (appSearchInput) appSearchInput.focus();
      }
    });
  }

  // =========================================================================
  // 4. Accordion Toggle for Manual Review Input
  // =========================================================================
  if (btnToggleManual && manualInputBody) {
    btnToggleManual.addEventListener('click', () => {
      const isCollapsed = manualInputBody.classList.toggle('collapsed');
      const arrow = btnToggleManual.querySelector('.accordion-icon');
      if (arrow) arrow.textContent = isCollapsed ? '▾' : '▴';
      btnToggleManual.classList.toggle('active', !isCollapsed);
    });
  }

  // Review Counter Helper
  function updateReviewCount() {
    const text = reviewsInput.value.trim();
    if (!text) {
      detectedCounter.textContent = '0 reviews detected';
      return;
    }
    const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 5);
    const count = lines.length;
    detectedCounter.textContent = `${count} review${count === 1 ? '' : 's'} detected`;
  }

  if (reviewsInput) reviewsInput.addEventListener('input', updateReviewCount);

  // Multi-Domain Sample Loader (Zomato, Amazon, SaaS)
  async function loadSampleReviews(dataset, buttonElem) {
    const originalHtml = buttonElem.innerHTML;
    try {
      buttonElem.disabled = true;
      buttonElem.innerHTML = `<span>Loading...</span>`;

      const response = await fetch(`/api/sample?dataset=${encodeURIComponent(dataset)}`);
      if (!response.ok) throw new Error('Failed to fetch sample data');
      const data = await response.json();

      const formatted = data.reviews.map((rev, idx) => `${idx + 1}. ${rev}`).join('\n\n');
      reviewsInput.value = formatted;
      updateReviewCount();
      hideError();
    } catch (err) {
      showError(`Could not load ${dataset} reviews: ` + err.message);
    } finally {
      buttonElem.disabled = false;
      buttonElem.innerHTML = originalHtml;
    }
  }

  document.querySelectorAll('.sample-btn-group button').forEach(btn => {
    btn.addEventListener('click', async () => {
      const dataset = btn.getAttribute('data-dataset') || 'zomato';
      document.querySelectorAll('.sample-btn-group button').forEach(b => b.classList.remove('active-sample'));
      btn.classList.add('active-sample');
      await loadSampleReviews(dataset, btn);
    });
  });

  if (btnClear) {
    btnClear.addEventListener('click', () => {
      reviewsInput.value = '';
      updateReviewCount();
      hideError();
    });
  }

  // Manual Review Analysis Submission
  if (btnAnalyze) {
    btnAnalyze.addEventListener('click', async () => {
      const text = reviewsInput.value.trim();
      if (!text) {
        showError('Please paste customer reviews or select one of the pre-loaded sample datasets.');
        return;
      }

      hideError();
      loadingState.classList.remove('hidden');
      loadingTitle.textContent = 'Analyzing customer reviews...';
      loadingSubtitle.textContent = 'Scoring product opportunities, classifying themes & compiling roadmap...';
      dashboardResults.classList.add('hidden');
      provenanceBanner.classList.add('hidden');
      btnAnalyze.disabled = true;

      try {
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            raw_text: text,
            product_name: 'Custom Pasted Reviews',
          }),
        });

        if (!res.ok) {
          const errorData = await res.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Analysis failed. Please check review format.');
        }

        const data = await res.json();
        currentAnalysis = data;
        renderDashboard(data);
        renderProvenanceBanner(data);

        setTimeout(() => {
          dashboardResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

      } catch (err) {
        showError(err.message);
      } finally {
        loadingState.classList.add('hidden');
        btnAnalyze.disabled = false;
      }
    });
  }

  // =========================================================================
  // 5. Master Dashboard Renderer
  // =========================================================================
  function renderDashboard(data) {
    const {
      sentiment_summary,
      theme_stats,
      top_pain_points,
      product_opportunities,
      user_requests,
      roadmap,
      reviews,
      product_brief
    } = data;

    // 1. KPI Cards
    kpiTotal.textContent = sentiment_summary.total_reviews;
    const sign = sentiment_summary.net_sentiment_score >= 0 ? '+' : '';
    kpiNetSentiment.textContent = `${sign}${sentiment_summary.net_sentiment_score.toFixed(1)}%`;
    kpiBreakdown.textContent = `${sentiment_summary.positive_pct}% Pos vs ${sentiment_summary.negative_pct}% Neg`;

    if (theme_stats && theme_stats.length > 0) {
      kpiDominantTheme.textContent = theme_stats[0].theme;
      kpiDominantCount.textContent = `${theme_stats[0].count} mentions (${theme_stats[0].percentage}%)`;
    }

    if (product_opportunities && product_opportunities.length > 0) {
      const topOpp = product_opportunities[0];
      kpiTopRisk.textContent = topOpp.opportunity_title || topOpp.theme;
      kpiRiskBadge.textContent = `POS Score: ${topOpp.opportunity_score.total_score}/100`;
    } else if (top_pain_points && top_pain_points.length > 0) {
      kpiTopRisk.textContent = top_pain_points[0].theme;
      kpiRiskBadge.textContent = `Priority: ${top_pain_points[0].priority}`;
    }

    // 2. Charts
    window.Charts.renderSentimentDonut('sentiment-donut-wrapper', sentiment_summary);
    window.Charts.renderThemeBars('theme-bars-container', theme_stats);

    // 3. Compact Product Opportunity Cards (Section 6 & 7)
    renderOpportunities(product_opportunities);

    // 4. What Users Want (Section 5)
    renderUserRequests(user_requests);

    // 5. 3-Horizon Actionable Roadmap (Section 9 & 10)
    renderRoadmap(roadmap);

    // 6. Top 3 Pain Points (Preserved V1)
    renderPainPoints(top_pain_points);

    // 7. Reviews Explorer
    renderReviewsList(reviews);

    // 8. Product Brief
    renderProductBrief(product_brief);

    // Reveal Dashboard
    dashboardResults.classList.remove('hidden');
  }

  // =========================================================================
  // 6. Compact Product Opportunity Cards (Section 6 & 7 Spec)
  // Short, visual, quick to understand in 5 seconds. Detailed reasoning in drawer.
  // =========================================================================
  function renderOpportunities(opportunities) {
    if (!opportunitiesContainer) return;
    opportunitiesContainer.innerHTML = '';

    if (!opportunities || opportunities.length === 0) {
      opportunitiesContainer.innerHTML = '<p class="text-secondary">No product opportunities identified.</p>';
      return;
    }

    opportunities.forEach(opp => {
      const card = document.createElement('div');
      card.className = 'opportunity-card';

      const score = opp.opportunity_score;
      const totalScore = score.total_score;
      const impactText = opp.impact_badge || (totalScore >= 75 ? 'CRITICAL IMPACT' : totalScore >= 50 ? 'HIGH IMPACT' : 'MEDIUM IMPACT');
      let impactClass = 'impact-medium';
      if (impactText.includes('CRITICAL')) impactClass = 'impact-critical';
      else if (impactText.includes('HIGH')) impactClass = 'impact-high';

      const title = opp.opportunity_title || opp.feature_recommendation;
      const userWant = opp.users_want_short || opp.pain_point;
      const action = opp.recommended_action_short || opp.feature_recommendation;

      const quotesHtml = opp.evidence.supporting_excerpts && opp.evidence.supporting_excerpts.length > 0
        ? opp.evidence.supporting_excerpts.map(q => `<p class="customer-quote">"${escapeHtml(q)}"</p>`).join('')
        : '<p class="customer-quote">Direct feedback observed across multiple reviews.</p>';

      card.innerHTML = `
        <div class="opportunity-card-top">
          <div class="opp-title-group">
            <span class="opp-rank-pill">#${opp.rank}</span>
            <div class="opp-header-meta">
              <div class="opp-main-title">
                <span class="opp-title-text">${escapeHtml(title)}</span>
                <span class="opp-badges-inline">
                  <span class="opp-theme-pill">${escapeHtml(opp.theme)}</span>
                  <span class="opp-impact-badge ${impactClass}">${escapeHtml(impactText)}</span>
                  <span class="roadmap-horizon-pill horizon-${opp.roadmap_horizon.toLowerCase()}">⚡ ${opp.roadmap_horizon}</span>
                </span>
              </div>
            </div>
          </div>

          <div class="opp-scores-bar">
            <div class="pos-main-badge" title="Product Opportunity Score (0-100)">
              <span class="pos-label">Score:</span>
              <span class="pos-value-highlight">${totalScore} / 100</span>
            </div>
            <div class="pos-breakdown-chips" title="Formula: Frequency (0-30) + Severity (0-40) + User Impact (0-30)">
              <span>Freq: <strong>+${score.frequency_score}</strong></span>
              <span>•</span>
              <span>Sev: <strong>+${score.severity_score}</strong></span>
              <span>•</span>
              <span>Impact: <strong>+${score.user_impact_score}</strong></span>
            </div>
          </div>
        </div>

        <!-- Glanceable 2-Box Summary (Short & Visual, Understood in 5 seconds) -->
        <div class="opp-glance-grid">
          <div class="opp-glance-box glance-want">
            <span class="glance-tag">🎯 Users Want:</span>
            <p class="glance-text">${escapeHtml(userWant)}</p>
          </div>
          <div class="opp-glance-box glance-action">
            <span class="glance-tag">➔ Action:</span>
            <p class="glance-text">${escapeHtml(action)}</p>
          </div>
        </div>

        <!-- Collapsible Deep-Dive Drawer Toggle -->
        <div class="opp-drawer-toggle" role="button" tabindex="0" title="Click to view root cause, innovation flow, and evidence">
          <span>🔍 <strong>Why? View Evidence</strong> (${opp.evidence.review_count} supporting reviews • ${opp.evidence.percentage}% of feedback)</span>
          <svg class="opp-toggle-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </div>

        <!-- Collapsible Deep-Dive Content -->
        <div class="opp-drawer-content">
          <div class="opp-chain-flow">
            <div class="opp-chain-step">
              <span class="opp-step-indicator step-indicator-pain">1. Pain Point</span>
              <p class="opp-step-content">${escapeHtml(opp.pain_point)}</p>
            </div>
            <div class="opp-chain-step">
              <span class="opp-step-indicator step-indicator-root">2. Root Cause Hypothesis</span>
              <p class="opp-step-content">${escapeHtml(opp.root_cause_hypothesis)}</p>
            </div>
            <div class="opp-chain-step">
              <span class="opp-step-indicator step-indicator-opp">3. Product Opportunity</span>
              <p class="opp-step-content">${escapeHtml(opp.product_opportunity)}</p>
            </div>
            <div class="opp-chain-step">
              <span class="opp-step-indicator step-indicator-fix">4. Recommended Feature</span>
              <p class="opp-step-content"><strong>${escapeHtml(opp.feature_recommendation)}</strong></p>
            </div>
          </div>

          <div class="opp-evidence-box">
            <div class="opp-evidence-header">
              <span class="evidence-count-tag">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                Customer Evidence: ${opp.evidence.review_count} reviews (${opp.evidence.percentage}%)
              </span>
              <span class="metric-text" style="color: #6ee7b7; font-size: 0.8rem; font-weight: 600;">
                🎯 Target Metric: ${escapeHtml(opp.success_metric)}
              </span>
            </div>

            <p class="opp-rationale"><strong>PM Rationale:</strong> ${escapeHtml(opp.evidence.reason_for_recommendation)}</p>

            <div class="opp-excerpts-list">
              <span class="quote-label">Direct Customer Voices:</span>
              ${quotesHtml}
            </div>
          </div>
        </div>
      `;

      // Collapsible toggle handler
      const toggleBtn = card.querySelector('.opp-drawer-toggle');
      const drawerContent = card.querySelector('.opp-drawer-content');
      if (toggleBtn && drawerContent) {
        toggleBtn.addEventListener('click', () => {
          const isOpen = drawerContent.classList.toggle('show');
          toggleBtn.classList.toggle('active', isOpen);
        });
        toggleBtn.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleBtn.click();
          }
        });
      }

      opportunitiesContainer.appendChild(card);
    });
  }

  // =========================================================================
  // 7. What Users Want (Section 5 Spec)
  // =========================================================================
  function renderUserRequests(userRequests) {
    if (!userRequestsContainer) return;
    userRequestsContainer.innerHTML = '';

    if (!userRequests || userRequests.length === 0) {
      userRequestsContainer.innerHTML = '<p class="text-secondary">No specific user requests or inferred desires extracted.</p>';
      return;
    }

    const filtered = userRequests.filter(req => {
      if (activeRequestFilter === 'all') return true;
      return req.request_type === activeRequestFilter;
    });

    if (filtered.length === 0) {
      userRequestsContainer.innerHTML = '<p class="text-secondary" style="grid-column: 1/-1; padding: 1.5rem; text-align: center;">No requests match this category.</p>';
      return;
    }

    filtered.forEach(req => {
      const card = document.createElement('div');
      card.className = 'user-request-card';

      const isExplicit = req.request_type === 'Explicit Request';
      const badgeClass = isExplicit ? 'request-type-explicit' : 'request-type-inferred';
      const badgeIcon = isExplicit ? '✨' : '💡';

      const quotesHtml = req.supporting_excerpts && req.supporting_excerpts.length > 0
        ? `<p class="customer-quote">"${escapeHtml(req.supporting_excerpts[0])}"</p>`
        : '';

      card.innerHTML = `
        <div class="request-card-top">
          <span class="request-type-badge ${badgeClass}">${badgeIcon} ${req.request_type}</span>
          <span class="request-count-pill">${req.mention_count} supporting review${req.mention_count === 1 ? '' : 's'}</span>
        </div>

        <h3 class="request-title">${escapeHtml(req.title)}</h3>

        <div style="display: flex; flex-direction: column; gap: 0.35rem;">
          <span class="quote-label">Short Supporting Review Excerpt:</span>
          ${quotesHtml}
        </div>

        <div class="request-link-tag">
          <span>Connected Opportunity: <strong>${escapeHtml(req.linked_opportunity)}</strong></span>
          <span class="roadmap-horizon-pill horizon-${req.roadmap_horizon.toLowerCase()}">${req.roadmap_horizon}</span>
        </div>
      `;

      userRequestsContainer.appendChild(card);
    });
  }

  if (requestTypeFilters) {
    requestTypeFilters.addEventListener('click', (e) => {
      const target = e.target.closest('.pill');
      if (!target) return;

      requestTypeFilters.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      target.classList.add('active');

      activeRequestFilter = target.getAttribute('data-req-filter');
      if (currentAnalysis) renderUserRequests(currentAnalysis.user_requests);
    });
  }

  // =========================================================================
  // 8. Actionable Product Roadmap & Interactive Modal (Section 9 & 10 Spec)
  // =========================================================================
  function renderRoadmap(roadmap) {
    if (!roadmap) return;

    if (roadmapNowCount) roadmapNowCount.textContent = roadmap.now ? roadmap.now.length : 0;
    if (roadmapNextCount) roadmapNextCount.textContent = roadmap.next ? roadmap.next.length : 0;
    if (roadmapLaterCount) roadmapLaterCount.textContent = roadmap.later ? roadmap.later.length : 0;

    renderRoadmapColumn(roadmapNowItems, roadmap.now, 'NOW');
    renderRoadmapColumn(roadmapNextItems, roadmap.next, 'NEXT');
    renderRoadmapColumn(roadmapLaterItems, roadmap.later, 'LATER');
  }

  function renderRoadmapColumn(container, items, horizon) {
    if (!container) return;
    container.innerHTML = '';

    if (!items || items.length === 0) {
      container.innerHTML = `<p style="font-size: 0.8rem; color: var(--text-muted); text-align: center; padding: 1.5rem 0;">No initiatives scheduled for ${horizon}.</p>`;
      return;
    }

    items.forEach(item => {
      const card = document.createElement('div');
      card.className = 'roadmap-card-item';
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      card.setAttribute('title', 'Click to view problem, user desire, recommended action & OKR metric');

      const priorityClass = item.priority.toLowerCase();

      card.innerHTML = `
        <div class="roadmap-card-top">
          <span class="roadmap-theme-pill">${escapeHtml(item.theme)}</span>
          <div style="display: flex; gap: 0.4rem; align-items: center;">
            <span class="priority-pill priority-${priorityClass}">${item.priority}</span>
            <span class="roadmap-pos-badge">Score: ${item.opportunity_score}</span>
          </div>
        </div>

        <h4 class="roadmap-item-title">${escapeHtml(item.title)}</h4>
        <p class="roadmap-item-desc">${escapeHtml(item.description)}</p>

        <div class="roadmap-footer-hint">
          <span class="roadmap-metric-tag">🎯 ${escapeHtml(item.success_metric)}</span>
          <span class="roadmap-click-hint">Inspect Spec ➔</span>
        </div>
      `;

      // Open detail modal when clicked
      card.addEventListener('click', () => {
        openRoadmapModal(item);
      });

      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openRoadmapModal(item);
        }
      });

      container.appendChild(card);
    });
  }

  function openRoadmapModal(item) {
    if (!roadmapModal) return;

    modalItemTitle.textContent = item.title;
    modalThemeBadge.textContent = item.theme;
    modalHorizonBadge.textContent = `⚡ ${item.horizon}`;
    modalHorizonBadge.className = `roadmap-horizon-pill horizon-${item.horizon.toLowerCase()}`;
    modalPosBadge.textContent = `Opportunity Score: ${item.opportunity_score}/100`;

    modalItemProblem.textContent = item.problem || item.description;
    modalItemWant.textContent = item.what_users_want || 'Frictionless, reliable customer experience.';
    modalItemAction.textContent = item.recommended_action || item.title;
    modalItemReason.textContent = item.why_prioritized || item.reason || 'High impact opportunity identified from customer reviews.';
    modalItemMetric.textContent = item.success_metric || 'Improve domain CSAT score by 30%.';
    modalItemCount.textContent = item.review_count
      ? `Validated by ${item.review_count} supporting customer reviews`
      : 'Validated by recurring feedback signals';

    roadmapModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeRoadmapModal() {
    if (!roadmapModal) return;
    roadmapModal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', closeRoadmapModal);
  }

  if (roadmapModal) {
    roadmapModal.addEventListener('click', (e) => {
      if (e.target === roadmapModal) closeRoadmapModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && roadmapModal && !roadmapModal.classList.contains('hidden')) {
      closeRoadmapModal();
    }
  });

  // =========================================================================
  // 9. Top 3 Pain Points (Preserved V1 Intact)
  // =========================================================================
  function renderPainPoints(painPoints) {
    painPointsContainer.innerHTML = '';
    if (!painPoints || painPoints.length === 0) {
      painPointsContainer.innerHTML = '<p class="text-secondary">No significant pain points detected.</p>';
      return;
    }

    painPoints.forEach(item => {
      const card = document.createElement('div');
      const priorityClass = item.priority.toLowerCase();
      card.className = `pain-card pain-card-${priorityClass}`;

      const quotesHtml = item.representative_quotes && item.representative_quotes.length > 0
        ? item.representative_quotes.map(q => `<p class="customer-quote">"${escapeHtml(q)}"</p>`).join('')
        : '<p class="customer-quote">No direct negative quotes recorded.</p>';

      card.innerHTML = `
        <div class="pain-card-top">
          <div>
            <span class="pain-rank-badge">#${item.rank}</span>
            <h3 class="pain-theme-title">${escapeHtml(item.theme)}</h3>
          </div>
          <span class="priority-pill priority-${priorityClass}">${item.priority} Priority</span>
        </div>

        <div class="pain-stats-row">
          <div class="pain-stat-item">
            <span class="pain-stat-label">Total Mentions</span>
            <span class="pain-stat-val">${item.frequency}</span>
          </div>
          <div class="pain-stat-item">
            <span class="pain-stat-label">Negative Friction</span>
            <span class="pain-stat-val" style="color: #fb7185;">${item.negative_count} reviews</span>
          </div>
          <div class="pain-stat-item">
            <span class="pain-stat-label">Severity Score</span>
            <span class="pain-stat-val">${item.severity_score}</span>
          </div>
        </div>

        <div class="pain-quotes-box">
          <span class="quote-label">Direct Customer Voice:</span>
          ${quotesHtml}
        </div>

        <div class="feature-box">
          <span class="feature-title">💡 Recommended Product Feature / Fix</span>
          <p class="feature-text">${escapeHtml(item.recommended_feature)}</p>
        </div>

        <div class="metric-box">
          <span class="metric-title">🎯 Measurable Success Metric</span>
          <p class="metric-text">${escapeHtml(item.success_metric)}</p>
        </div>
      `;

      painPointsContainer.appendChild(card);
    });
  }

  // =========================================================================
  // 10. Filterable Reviews Explorer (Preserved V1 Intact)
  // =========================================================================
  function renderReviewsList(reviews) {
    if (!reviews) return;

    const filtered = reviews.filter(rev => {
      if (activeSentimentFilter !== 'all' && rev.sentiment !== activeSentimentFilter) {
        return false;
      }
      if (activeThemeFilter !== 'all' && !rev.themes.includes(activeThemeFilter)) {
        return false;
      }
      if (activeSearchQuery) {
        const q = activeSearchQuery.toLowerCase();
        const matchesText = rev.text.toLowerCase().includes(q);
        const matchesThemes = rev.themes.some(t => t.toLowerCase().includes(q));
        if (!matchesText && !matchesThemes) return false;
      }
      return true;
    });

    reviewsListContainer.innerHTML = '';

    if (filtered.length === 0) {
      reviewsListContainer.innerHTML = `
        <div style="padding: 2rem; text-align: center; color: var(--text-muted);">
          No reviews match the selected filter or search query.
        </div>
      `;
      return;
    }

    filtered.forEach(rev => {
      const item = document.createElement('div');
      item.className = 'review-card-item';

      const sentLower = rev.sentiment.toLowerCase();
      const themePills = rev.themes.map(t => `<span class="theme-pill-tag">${t}</span>`).join('');
      const painPills = rev.pain_flags && rev.pain_flags.length > 0
        ? `<div class="review-pain-flags">${rev.pain_flags.map(f => `<span class="pain-flag-badge">⚠️ ${escapeHtml(f)}</span>`).join('')}</div>`
        : '';

      const scoreSign = rev.sentiment_score >= 0 ? '+' : '';

      item.innerHTML = `
        <div class="review-card-top">
          <div class="review-tags-group">
            <span class="sentiment-tag ${sentLower}">${rev.sentiment} (${scoreSign}${rev.sentiment_score})</span>
            ${themePills}
          </div>
          <span style="font-size: 0.75rem; color: var(--text-muted);">Review #${rev.id}</span>
        </div>
        <p class="review-text">${escapeHtml(rev.text)}</p>
        ${painPills}
      `;

      reviewsListContainer.appendChild(item);
    });
  }

  if (sentimentFilters) {
    sentimentFilters.addEventListener('click', (e) => {
      const target = e.target.closest('.pill');
      if (!target) return;
      sentimentFilters.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      target.classList.add('active');
      activeSentimentFilter = target.getAttribute('data-filter');
      if (currentAnalysis) renderReviewsList(currentAnalysis.reviews);
    });
  }

  if (themeFilterSelect) {
    themeFilterSelect.addEventListener('change', (e) => {
      activeThemeFilter = e.target.value;
      if (currentAnalysis) renderReviewsList(currentAnalysis.reviews);
    });
  }

  if (reviewSearch) {
    reviewSearch.addEventListener('input', (e) => {
      activeSearchQuery = e.target.value.trim();
      if (currentAnalysis) renderReviewsList(currentAnalysis.reviews);
    });
  }

  // =========================================================================
  // 11. Upgraded Executive Product Brief (Section 11 Spec)
  // =========================================================================
  function renderProductBrief(brief) {
    if (!brief) return;

    briefWrapper.innerHTML = `
      <h1>${escapeHtml(brief.title)}</h1>
      <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
        PulsePM Intelligence Engine v2.0 • Provenance: <strong>${escapeHtml(brief.review_source || 'Apple App Store')}</strong> • Analyzed: ${brief.fetch_timestamp || 'Recently'}
      </p>

      <h2>1. Executive Summary</h2>
      <p>${escapeHtml(brief.executive_summary)}</p>

      <h2>2. Key Findings</h2>
      <ul>
        ${brief.key_findings.map(f => `<li>${formatMarkdownBold(f)}</li>`).join('')}
      </ul>

      <h2>3. Prioritized Roadmap & Proposed Fixes</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Domain Theme</th>
            <th>Priority</th>
            <th>Proposed Engineering / Product Fix</th>
          </tr>
        </thead>
        <tbody>
          ${brief.action_plan.map(a => `
            <tr>
              <td><strong>#${a.rank}</strong></td>
              <td>${escapeHtml(a.theme)}</td>
              <td><span class="priority-pill priority-${a.priority.toLowerCase()}">${a.priority}</span></td>
              <td>${escapeHtml(a.feature)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <h2>4. Target OKRs & Measurable Success Metrics</h2>
      <ul>
        ${brief.kpi_targets.map(t => `<li>${formatMarkdownBold(t)}</li>`).join('')}
      </ul>
    `;
  }

  if (btnCopyBrief) {
    btnCopyBrief.addEventListener('click', async () => {
      if (!currentAnalysis || !currentAnalysis.product_brief) return;
      try {
        await navigator.clipboard.writeText(currentAnalysis.product_brief.markdown);
        const originalText = btnCopyBrief.innerHTML;
        btnCopyBrief.innerHTML = `
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          Copied to Clipboard!
        `;
        setTimeout(() => {
          btnCopyBrief.innerHTML = originalText;
        }, 2000);
      } catch (err) {
        alert('Could not copy to clipboard. Please copy manually.');
      }
    });
  }

  if (btnPrintBrief) {
    btnPrintBrief.addEventListener('click', () => {
      window.print();
    });
  }

  // =========================================================================
  // 12. Helpers
  // =========================================================================
  function showError(msg) {
    errorMessage.textContent = msg;
    errorAlert.classList.remove('hidden');
    errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function hideError() {
    errorAlert.classList.add('hidden');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatMarkdownBold(str) {
    if (!str) return '';
    return escapeHtml(str).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  }

  // Load curated apps immediately on start
  loadCuratedApps();
});
