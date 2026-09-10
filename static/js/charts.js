/**
 * Charts module: Pure Vanilla SVG & DOM implementations
 * Zero external libraries, 100% offline, lightweight and responsive.
 */

const Charts = {
  /**
   * Render SVG Sentiment Donut Chart
   */
  renderSentimentDonut(wrapperId, sentimentSummary) {
    const wrapper = document.getElementById(wrapperId);
    if (!wrapper) return;

    const { positive_pct, neutral_pct, negative_pct, net_sentiment_score } = sentimentSummary;
    const totalPct = positive_pct + neutral_pct + negative_pct || 100;

    // SVG parameters
    const size = 220;
    const strokeWidth = 24;
    const radius = 75;
    const center = size / 2;
    const circumference = 2 * Math.PI * radius; // ~471.24

    // Calculate stroke lengths
    const posLength = (positive_pct / totalPct) * circumference;
    const neuLength = (neutral_pct / totalPct) * circumference;
    const negLength = (negative_pct / totalPct) * circumference;

    // Dash offsets (running cumulatively)
    const posOffset = 0;
    const neuOffset = -posLength;
    const negOffset = -(posLength + neuLength);

    const netScoreFormatted = `${net_sentiment_score >= 0 ? '+' : ''}${net_sentiment_score.toFixed(1)}%`;
    const netScoreColor = net_sentiment_score > 0 ? '#10b981' : net_sentiment_score < 0 ? '#f43f5e' : '#f59e0b';

    wrapper.innerHTML = `
      <svg class="donut-svg" viewBox="0 0 ${size} ${size}">
        <!-- Base Track -->
        <circle 
          cx="${center}" cy="${center}" r="${radius}" 
          fill="none" 
          stroke="rgba(255, 255, 255, 0.05)" 
          stroke-width="${strokeWidth}" 
        />
        
        <!-- Negative Arc -->
        <circle 
          cx="${center}" cy="${center}" r="${radius}" 
          fill="none" 
          stroke="#f43f5e" 
          stroke-width="${strokeWidth}"
          stroke-dasharray="${negLength} ${circumference}"
          stroke-dashoffset="${negOffset}"
          stroke-linecap="round"
          style="transition: stroke-dasharray 0.8s ease, stroke-dashoffset 0.8s ease;"
        />
        
        <!-- Neutral Arc -->
        <circle 
          cx="${center}" cy="${center}" r="${radius}" 
          fill="none" 
          stroke="#f59e0b" 
          stroke-width="${strokeWidth}"
          stroke-dasharray="${neuLength} ${circumference}"
          stroke-dashoffset="${neuOffset}"
          stroke-linecap="round"
          style="transition: stroke-dasharray 0.8s ease, stroke-dashoffset 0.8s ease;"
        />

        <!-- Positive Arc -->
        <circle 
          cx="${center}" cy="${center}" r="${radius}" 
          fill="none" 
          stroke="#10b981" 
          stroke-width="${strokeWidth}"
          stroke-dasharray="${posLength} ${circumference}"
          stroke-dashoffset="${posOffset}"
          stroke-linecap="round"
          style="transition: stroke-dasharray 0.8s ease, stroke-dashoffset 0.8s ease;"
        />
      </svg>
      
      <div class="donut-center-text">
        <span class="donut-center-score" style="color: ${netScoreColor}">${netScoreFormatted}</span>
        <span class="donut-center-label">Net Sentiment</span>
      </div>
    `;

    // Update legend values
    const posVal = document.getElementById('legend-pos-val');
    const neuVal = document.getElementById('legend-neu-val');
    const negVal = document.getElementById('legend-neg-val');

    if (posVal) posVal.textContent = `${sentimentSummary.positive_count} (${positive_pct}%)`;
    if (neuVal) neuVal.textContent = `${sentimentSummary.neutral_count} (${neutral_pct}%)`;
    if (negVal) negVal.textContent = `${sentimentSummary.negative_count} (${negative_pct}%)`;
  },

  /**
   * Render Theme Mention Frequency & Friction Bar Chart
   */
  renderThemeBars(containerId, themeStats) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';
    const maxCount = Math.max(...themeStats.map(t => t.count), 1);

    const themeIcons = {
      "Delivery": "🚚",
      "Payment": "💳",
      "Pricing": "🏷️",
      "UI": "📱",
      "Customer Support": "🎧",
      "Order Quality": "🍲",
      "Bugs": "🐛",
      "Offers/Coupons": "🎟️"
    };

    themeStats.forEach(stat => {
      const percentageOfMax = Math.round((stat.count / maxCount) * 100);
      const isHighFriction = stat.negative_count >= 2 || stat.severity_score >= 5.0;

      const row = document.createElement('div');
      row.className = 'theme-bar-row';
      row.innerHTML = `
        <div class="theme-bar-header">
          <span class="theme-bar-name">
            <span>${themeIcons[stat.theme] || '📌'}</span>
            <span>${stat.theme}</span>
          </span>
          <div class="theme-bar-stats">
            ${isHighFriction ? `<span class="theme-friction-pill">${stat.negative_count} negative</span>` : ''}
            <span class="theme-bar-count">${stat.count} mentions</span>
            <span>(${stat.percentage}%)</span>
          </div>
        </div>
        <div class="theme-progress-track">
          <div class="theme-progress-fill ${isHighFriction ? 'high-friction' : ''}" style="width: 0%"></div>
        </div>
      `;

      container.appendChild(row);

      // Trigger width animation on next tick
      setTimeout(() => {
        const fill = row.querySelector('.theme-progress-fill');
        if (fill) {
          fill.style.width = `${Math.max(percentageOfMax, 4)}%`;
        }
      }, 50);
    });
  }
};

window.Charts = Charts;
