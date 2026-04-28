(function () {
  function escapeHtml(value) {
    return (value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function normalize(value) {
    return (value || "")
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s]+/gu, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function getTokens(query) {
    return normalize(query).split(" ").filter(Boolean);
  }

  function buildSnippet(text, tokens) {
    const plain = (text || "").replace(/\s+/g, " ").trim();
    if (!plain) return "";

    const lowerPlain = plain.toLowerCase();
    let position = -1;
    let matchLength = 0;

    for (let i = 0; i < tokens.length; i += 1) {
      const currentPosition = lowerPlain.indexOf(tokens[i].toLowerCase());
      if (currentPosition !== -1) {
        position = currentPosition;
        matchLength = tokens[i].length;
        break;
      }
    }

    if (position === -1) {
      return plain.slice(0, 180) + (plain.length > 180 ? "..." : "");
    }

    const start = Math.max(0, position - 70);
    const end = Math.min(plain.length, position + Math.max(matchLength, 1) + 140);
    const prefix = start > 0 ? "..." : "";
    const suffix = end < plain.length ? "..." : "";
    return prefix + plain.slice(start, end).trim() + suffix;
  }

  function highlightMatches(text, tokens) {
    let output = escapeHtml(text);
    const uniqueTokens = Array.from(new Set(tokens)).sort(function (a, b) {
      return b.length - a.length;
    });

    uniqueTokens.forEach(function (token) {
      const pattern = new RegExp("(" + escapeRegExp(escapeHtml(token)) + ")", "gi");
      output = output.replace(pattern, '<mark class="search-highlight">$1</mark>');
    });

    return output;
  }

  function scoreEntry(entry, query, tokens) {
    const title = normalize(entry.title);
    const content = normalize(entry.content);
    const category = normalize(entry.category);
    let score = 0;

    if (query && title.includes(query)) score += 60;
    if (query && content.includes(query)) score += 30;

    for (let i = 0; i < tokens.length; i += 1) {
      const token = tokens[i];
      if (!title.includes(token) && !content.includes(token) && !category.includes(token)) {
        return -1;
      }

      if (title.includes(token)) score += 12;
      if (category.includes(token)) score += 6;
      if (content.includes(token)) score += 3;
    }

    return score;
  }

  function renderResults(results, query, elements) {
    const status = elements.status;
    const container = elements.results;

    if (!query) {
      status.textContent = "Type to start searching.";
      container.innerHTML = "";
      return;
    }

    status.textContent = results.length
      ? results.length + ' results matching "' + query + '"'
      : 'No results matching "' + query + '"';

    if (!results.length) {
      container.innerHTML = '<div class="search-empty">Try a different keyword or a shorter phrase.</div>';
      return;
    }

    container.innerHTML = results.map(function (result) {
      const meta = [result.type, result.category, result.lang].filter(Boolean).join(" · ");
      const snippet = highlightMatches(buildSnippet(result.content, result.tokens), result.tokens);

      return (
        '<article class="search-card">' +
          '<div class="search-meta">' + escapeHtml(meta) + '</div>' +
          '<h3><a href="' + result.url + '">' + escapeHtml(result.title) + '</a></h3>' +
          '<p class="search-snippet">' + snippet + '</p>' +
        '</article>'
      );
    }).join("");
  }

  document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("site-search-input");
    const status = document.getElementById("search-status");
    const results = document.getElementById("search-results");

    if (!input || !status || !results) return;

    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get("q") || "";
    const elements = { status: status, results: results };
    let searchIndex = [];

    status.textContent = "Loading search index...";
    results.innerHTML = '<div class="search-loading">Loading...</div>';

    fetch("/search-index.json")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        searchIndex = Array.isArray(data) ? data : [];
        input.value = initialQuery;
        runSearch(initialQuery);
      })
      .catch(function () {
        status.textContent = "Search index could not be loaded.";
        results.innerHTML = '<div class="search-empty">Search is temporarily unavailable.</div>';
      });

    function updateUrl(query) {
      const url = new URL(window.location.href);
      if (query) {
        url.searchParams.set("q", query);
      } else {
        url.searchParams.delete("q");
      }
      window.history.replaceState({}, "", url);
    }

    function runSearch(rawQuery) {
      const query = normalize(rawQuery);
      const tokens = getTokens(rawQuery);

      if (!query) {
        renderResults([], "", elements);
        updateUrl("");
        return;
      }

      const matched = searchIndex
        .map(function (entry) {
          const score = scoreEntry(entry, query, tokens);
          return score < 0 ? null : {
            title: entry.title,
            url: entry.url,
            content: entry.content,
            lang: entry.lang,
            category: entry.category,
            type: entry.type,
            score: score,
            tokens: tokens
          };
        })
        .filter(Boolean)
        .sort(function (a, b) {
          return b.score - a.score;
        })
        .slice(0, 50);

      renderResults(matched, rawQuery.trim(), elements);
      updateUrl(rawQuery.trim());
    }

    input.addEventListener("input", function () {
      runSearch(input.value);
    });
  });
})();
