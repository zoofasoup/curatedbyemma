"""
Indonesian Contextual Reply Generator for Shopee Affiliate Bot.
Evaluates Indonesian Threads complaints and crafts authentic, empathetic replies
using cloaked clean links (curatedbyemma.pages.dev/go/[slug]) and closing conversation magnets.
"""

import os
import sys
import json
import re

CATALOG_ID = {
    "serbuk": {
        "slug": "serbuk",
        "title": "Serbuk Ajaib Pembersih Kerak Wajan & Panci Gosong",
        "category": "Pembersih kerak wajan / panci",
        "keywords": ["wajan", "gosong", "kerak", "panci", "pantat panci", "kerak minyak", "alat masak hitam", "membersihkan wajan"],
        "drafts": [
            "asli relate bgt dulu wajan gue gosong ampe mau dibuang wkwk. akhirnya nemu serbuk pembersih ini ampuh bgt ga pake tenaga keraknya langsung rontok: curatedbyemma.pages.dev/go/serbuk jangan lupa pas oles pake sarung tangan ya. wajan lu bahan stainless apa teflon?",
            "panci gosong kalo disikat kawat doang emg bikin tangan kapalan wkwk. mending tabur serbuk pembersih ini diemin 15 menit langsung kinclong: curatedbyemma.pages.dev/go/serbuk keraknya tebel bgt ga di bagian bawahnya?"
        ]
    },
    "rak": {
        "slug": "rak",
        "title": "Rak Gantung Sudut Kamar Mandi Tempel Tanpa Bor",
        "category": "Kosan / Kamar mandi sempit",
        "keywords": ["kamar mandi sempit", "kamar mandi kosan", "ga boleh ngebor", "botol sabun berantakan", "rak sudut", "tempat sabun", "kamar mandi kecil"],
        "drafts": [
            "buat anak kosan yg ga boleh ngebor tembok mending pake rak sudut tempel ini deh, lemnya kuat bgt ga gampang copot: curatedbyemma.pages.dev/go/rak kamar mandi jd lega ga ada botol berantakan di lantai. tembok kamar mandi lu keramik licin kan?",
            "kamar mandi sempit emg paling bener pake rak gantung sudut tempel biar lantainya ga sumpek wkwk. gue pake yg ini kokoh bgt: curatedbyemma.pages.dev/go/rak lu botol sabun sama shampoonya banyak ya?"
        ]
    },
    "pel": {
        "slug": "pel",
        "title": "Alat Pel Putar Otomatis Flat Mop Peras Sendiri",
        "category": "Alat pel praktis",
        "keywords": ["ngepel", "kain pel", "meras pel", "tangan kotor", "lantai basah", "males ngepel", "alat pel"],
        "drafts": [
            "ngepel pake kain pel biasa emg paling bikin males pas merasnya wkwk. gue ganti ke flat mop yg bisa peras sendiri ini: curatedbyemma.pages.dev/go/pel tangan ga basah kotor sama sekali dan cepet kering. kosan lu lantainya luas bgt ga?",
            "gue dulu juga males bgt ngepel grgr jijik meras air kotornya wkwk. pas pake flat mop hands-free ini jd sat-set bgt beresnya: curatedbyemma.pages.dev/go/pel lu biasanya ngepel seminggu berapa kali?"
        ]
    },
    "tawas": {
        "slug": "tawas",
        "title": "Deodorant Tawas Spray Alami Non-Alkohol",
        "category": "Bodycare / Bau ketiak",
        "keywords": ["bau ketiak", "bau badan", "ketiak", "deodorant", "bau asem", "ketiak item", "deodorant ga mempan", "burket", "ketiak basah", "ketiak bau"],
        "drafts": [
            "kalo roll-on biasa bikin baju kuning & ketiak item, coba switch ke tawas spray alami ini deh, seharian bebas bau asem: curatedbyemma.pages.dev/go/tawas beneran ga ada residu putih di baju. lu biasanya pake deodorant roll-on atau spray?",
            "tawas spray beneran holy grail buat yg gampang keringetan dan bau asem wkwk. ga lengket sama sekali dan ga noda di baju putih: curatedbyemma.pages.dev/go/tawas kulit ketiak lu sensitif ga kalo kena wangi-wangian?"
        ]
    },
    "acne": {
        "slug": "acne",
        "title": "Hydrocolloid Acne Patch Penghisap Nanah Jerawat",
        "category": "Skincare Jerawat",
        "keywords": ["jerawat mendem", "jerawat batu", "jerawat mateng", "pengen mencet jerawat", "acne patch", "jerawat bernanah", "bopeng jerawat"],
        "drafts": [
            "jangan pernah dipencet paksa ntar bopeng dan berbekas! tempelin hydrocolloid acne patch ini pas tidur, paginya nanahnya kesedot tuntas: curatedbyemma.pages.dev/go/acne tipis bgt jd ga keliatan kalo dipake keluar. jerawatnya tipe mendem sakit atau udah bermata?",
            "kalo tangan gatel pengen mencet mending langsung tutupin pake acne patch ini deh biar ga kena kuman tangan: curatedbyemma.pages.dev/go/acne paginya langsung kempes ga berbekas hitam. lu jerawatnya sering muncul di pipi atau jidat?"
        ]
    }
}

def evaluate_and_draft_id(post_text: str, author: str = "user") -> dict:
    """
    Evaluates Indonesian Threads complaints and returns matched product,
    safe cloaked link, and conversational 5-part reply.
    """
    t = post_text.lower()
    
    # Negative filter (banned / irrelevant context)
    banned = ["judi", "slot", "gacor", "politik", "anies", "prabowo", "gibran", "dpr", "kpop", "giveaway", "olshop", "open bo", "promo", "voucher"]
    if any(b in t for b in banned):
        return {"verdict": "REJECT", "reason": "Banned or political/spam context"}

    best_match = None
    highest_score = 0

    for slug, data in CATALOG_ID.items():
        score = sum(1 for kw in data["keywords"] if kw in t)
        if score > highest_score:
            highest_score = score
            best_match = slug

    if not best_match or highest_score == 0:
        return {"verdict": "REJECT", "reason": "No matching problem solver in Indo catalog"}

    spec = CATALOG_ID[best_match]
    drafts = spec["drafts"]
    chosen_draft = drafts[abs(hash(post_text)) % len(drafts)]

    return {
        "verdict": "ACCEPT",
        "slug": best_match,
        "product_name": spec["title"],
        "reply_draft": chosen_draft,
        "cloaked_url": f"https://curatedbyemma.pages.dev/go/{best_match}",
        "reason": f"Matched Indonesian pain point: {spec['category']}"
    }

if __name__ == "__main__":
    test_complaints = [
        "Wajan teflon gue udah gosong banget pantatnya ada kerak hitam tebel, bersihin pake apa ya?",
        "Kamar mandi kosan gue sempit banget gila, botol sabun shampoo bertebaran di lantai ga boleh ngebor tembok lagi sama ibu kos",
        "Capek bgt tiap hari ngepel, pas meras kain pelnya air kotornya bikin tangan bau",
        "Udah ganti 3 merk deodorant ketiak tetep bau asem kalo siang, baju seragam sampe kuning",
        "Ada jerawat batu mateng banget di pipi cenat-cenut sakit gatel pengen gue pencet rasanya"
    ]

    for c in test_complaints:
        res = evaluate_and_draft_id(c)
        print(f"Complaint: {c[:60]}...")
        print(f"Verdict: {res['verdict']} | Product: {res.get('product_name')}")
        print(f"Draft: {res.get('reply_draft')}\n")
