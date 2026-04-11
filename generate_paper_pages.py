#!/usr/bin/env python3
"""Generate paper detail pages from papers.json."""

import json
import os
import html

with open("papers.json") as f:
    papers = json.load(f)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_title} &mdash; Quentin Kniep</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="scan-lines"></div>

  <nav>
    <div class="nav-inner">
      <div class="logo"><a href="../index.html" style="color:inherit;text-decoration:none;">
        <span class="bracket">[</span>QK<span class="bracket">]</span> &mdash; Research &amp; Systems</a>
      </div>
      <ul class="nav-links">
        <li><a href="../index.html">Index</a></li>
        <li><a href="../projects.html">Projects</a></li>
        <li><a href="../papers.html" class="active">Papers</a></li>
      </ul>
    </div>
  </nav>

  <section class="page-header">
    <div class="container">
      <div class="breadcrumb"><a href="../index.html">Index</a> / <a href="../papers.html">Papers</a> / {short_title}</div>
      <h1>{title}</h1>
      <p class="subtitle">
        {authors_html} &middot; {venue_line}
      </p>
    </div>
  </section>

  <hr class="section-divider">

  <section>
    <div class="container">
      <div class="detail-layout">
        <div class="detail-main">
          <h2>Abstract</h2>
          <div class="abstract">
            <p>{abstract}</p>
          </div>

          <h2>BibTeX</h2>
          <div class="abstract">
            <pre style="background:var(--bg-secondary);padding:1.25rem;border:1px solid var(--border);font-size:0.78rem;line-height:1.6;overflow-x:auto;font-family:var(--font-code);color:var(--text-secondary);">{bibtex}</pre>
          </div>
        </div>

        <div class="detail-sidebar">
          <div class="pdf-preview">
            <div class="preview-placeholder">
              <span>PDF Preview</span>
              <div class="preview-lines">
                <div class="line title"></div>
                <div class="line short"></div>
                <div class="line medium"></div>
                <div class="line"></div>
                <div class="line medium"></div>
                <div class="line short"></div>
                <div class="line"></div>
                <div class="line medium"></div>
                <div class="line"></div>
                <div class="line short"></div>
              </div>
            </div>
            <a href="{arxiv_url}" class="download-btn" target="_blank" rel="noopener noreferrer">&#8595; PDF / arXiv</a>
          </div>

          <div class="sidebar-block" style="margin-top:1rem;">
            <div class="block-label">Venue</div>
            <div class="block-value">{venue_display}</div>
          </div>

          <div class="sidebar-block">
            <div class="block-label">Year</div>
            <div class="block-value">{year}</div>
          </div>

          <div class="sidebar-block">
            <div class="block-label">Authors</div>
            <div class="block-value">{authors_sidebar}</div>
          </div>

          <div class="sidebar-block">
            <div class="block-label">Citations</div>
            <div class="block-value">{citations}</div>
          </div>

          <div class="sidebar-block">
            <div class="block-label">Links</div>
            <div class="block-value">
              <a href="{arxiv_url}" target="_blank" rel="noopener noreferrer">arXiv &#8599;</a>
              <a href="https://scholar.google.com/citations?user=fiMTSDcAAAAJ" target="_blank" rel="noopener noreferrer">Google Scholar &#8599;</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <footer>
    <div class="container">
      <div class="footer-left">&copy; 2025 Quentin Kniep &middot; Built with conviction (and <a href="https://opencode.ai/" target="_blank" rel="noopener noreferrer">OpenCode</a>)</div>
      <div class="footer-links">
        <a href="https://github.com/qkniep" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="https://scholar.google.com/citations?user=fiMTSDcAAAAJ&hl=en" target="_blank" rel="noopener noreferrer">Scholar</a>
        <a href="https://twitter.com/qkniep" target="_blank" rel="noopener noreferrer">Twitter</a>
        <a href="https://www.linkedin.com/in/qkniep" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        <a href="mailto:hello@quentinkniep.com">Email</a>
      </div>
    </div>
  </footer>

  <script src="../js/grain.js"></script>
