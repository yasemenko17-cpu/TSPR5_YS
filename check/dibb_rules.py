"""Правила перевірки артефакту частини Б: ланцюжок DIBB і пітч Shape Up (форма й узгодженість, а не зміст).

Артефакт лежить у файлі dibb/my_dibb.json; формат показано в dibb/format_example.json.
Кожне правило повертає список зауважень; порожній список означає, що правило виконано.
Запуск: pytest check -q (змінна DIBB задає інший файл).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPETITES = (1, 2, 6)
ALLOWED_UNKNOWN = {1: 1, 2: 2, 6: 3}
TOP = ("product", "data", "insights", "beliefs", "bets", "pitch", "decision", "review")
ID = {"data": r"D\d+", "insights": r"I\d+", "beliefs": r"B\d+", "bets": r"T\d+"}
REFS = {"insights": ("data", "data"), "beliefs": ("insights", "insights"), "bets": ("beliefs", "beliefs")}
MIN_COUNT = {"data": 4, "insights": 3, "beliefs": 2, "bets": 2}


def load_artifact(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def words(text):
    return len(str(text).split())


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def items(art, key):
    value = art.get(key)
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def text_problem(label, text, minimum):
    if not isinstance(text, str) or words(text) < minimum:
        return [f"{label}: потрібно щонайменше {minimum} слів"]
    return []


def rule_structure(art):
    problems = [f"немає розділу {k}" for k in TOP if k not in art]
    for k in ("data", "insights", "beliefs", "bets", "review"):
        if k in art and not isinstance(art[k], list):
            problems.append(f"{k} має бути списком")
    for k in ("product", "pitch", "decision"):
        if k in art and not isinstance(art[k], dict):
            problems.append(f"{k} має бути об'єктом")
    return problems


def rule_product(art):
    p = art.get("product")
    if not isinstance(p, dict):
        return ["немає розділу product"]
    out = []
    for key, n in (("name", 2), ("audience", 3), ("north_star", 2)):
        out += text_problem(f"product.{key}", p.get(key), n)
    return out


def rule_data(art):
    rows = items(art, "data")
    out = [] if len(rows) >= MIN_COUNT["data"] else [f"потрібно щонайменше {MIN_COUNT['data']} записи даних, є {len(rows)}"]
    for r in rows:
        rid = r.get("id", "?")
        if not isinstance(rid, str) or not re.fullmatch(ID["data"], rid):
            out.append(f"{rid}: ідентифікатор має вигляд D1, D2, ...")
        out += text_problem(f"{rid}.what", r.get("what"), 4)
        out += text_problem(f"{rid}.source", r.get("source"), 2)
        if not isinstance(r.get("metric"), str) or not r.get("metric").strip():
            out.append(f"{rid}: немає назви метрики")
        if not is_num(r.get("value")) or not 0 <= r.get("value") <= 100:
            out.append(f"{rid}: value має бути числом від 0 до 100")
    return out


def chain_problems(art):
    """Та сама логіка, що в задачі 3, але для артефакту, який складає студент."""
    out, seen, rep = [], set(), set()
    for key in ("data", "insights", "beliefs", "bets"):
        for x in items(art, key):
            if x.get("id") in seen:
                rep.add(x.get("id"))
            seen.add(x.get("id"))
        n = len(items(art, key))
        if n < MIN_COUNT[key]:
            out.append(f"{key}: потрібно щонайменше {MIN_COUNT[key]}, є {n}")
    out += [f"повторний ідентифікатор {x}" for x in sorted(rep, key=str)]
    ids = {k: {x.get("id") for x in items(art, k)} for k in ID}
    for level, (field, target) in REFS.items():
        for x in items(art, level):
            refs = x.get(field)
            if not isinstance(refs, list) or not refs:
                out.append(f"{x.get('id')}: немає посилань у полі {field}")
                continue
            out += [f"{x.get('id')}: невідоме посилання {r}" for r in refs if r not in ids[target]]
    used = {"data": {r for x in items(art, "insights") for r in (x.get("data") or [])},
            "insights": {r for x in items(art, "beliefs") for r in (x.get("insights") or [])},
            "beliefs": {r for x in items(art, "bets") for r in (x.get("beliefs") or [])}}
    label = {"data": "дані без інсайту", "insights": "інсайт без переконання", "beliefs": "переконання без ставки"}
    for level in ("data", "insights", "beliefs"):
        out += [f"{x.get('id')}: {label[level]}" for x in items(art, level) if x.get("id") not in used[level]]
    return out


def rule_chain(art):
    return chain_problems(art)


def reachable_data(art, belief):
    insights = {x.get("id"): x for x in items(art, "insights")}
    data = {x.get("id"): x for x in items(art, "data")}
    found = []
    for i in belief.get("insights") or []:
        for d in (insights.get(i) or {}).get("data") or []:
            if d in data:
                found.append(data[d])
    return found


def rule_beliefs(art):
    out = []
    for b in items(art, "beliefs"):
        bid = b.get("id", "?")
        out += text_problem(f"{bid}.text", b.get("text"), 4)
        base, target = b.get("baseline"), b.get("target")
        if not (is_int(base) and is_int(target) and 0 <= base < target <= 100):
            out.append(f"{bid}: baseline і target мають бути цілими, 0 <= baseline < target <= 100")
            continue
        match = [d for d in reachable_data(art, b) if d.get("metric") == b.get("metric")]
        if not match:
            out.append(f"{bid}: жоден запис даних за посиланнями не має метрики «{b.get('metric')}»")
        elif all(d.get("value") != base for d in match):
            out.append(f"{bid}: baseline {base} не збігається зі значенням даних ({match[0].get('value')})")
    return out


def rule_bets(art):
    out = []
    beliefs = {b.get("id"): b for b in items(art, "beliefs")}
    for t in items(art, "bets"):
        tid = t.get("id", "?")
        out += text_problem(f"{tid}.title", t.get("title"), 2)
        out += text_problem(f"{tid}.experiment", t.get("experiment"), 4)
        if t.get("appetite_weeks") not in APPETITES or not is_int(t.get("appetite_weeks")):
            out.append(f"{tid}: апетит має бути 1, 2 або 6 тижнів")
        linked = [beliefs[r] for r in t.get("beliefs") or [] if r in beliefs]
        if linked and any(b.get("metric") != t.get("metric") for b in linked):
            out.append(f"{tid}: метрика ставки не збігається з метрикою переконання")
        me = t.get("min_effect_pp")
        if not is_num(me):
            out.append(f"{tid}: min_effect_pp має бути числом")
        elif linked:
            pairs = [(b.get("baseline"), b.get("target")) for b in linked]
            if all(is_int(x) and is_int(y) for x, y in pairs):
                planned = min(y - x for x, y in pairs)
                if not 0 < me <= planned:
                    out.append(f"{tid}: min_effect_pp має бути в межах від 0 до {planned}")
    return out


def rule_pitch_form(art):
    p = art.get("pitch")
    if not isinstance(p, dict):
        return ["немає розділу pitch"]
    out = []
    bets = {t.get("id"): t for t in items(art, "bets")}
    bet = bets.get(p.get("bet"))
    if bet is None:
        out.append(f"pitch.bet: невідома ставка {p.get('bet')}")
    elif bet.get("appetite_weeks") != p.get("appetite_weeks"):
        out.append("pitch.appetite_weeks не збігається з апетитом ставки")
    out += text_problem("pitch.problem", p.get("problem"), 15)
    solution = [e for e in p.get("solution") or [] if isinstance(e, dict)]
    if len(solution) < 3:
        out.append("pitch.solution: потрібно щонайменше 3 елементи")
    names = [e.get("name") for e in solution]
    if len(set(names)) != len(names) or any(not isinstance(n, str) or not n.strip() for n in names):
        out.append("pitch.solution: назви елементів мають бути непорожніми й унікальними")
    holes = [h for h in p.get("rabbit_holes") or [] if isinstance(h, dict)]
    closed = {h.get("element") for h in holes if words(h.get("resolution", "")) >= 2}
    for e in solution:
        if e.get("unknown") is True and e.get("name") not in closed:
            out.append(f"«{e.get('name')}»: невідоме без закритої нори")
    for h in holes:
        if h.get("element") not in names:
            out.append(f"нора для невідомого елемента «{h.get('element')}»")
    unknown = sum(e.get("unknown") is True for e in solution)
    if unknown == 0:
        out.append("pitch.solution: позначте хоча б один елемент як unknown (місце, де можна загрузнути)")
    if p.get("appetite_weeks") in ALLOWED_UNKNOWN and unknown > ALLOWED_UNKNOWN[p["appetite_weeks"]]:
        out.append(f"забагато невідомого: {unknown} замість допустимих {ALLOWED_UNKNOWN[p['appetite_weeks']]}")
    no_gos = p.get("no_gos")
    if not isinstance(no_gos, list) or len(no_gos) < 2:
        out.append("pitch.no_gos: потрібно щонайменше 2 пункти «не робимо»")
    else:
        low = {str(n).casefold() for n in names}
        out += [f"«{g}» одночасно в рішенні й у «не робимо»" for g in no_gos if str(g).casefold() in low]
    return out


def rule_pitch_scope(art):
    p = art.get("pitch")
    if not isinstance(p, dict):
        return ["немає розділу pitch"]
    scopes = [s for s in p.get("scopes") or [] if isinstance(s, dict)]
    out = []
    if len(scopes) < 3:
        return ["pitch.scopes: потрібно щонайменше 3 скоупи"]
    names = [s.get("name") for s in scopes]
    if len(set(names)) != len(names):
        out.append("pitch.scopes: назви мають бути унікальними")
    for s in scopes:
        if not is_int(s.get("weeks")) or s.get("weeks") < 1:
            out.append(f"скоуп «{s.get('name')}»: weeks має бути додатним цілим")
        if not isinstance(s.get("must"), bool):
            out.append(f"скоуп «{s.get('name')}»: must має бути true або false")
        if s.get("needs") and s["needs"] not in names:
            out.append(f"скоуп «{s.get('name')}»: невідома залежність «{s['needs']}»")
    teams = p.get("teams")
    if not is_int(teams) or teams < 1:
        out.append("pitch.teams має бути цілим не менше 1")
        return out
    if p.get("appetite_weeks") not in APPETITES or out:
        return out
    capacity = p["appetite_weeks"] * teams
    must = sum(s["weeks"] for s in scopes if s["must"])
    if must > capacity:
        out.append(f"обов'язкові скоупи ({must} тижн.) не вкладаються в апетит ({capacity} тижн.)")
    if all(s["must"] for s in scopes):
        out.append("усі скоупи обов'язкові: позначте хоча б один як необов'язковий (його можна вирізати)")
    return out


def rule_decision(art):
    d = art.get("decision")
    if not isinstance(d, dict):
        return ["немає розділу decision"]
    out = []
    bets = {t.get("id"): t for t in items(art, "bets")}
    cap = d.get("capacity_weeks")
    if not is_int(cap) or cap < 1:
        out.append("decision.capacity_weeks має бути додатним цілим")
    chosen = d.get("chosen")
    if not isinstance(chosen, list) or not chosen:
        out.append("decision.chosen: оберіть щонайменше одну ставку")
        chosen = []
    deferred = [x for x in d.get("deferred") or [] if isinstance(x, dict)]
    out += [f"decision.chosen: невідома ставка {c}" for c in chosen if c not in bets]
    out += [f"decision.deferred: невідома ставка {x.get('bet')}" for x in deferred if x.get("bet") not in bets]
    for x in deferred:
        out += text_problem(f"decision.deferred {x.get('bet')} (причина)", x.get("reason"), 3)
    seen = list(chosen) + [x.get("bet") for x in deferred]
    if set(seen) != set(bets) or len(seen) != len(set(seen)):
        out.append("кожна ставка має бути рівно в одному зі списків chosen і deferred")
    if is_int(cap) and all(c in bets for c in chosen):
        total = sum(bets[c].get("appetite_weeks", 0) for c in chosen if is_int(bets[c].get("appetite_weeks")))
        if total > cap:
            out.append(f"обрані ставки ({total} тижн.) перевищують місткість ({cap} тижн.)")
    pitch_bet = (art.get("pitch") or {}).get("bet") if isinstance(art.get("pitch"), dict) else None
    if pitch_bet and pitch_bet not in chosen:
        out.append("ставка з пітчу має бути серед обраних")
    if d.get("cooldown_weeks") != 2:
        out.append("decision.cooldown_weeks має дорівнювати 2")
    return out


def rule_review(art):
    rows = items(art, "review")
    out = [] if len(rows) >= 2 else ["review: потрібно щонайменше 2 записи"]
    for k, r in enumerate(rows, 1):
        out += text_problem(f"review[{k}].note", r.get("note"), 4)
    return out


RULES = [rule_structure, rule_product, rule_data, rule_chain, rule_beliefs, rule_bets, rule_pitch_form,
         rule_pitch_scope, rule_decision, rule_review]
