#!/usr/bin/env python3
"""Fetch papers from Google Scholar and generate portfolio HTML snippets."""

import json
import re
import urllib.request

SCHOLAR_URL = "https://scholar.google.com/citations?user=fiMTSDcAAAAJ&hl=en"

papers = [
    {
        "title": "Solana Alpenglow Consensus",
        "authors": "Q. Kniep, J. Sliwinski, R. Wattenhofer",
        "year": 2025,
        "venue": "",
        "citations": 5,
        "self_author": "Q. Kniep",
    },
    {
        "title": "Pilotfish: Distributed Transaction Execution for Lazy Blockchains",
        "authors": "Q. Kniep, L. Kokoris-Kogias, A. Sonnino, I. Zablotchi, N. Zhang",
        "year": 2024,
        "venue": "",
        "citations": 10,
        "self_author": "Q. Kniep",
    },
    {
        "title": "Halting the Solana blockchain with epsilon stake",
        "authors": "J. Sliwinski, Q. Kniep, R. Wattenhofer, F. Schaich",
        "year": 2024,
        "venue": "DISC 2024",
        "citations": 10,
        "self_author": "Q. Kniep",
    },
    {
        "title": "Byzantine Fault-Tolerant Aggregate Signatures",
        "authors": "Q. Kniep, R. Wattenhofer",
        "year": 2024,
        "venue": "ASIA CCS 2024",
        "citations": 4,
    },
    {
        "title": "Quantifying Liveness and Safety of Avalanche's Snowball",
        "authors": "Q. Kniep, M. Laval, J. Sliwinski, R. Wattenhofer",
        "year": 2024,
        "venue": "ESORICS 2024",
        "citations": 1,
    },
    {
        "title": "Tyche: Collateral-free coalition-resistant multiparty lotteries with arbitrary payouts",
        "authors": "Q. Kniep, R. Wattenhofer",
        "year": 2024,
        "venue": "",
        "citations": 1,
    },
    {
        "title": "DeFi and NFTs Hinder Blockchain Scalability",
        "authors": "L. Heimbach, Q. Kniep, Y. Vonlanthen, R. Wattenhofer",
        "year": 2023,
        "venue": "FC 2023",
        "citations": 25,
    },
    {
        "title": "Dissecting the EIP-2930 Optional Access Lists",
        "authors": "L. Heimbach, Q. Kniep, Y. Vonlanthen, R. Wattenhofer, P. Züst",
        "year": 2023,
        "venue": "",
        "citations": 11,
    },
    {
        "title": "Post-Quantum Cryptography in WireGuard VPN",
        "authors": "Q.M. Kniep, W. Müller, J.P. Redlich",
        "year": 2020,
        "venue": "SecureComm 2020",
        "citations": 7,
    },
    {
        "title": "Post-Quantum FIDO2 Security Keys using Hash-Based Signatures",
        "authors": "Q.M. Kniep",
        "year": 2021,
        "venue": "",
        "citations": 0,
    },
    {
        "title": "Mangrove: Fast and parallelizable state replication for blockchains",
        "authors": "A. Paramonov, Y. Vonlanthen, Q. Kniep, J. Sliwinski, R. Wattenhofer",
        "year": 2025,
        "venue": "",
        "citations": 1,
    },
]

for p in papers:
    # highlight self in authors
    authors_html = re.sub(
        r"(Q\.M?\.?\s*Kniep)",
        r'<span class="self">\1</span>',
        p["authors"],
    )
    p["authors_html"] = authors_html

    # slug for filenames
    slug = re.sub(r"[^a-z0-9]+", "-", p["title"].lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    p["slug"] = slug

    # venue tag
    if p["venue"]:
        p["venue_tag"] = f'\n            <span class="tag venue">{p["venue"]}</span>'
    else:
        p["venue_tag"] = ""

    # tags
    tags = []
    title_lower = p["title"].lower()
    if "consensus" in title_lower:
        tags.append("Consensus")
    if "blockchain" in title_lower or "solana" in title_lower:
        tags.append("Blockchain")
    if "byzantine" in title_lower or "fault-tolerant" in title_lower:
        tags.append("BFT")
    if (
        "cryptograph" in title_lower
        or "post-quantum" in title_lower
        or "signature" in title_lower
    ):
        tags.append("Cryptography")
    if "defi" in title_lower or "nft" in title_lower:
        tags.append("DeFi")
    if "wireguard" in title_lower or "vpn" in title_lower:
        tags.append("Networking")
    if "liveness" in title_lower or "safety" in title_lower:
        tags.append("Formal Methods")
    if "lottery" in title_lower or "multiparty" in title_lower:
        tags.append("Game Theory")
    if "transaction" in title_lower or "execution" in title_lower:
        tags.append("Distributed Systems")
    if "state" in title_lower or "replication" in title_lower:
        tags.append("Systems")
    if "access list" in title_lower or "eip" in title_lower:
        tags.append("Ethereum")

    p["tags_html"] = "\n            ".join(
        f'<span class="tag">{t}</span>' for t in tags
    )

with open("papers.json", "w") as f:
    json.dump(papers, f, indent=2)

print(f"Saved {len(papers)} papers to papers.json")