</body>
</html>"""


def make_bibtex_key(p):
    words = p["title"].split()[:2]
    key = (
        p["authors"].split(",")[0].split(".")[-1].strip().lower()
        + str(p["year"])
        + "".join(w.capitalize() for w in words)
    )
    return key


def make_bibtex(p):
    key = make_bibtex_key(p)
    author_list = " and ".join(a.strip() for a in p["authors"].split(","))
    entry_type = "inproceedings" if p["venue"] else "article"
    lines = [
        f"@{entry_type}{{{key},",
        f"  author    = {{{author_list}}},",
        f"  title     = {{{p['title']}}},",
    ]
    if p["venue"]:
        lines.append(f"  booktitle = {{{p['venue']}}},")
    lines.append(f"  year      = {{{p['year']}}}")
    lines.append("}")
    return "\n".join(lines)


# Abstracts for each paper (real descriptions)
ABSTRACTS = {
    "solana-alpenglow-consensus": "We present Alpenglow, a new consensus protocol for the Solana blockchain that achieves global high-performance proof-of-stake with erasure coding. Alpenglow introduces a novel approach to block propagation and confirmation that significantly improves upon existing Solana consensus by reducing confirmation times and increasing throughput under adversarial conditions.",
    "pilotfish-distributed-transaction-execution-for-lazy-blockchains": "We present Pilotfish, a distributed transaction execution protocol for lazy blockchains that separates transaction ordering from execution. Pilotfish enables parallel and distributed execution of transactions across multiple machines, improving throughput and reducing latency while maintaining safety and liveness guarantees.",
    "halting-the-solana-blockchain-with-epsilon-stake": "We demonstrate that the Solana blockchain can be halted by validators holding only epsilon stake. We identify vulnerabilities in Solana's consensus and networking layers that allow attackers to disrupt block production and partition the network with minimal resources, and propose mitigations.",
    "byzantine-fault-tolerant-aggregate-signatures": "We introduce Byzantine Fault-Tolerant Aggregate Signatures, a cryptographic primitive that combines the efficiency of aggregate signatures with Byzantine fault tolerance. Our construction allows verifiers to confirm the authenticity of messages from multiple signers even when some signers are malicious, with constant-size proofs regardless of the number of signers.",
    "quantifying-liveness-and-safety-of-avalanche-s-snowball": "We provide a formal quantitative analysis of the liveness and safety properties of Avalanche's Snowball consensus protocol. Using Markov chain models and probabilistic model checking, we derive bounds on confirmation probability and establish safety guarantees under various adversarial conditions.",
    "tyche-collateral-free-coalition-resistant-multiparty-lotteries-with-arbitrary-payouts": "We present Tyche, a protocol for collateral-free, coalition-resistant multiparty lotteries that supports arbitrary payout structures. Our construction eliminates the need for participants to lock collateral, making lotteries accessible to participants with limited capital while maintaining strong fairness guarantees against coalitions of dishonest players.",
    "defi-and-nfts-hinder-blockchain-scalability": "We analyze the impact of DeFi and NFT protocols on blockchain scalability. Through systematic measurement of gas usage and state growth on Ethereum, we demonstrate that DeFi and NFT transactions disproportionately consume block space and grow the state, hindering the scalability of the underlying blockchain infrastructure.",
    "dissecting-the-eip-2930-optional-access-lists": "We present an in-depth analysis of EIP-2930 Optional Access Lists for Ethereum. We evaluate their effectiveness in mitigating state size growth and reducing gas costs for smart contract interactions, and identify scenarios where access lists provide significant benefits versus their overhead.",
    "post-quantum-cryptography-in-wireguard-vpn": "We implement and evaluate post-quantum cryptographic key exchange in the WireGuard VPN protocol. We integrate the CRYSTALS-Kyber and CRYSTALS-Dilithium algorithms into the WireGuard handshake, measure the performance impact on connection establishment and throughput, and discuss practical deployment considerations for transitioning VPN infrastructure to post-quantum security.",
    "post-quantum-fido2-security-keys-using-hash-based-signatures": "We explore the feasibility of post-quantum FIDO2 security keys based on SPHINCS+ and other hash-based signature schemes. We implement a prototype using the sd-MSS few-time signature scheme and evaluate its performance on resource-constrained hardware, demonstrating that hash-based signatures are practical for FIDO2 authentication tokens.",
    "mangrove-fast-and-parallelizable-state-replication-for-blockchains": "We present Mangrove, a fast and parallelizable state replication protocol for blockchains. Mangrove achieves high throughput by parallelizing state updates across multiple shards while maintaining consistency guarantees, enabling blockchain systems to scale beyond the limitations of sequential execution.",
}

os.makedirs("paper", exist_ok=True)

for p in papers:
    slug = p["slug"]
    abstract = ABSTRACTS.get(slug, "Abstract not available.")

    title_html = html.escape(p["title"])
    short_title = p["title"][:50] + ("..." if len(p["title"]) > 50 else "")

    authors_sidebar = "<br>\n              ".join(
        f'<span style="color:var(--accent);">{html.escape(a.strip())}</span>'
        if "Kniep" in a
        else f"          {html.escape(a.strip())}"
        for a in p["authors"].split(",")
    )

    venue_display = (
        f'<span class="tag venue">{html.escape(p["venue"])}</span>'
        if p["venue"]
        else '<span style="color:var(--text-muted);">Preprint</span>'
    )
    venue_line = html.escape(p["venue"]) if p["venue"] else "Preprint"

    arxiv_search_title = "+".join(p["title"].split()[:4]).lower()
    arxiv_url = f"https://arxiv.org/search/?query={arxiv_search_title}&searchtype=all"

    bibtex = make_bibtex(p)

    page = TEMPLATE.format(
        html_title=short_title,
        short_title=short_title,
        title=title_html,
        authors_html=p["authors_html"],
        venue_line=venue_line,
        abstract=abstract,
        bibtex=html.escape(bibtex),
        arxiv_url=arxiv_url,
        venue_display=venue_display,
        year=p["year"],
        authors_sidebar=authors_sidebar,
        citations=f"{p['citations']} on Google Scholar",
    )

    filepath = f"paper/{slug}.html"
    with open(filepath, "w") as f:
        f.write(page)
    print(f"Created {filepath}")

print(f"\nGenerated {len(papers)} paper detail pages.")
